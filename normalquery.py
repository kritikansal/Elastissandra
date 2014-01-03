import subprocess
import ast
import os
import json
import csv
import sys
import re
if len( sys.argv ) < 2:
	print "You must provide a file path"
	sys.exit(0)
file_path=os.path.abspath( sys.argv[1])
reader = csv.reader( open(file_path), delimiter=",")
header = reader.next()
print header
output = open('out.json', "wb")
data = []
def hasher( lst ):
	ret = {}
	for item in lst:
	    ret[item[0]] = item[1]
	return ret
	#print "Converting..."
i=0
for row in reader:
	i=i+1
  	data.append( hasher( zip( header, row ) ) )
print "Writting..."
final={};
for key in data:
	final[key['Tweet_ID']]=key;
	n=key['Tweet_ID'];
#json.dump( final, output)
output.close()
import pycassa
import time
import json
from elasticsearch import Elasticsearch
from datetime import date
from pprint import pprint
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
pool=ConnectionPool('Twitter',['localhost:9160'])
col_fam=ColumnFamily(pool,'Tweets')
#s={'article3': {'author': 'Monam ', 'data': 'ye kya bc kaat rhe hai hum opps BC!!!!!!','time_of_addition': time.strftime("%c") },'article4': { 'author': 'Kriti' ,'data' : 'yaar  bakwass hai ye kuch ni hona iss project ka','time_of_addition':time.strftime("%c")}}
#print s;
print final[n];
s=final;
print s[n];
col_fam.batch_insert(s)

es=Elasticsearch(["localhost:9200", "localhost:9200"])
count=1;
for key in s.keys():
	#print key
	#print s[key]['data']
	content1=s[key]['Tweet_Data'];
#	l=content1.split()
	#print l;
	for word in re.findall(r"\w+", content1):
		word=word.lower();
		t={"name":"'"+word+"'",'docid': "'"+key+"'"}
	#print t
#	res=es.index(index="twitter", doc_type=word, id=count, body=t)
		os.system("curl -XPUT http://localhost:9200/twitter/tweet/"+str(count) +" -d '"+str(t)+"' >> out");
		count=count+1
		#print res

def Tweet_Comment(res):
	for entry in res['hits']['hits']:
		print dict(col_fam.get(entry['_source']['docname']))['Tweet_Comment']
def Tweet_ID(res):
	for entry in res['hits']['hits']:
		print dict(col_fam.get(entry['_source']['docname']))['Tweet_ID']


def Tweet_Time(res):
	for entry in res['hits']['hits']:
		print dict(col_fam.get(entry['_source']['docname']))['Tweet_Time']


def Tweet_User(res):
	for entry in res['hits']['hits']:
		print dict(col_fam.get(entry['_source']['docname']))['Tweet_User']

def Tweet_Data(res):
#	print res
#	print res['hits']
	for entry in res['hits']['hits']:
#		print entry
		print dict(col_fam.get(entry['_source']['docname']))['Tweet_Data']


#print res['hits']['hits']

y=raw_input("Enter Query type:")
x=raw_input("Enter Query String:")

#r = es.get(index=x,doc_type='position',body={"query:{}"})
#print r
#try:
#res = es.search(index="twitter", body={"query":{"name": x}})
#res = es.search(index="twitter", body={"query": {"match_all": {}}})
#print res
#	s="http://localhost:9200/twitter/tweet/_search?q=name:\""+x+"\""
#	proc = subprocess.Popen(["curl", "-XGET",s], stdout=subprocess.PIPE, shell=True)
#	(res, err) = proc.communicate()
#print "Enter"
os.system("curl -XGET 'http://localhost:9200/twitter/tweet/_search?q=name:\""+x+"\"' > deed.txt");
#print "Exit"
#f=open("res","r");
#3s = open('deed.txt', 'r').read()
#print "read"
#print s
#r=s[0:]
#res=dict(r)
#print "loaded"
#print s
#print res
#	line=f.read();
#	print line
#	name = raw_input("> ")
#	if name in line:
#		print line[name]
#	res=ast.literal_eval(line)
#	res=json.loads(line)
#	splitLine = line.split()
#	res[(splitLine[0])] = ",".join(splitLine[1:])

#	res = dict([res.strip('{}').split(":"),])
if y=="Tweet_ID":
	Tweet_ID(res)
elif y=="Tweet_Data":
	Tweet_Data(res)
elif y=="Tweet_Time":
	Tweet_Time(res)
elif y=="Tweet_User":
	Tweet_User(res)
elif y=="Tweet_Comment":
	Tweet_Comment(res)

#except:
#print "\n"
#print("Got %d Hits:" % res['hits']['total'])
#for hit in res['hits']['hits']:
