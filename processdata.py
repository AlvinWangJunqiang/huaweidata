#coding="utf-8"
def view():
    for ne in NEmap.values():
        for so in AlarmSmap.values():
            print len(structdata[ne][so])

def dealne(nename,structdata):
    seqlst= [ i for i in structdata[nename].values() if len(i)>=0]  #�޶�Ԫ�ظ�������Ϊn������������������
    #counlst=map(seqdcit,seqlst)#���ý��̼��٣�cpu�ܼ���,����Ӧ��paitial
    cuntlst=[seqdcit(i,i[0][1]-5,60,3) for i in seqlst]  #���������ʱ�䴰��length���ظ�n
    houxuanji=joindictlst(cuntlst)
    return houxuanji
    
from othertools import joindictlst,dictfind          
from readsql import readdata,retalldata,groupinfo
import itertools as itl
import collections as col
from dealseq import *
import json
import pprint

if __name__=="__main__":
    try:
      database=readdata("testsmall","uiop.123.123",'root')
      con1=database.connectsql()  #��ʼ�����ݿ⣬���ݿ���Ϊ������Ĭ��Ϊutf-8
      data=retalldata(con1)       #�����ݿ��е����ݴ浽data����������ΪǶ�׵�tuple�������5������Ϊ�˲��Կɼ���,�����������Ϊ100��
      infos=groupinfo(con1)       #�����ֵ䣬����������Ϣ���������name��NE��alarmsource �����ͣ�����ӳ�䵽"1-n"     
      datatest=data
      #print len(datatest)          #��NE��Name��alarmsourceӳ�䵽��1��200���� MSCServer��0��CGPOMU �� 1
      NEmap=dict(zip(infos["NE"],xrange(200)))
      Namemap=dict(zip(infos["Name"],xrange(200)))
      AlarmSmap=dict(zip(infos["AlarmSource"],xrange(200)))
      base1={i:col.deque() for i in AlarmSmap.values()}
      structdata={ne:base1.copy() for ne in NEmap.values()}
      count=0   #������������ݸ���
      errcount=0 #����ĸ���
      houxu=[]  #�����洢ÿ����Ԫ�±���������ֵ䣬ֱ�Ӵ��룬makerule
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
       
      print len(houxu)
      print u'��Ԫ1��ѡ��',len(houxu[1].keys())
      print 'items',sorted((houxu[1].items()))
      print 'sun values' ,houxu[0].values()
      sun1=[x for x in houxu[0].keys() if len(x)==1]
      sun2=[x for x in houxu[1].keys() if len(x)==1]
      print u"һ�����Ŀ"
      print len(sun1),len(sun2)
      print "names from NEmap",len(Namemap.values())
      print "names from sql",len(infos["Name"])
      print count,"sucessful count",
      print errcount,"error count"
      rules=[rulemake(rudict,2,0.7) for rudict in houxu]   #֧�ֶ�Ϊ2�����Ŷ�Ϊ0.7
      print "dumping rules***"
      fout=open("rules.json","w")
      strrules=rules[:] #a copy of rule
      for rulejihe in strrules: #���������룬����û�ɹ�
          for smallrule in rulejihe:
              front,back,confidece=smallrule
              strfront=[dictfind(i,Namemap) for i in front]
              strback=[dictfind(i,Namemap) for i in back]
              print >>fout,strfront,',',strback,',',confidece
      #json.dump(rules,fout)          
      print " ok no error deted"
    except Exception as e:
         print str(e)
    finally:
         con1.close()
         fout.close()