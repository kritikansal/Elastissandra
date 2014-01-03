import pycassa
import time
import json
import elasticsearch
from elasticsearch import Elasticsearch
from datetime import date
from pprint import pprint
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
pool=ConnectionPool('Big',['localhost:9160'])
col_fam=ColumnFamily(pool,'TweetData')
import subprocess
import ast
import os
import json
import csv
import sys
import re
es = elasticsearch.Elasticsearch([{"host": "localhost","port": 9200}])
def Tweet_Comment(res):
        for entry in res['hits']['hits']:
                print dict(col_fam.get(entry['_source']['docid']))['Tweet_Comment']
def Tweet_ID(res):
        for entry in res['hits']['hits']:
                print dict(col_fam.get(entry['_source']['docid']))['Tweet_ID']


def Tweet_Time(res):
        for entry in res['hits']['hits']:
                print dict(col_fam.get(entry['_source']['docid']))['Tweet_Time']


def Tweet_User(res):
        for entry in res['hits']['hits']:
                print dict(col_fam.get(entry['_source']['docid']))['Tweet_User']

def Tweet_Data(id):
 	print dict(col_fam.get(id))['Tweet_Data']
#       print res
#       print res['hits']
#        for entry in res['hits']['hits']:
#              print entry




from collections import defaultdict
from math import sqrt
import random
import os
import sys
import csv
import json
from random import randint
worddict={};
maptweet={}
def densify(x, n):
    d = [0] * n
    for i, v in x:
        d[i] = v
    return d


def dist(x, c):
    sqdist = 0.0
    tot=0
    for i, v in x:
        sqdist += (v*c[i])
	tot=tot+1
    if tot==0:
    	sqdist=0
    else:
	sqdist=sqdist/tot
    return sqdist


def mean(xs, l):
    c = [0.] * l
    n = 0
    for x in xs:
        for i, v in x:
            c[i] += v
        n += 1
    for i in xrange(l):
	if n>0:
        	c[i] /= n
    return c


centers=[];
def kmeans(k, xs, l, n_iter=1):
    for i in random.sample(xrange(len(xs)), k):
	    centers.append(densify(xs[i],l));
	    #print i	
    cluster = [None] * len(xs)
    currdist=[None] * len(xs)
    print "CENTERSEEEE",centers
    for _ in xrange(n_iter):
	val=0;
        for i in centers:
#		print "selected centorid:",i
		for ll in range(len(i)):
			if i[ll]>=1:
				word=worddict[ll];
#				word=vocab[
#				print "word searched: " ,word
#				os.system("curl -XGET 'http://localhost:9200/kmeans/tweet/_search?q=name:\""+word+"\"' > deed.txt");
				res=es.search(index="kmeans", body={"query": {"match": {"content": word}}})
#f=open("deed.txt","r")
#	x=f.read()
#	                	x=x.replace("name","\"name\"");
#				x=x.replace("docid","\"docid\"");
#				res=json.loads(x)
	                	for entry in res['hits']['hits']:
					ids=str(entry['_source']['title'])
#	idd="\'"+ids+"\'"
					print "IDSS",ids
#					print ids,maptweet[ids];
					tweetnumber=int(maptweet[ids])
					if(currdist[tweetnumber]==None):
						currdist[tweetnumber]=dist(xs[tweetnumber],i);
						cluster[tweetnumber]=val;
					else:
						dd=dist(xs[tweetnumber],i);
						if(dd<currdist[tweetnumber]):
							currdist[tweetnumber]=dd;
							cluster[tweetnumber]=val;
#					print cluster

	val=val+1;
	for i,j in enumerate(cluster):
		if j==None:
			assign=randint(0,k-1);
			cluster[i]=assign;
