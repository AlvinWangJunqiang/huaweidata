#coding="utf-8"
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from othertools import joindictlst,dictfind          
from readsql import readdata,retalldata,groupinfo
import itertools as itl
import collections as col
from dealseq import *
import json
import pprint
import copy
from toexcel import filterrules
''' fucking the terrible encode and decode  '''

def translate_rule(rulelist_func,indexhouxu):
    '''��name��123����ӳ�䵽���ݿ��е����֣����������ﴦ���������⣬�Լ�������ļ���'''
    newrulelist=[]
    for arule in rulelist_func:
        front,back,confidence=arule
        front_new=[dictfind(key,Namemap) for key in front]
        back_new=[dictfind(key1,Namemap) for key1 in back]
        x_support=houxu[indexhouxu].get(front,'none')
        y_support=houxu[indexhouxu].get(back,'none')
        newrulelist.append([front_new,back_new,confidence,x_support,y_support])
    return newrulelist
        
def write_rule_excel(torulelist_func,name):
    '''�����Ž�����д�뵽xls�ļ���,��ͬ��Ԫ��index��ͬ'''
    workbook = xlwt.Workbook()    # ע�������Workbook����ĸ�Ǵ�д
    sheet1=workbook.add_sheet('sheet_1')
    sheet1.write(0,0,u'ǰ��')
    sheet1.write(0,1,u'x_support')
    sheet1.write(0,2,'back')
    sheet1.write(0,3,'y_support')
    sheet1.write(0,4,'confidence')
    row=1
    for amyrule in torulelist_func:
                    front,back,confidence,x_sum,y_sum=amyrule
                    front_text=' '.join(front)
                    back_text=' '.join(back)
                    confid=str(confidence)
                    sheet1.write(row,0,front_text)
                    sheet1.write(row,1,str(x_sum))
                    sheet1.write(row,2,back_text)
                    sheet1.write(row,3,str(y_sum))
                    sheet1.write(row,4,confid)
                    row+=1                            
    workbook.save(name+"test_excel.xls")
    
    
    
    
    
def write_rule_view(torulelist_func):
    '''�����Ž�����д�뵽txt�ļ���'''
    with open('D:/sun.txt','wb') as f:
        for amyrule in torulelist_func:
                front,back,confidence,x_count,y_count=amyrule
                for front_item in front:
                    print front_item,"--",
                print '\n'
                for back_item in back:
                        print back_item,
                print '\n'
                print confidence
                print x_count,y_count
                
                                 
def view():
    for ne in NEmap.values():
        for so in AlarmSmap.values():
            print len(structdata[ne][so])

def dealne(nename,structdata):
    '''ͳ�Ʋ�ͬ��Ԫ�ĺ�ѡ�����������ϲ���ͬ�ı���Ԫ�µļ�������alarmsource'''
    seqlst= [ i for i in structdata[nename].values() if len(i)>=2]  #�޶�Ԫ�ظ�������Ϊn������������������
    #counlst=map(seqdcit,seqlst)#���ý��̼��٣�cpu�ܼ���,����Ӧ��paitial
    cuntlst=[seqdcit(i,i[0][1]-5,60,4) for i in seqlst]  #���������ʱ�䴰��length���ظ�n
    houxuanji=joindictlst(cuntlst)
    return houxuanji
    


if __name__=="__main__":
    try:
      database=readdata("test","uiop.123.123",'root')
      con1=database.connectsql()  #��ʼ�����ݿ⣬���ݿ���Ϊ������Ĭ��Ϊutf-8
      data=retalldata(con1)       #�����ݿ��е����ݴ浽data����������ΪǶ�׵�tuple�������5������Ϊ�˲��Կɼ���,�����������Ϊ100��
      infos=groupinfo(con1)       #�����ֵ䣬����������Ϣ���������name��NE��alarmsource �����ͣ�����ӳ�䵽"1-n"     
      datatest=data
      #print len(datatest)          #��NE��Name��alarmsourceӳ�䵽��1��200���� MSCServer��0��CGPOMU �� 1
      print u'���ݶ�ȡ��ɿ�ʼ����',len(data)
      NEmap=dict(zip(infos["NE"],xrange(len(infos["NE"])+2)) )
      Namemap=dict(zip(infos["Name"],xrange(len(infos["Name"])+2)))
      AlarmSmap=dict(zip(infos["AlarmSource"],xrange(len(infos["AlarmSource"])+2)))
      base1={i:col.deque() for i in AlarmSmap.values()}
      structdata={ne:copy.deepcopy(base1) for ne in NEmap.values()}
      count=0   #������������ݸ���
      errcount=0 #����ĸ���
      houxu=[]  #�����洢ÿ����Ԫ�±���������ֵ䣬ֱ�Ӵ��룬��ͬ��Ԫ��������ɵ��б�ͳ�Ƶ�ʱ�������￴��ѡ��������
      for item in datatest:
            name,AlarmSource,OccurenceTime,NE=item[1],item[2],int(item[4]),item[6]
            iteminfo=(Namemap[name],OccurenceTime)
            try:
              structdata[NEmap[NE]][AlarmSmap[AlarmSource]].append(iteminfo)  #���˿��Խ������������롣
              count+=1
            except Exception as e:
                errcount+=1
      for neid in sorted(NEmap.values()):
          houxu.append(dealne(neid,structdata))  #����Ϊֹ���к�ѡ�����������б���
       
      print u'��Ԫ1��ѡ��',len(houxu[1].keys())
      print 'items',houxu[1]==houxu[0]
      print count,"sucessful count",
      print errcount,"error count"
      rules=[rulemake(rudict,2,0.7) for rudict in houxu]   #֧�ֶ�Ϊ2�����Ŷ�Ϊ0.7,��������Ԫ���Ϊindex�Ĺ��򣬱�����Ԫ1->rule[1]
      print "dealing rules***"
      print len(rules),'NE in sum'
      print " ok no error deted"
      print u"trying to translate to chinese"
      #my_test_new_rule=translate_rule(sorted(rules[0],key=lambda x: x[-1]),0) #�������ŶȽ�������
      #print houxu[0].values()
      #print my_test_new_rule
      #write_rule_view(my_test_new_rule)
      #write_rule_excel(my_test_new_rule,0) #д��excel���Գɹ�����
      rules=[filterrules(a_lst_rule) for a_lst_rule in rules]  #ȥ�����������¹���
      print u'ȥ������ɹ�'
      newrulelst=[]
      for index_g,rule_my in enumerate(rules):
          newrulelst.append(translate_rule(sorted(rule_my,key=lambda x: x[-1]),index_g))
      '''for NE_index,rule_new in enumerate(newrulelst):
          write_rule_excel(rule_new,NE_index)'''
      sun1=0
      for rule_ne in newrulelst:
          write_rule_excel(rule_ne,str(sun1))
          sun1+=1
          
      print 'stop running'                
                
     
      
    except Exception as e:
         print str(e)
    finally:
         con1.close()