#		for j in range(1,k):
#			dd=dist(xs[i],centers[j]);
#			if minn>=dd:
#				minn=dd;
#				mx=j;
#		cluster[i]=mx;
	print "MAPTWEET IDSS",maptweet
        for j, c in enumerate(centers):
            members = (x for i, x in enumerate(xs) if cluster[i] == j)
            centers[j] = mean(members, l)

    return cluster
"""    for _ in xrange(n_iter):
        for i, x in enumerate(xs):
		minn=dist(xs[i],centers[0]);
		mx=0;
		for j in range(1,k):
			dd=dist(xs[i],centers[j]);
			if minn>=dd:
				minn=dd;
				mx=j;
		cluster[i]=mx;
        for j, c in enumerate(centers):
            members = (x for i, x in enumerate(xs) if cluster[i] == j)
            centers[j] = mean(members, l)
	    """

if __name__ == '__main__':
    # Cluster a bunch of text documents.
    import re
    import sys

    def usage():
        print("usage: %s k docs..." % sys.argv[0])
        print("    The number of documents must be >= k.")
        sys.exit(1)

    try:
        k = int(sys.argv[1])
    except ValueError():
        usage()
    if len(sys.argv) < 3:
        usage()

    vocab = {}
    xs = []
    args=[]
    filename = sys.argv[2];
    file_path=os.path.abspath(filename)
    reader = csv.reader( open(file_path), delimiter=",")
    header = reader.next()
    data = []
    def hasher( lst ):
        ret = {}
        for item in lst:
            ret[item[0]] = item[1]
        return ret
        #print "Converting..."


    final={};
    tweetno=0;
    mainn=[]
    i=0
    for row in reader:
        i=i+1
	print i
        data.append( hasher( zip( header, row ) ) )
	args.append(row[0])
        maptweet[row[0]]=tweetno;
	tweetno=tweetno+1;
        x = defaultdict(float)
	key=row[0];

        for w in re.findall(r"\w+", row[4]):
                plen=len(vocab);
		vocab.setdefault(w, len(vocab))
		nlen=len(vocab)
		if(plen<nlen):
			worddict[plen]=w;
                x[vocab[w]] += 1
		t={"name":"'"+w+"'",'docid': "'"+key+"'"}
#		os.system("curl -XPUT http://localhost:9200/kmeans/tweet/"+str(tweetno) +" -d '"+str(t)+"' >> out");
		es.index(
				index="kmeans",
				doc_type="blog_post",
				id=1,
				body={
					"title": key,
					"content": row[2],
#       "date": datetime.date(2013, 9, 24),     
				     }
			)

	mainn.append(key)
#	print "x==",x
#	print "vocab==",vocab
#	print "word==", worddict
        xs.append(x.items())
    for key in data:
        final={}
        final[key['Tweet_ID']]=key;
	print final
#	col_fam.batch_insert(final);
        n=key['Tweet_ID'];

#   col_fam.batch_insert(final)
    print "FINALL",final;
    print xs
    print "vocab:",vocab
#    print maptweet
#   print "xs:",xs
    cluster_ind = kmeans(k, xs, len(vocab))
#    print cluster_ind
    clusters = [set() for _ in xrange(k)]
    for i, j in enumerate(cluster_ind):
	if j==None:
		assign=randint(0,k-1);
		cluster_ind[i]=assign;
		j=assign
        clusters[j].add(i)
#   print clusters
    for j, c in enumerate(clusters):
        print("cluster %d:" % j)
        for i in c:
            print("\t%s" % args[i])
#    print centers
     
	while 1:
	    querys=raw_input("Enter Query: ");
            x = defaultdict(float)
    	    for w in re.findall(r"\w+", querys):
                try:
		    x[vocab[w]] += 1
		except:
		       print 
	    minn=dist(x.items(),centers[0]);
	    minid=0;
	    for m in range(1,k):
		    dd=dist(x.items(),centers[m]);
		    if(minn<dd):
			minn=dd;
			minid=m;
	    print "cluster: ",minid
	    for i in clusters[minid]:
	          Tweet_Data(mainn[i])
    


