from collections import defaultdict
from math import sqrt
import random
import os
import sys
import csv
def densify(x, n):
#    """Convert a sparse vector to a dense one."""
    d = [0] * n
    for i, v in x:
        d[i] = v
    return d


def dist(x, c):
#   """Euclidean distance between sample x and cluster center c.

#   Inputs: x, a sparse vector
#           c, a dense vector
#   """
    sqdist = 0.0
    for i, v in x:
        sqdist += (v - c[i]) *(v-c[i])
    return sqrt(sqdist)
#  print sqdist
#   return sqdist


def mean(xs, l):
#   Mean (as a dense vector) of a set of sparse vectors of length l
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


def kmeans(k, xs, l, n_iter=10):
# centers = [densify(xs[i], l) for i in random.sample(xrange(len(xs)), k)]
    centers=[];
    for i in random.sample(xrange(len(xs)), k):
#	    print i;
	    centers.append(densify(xs[i],l));
#	    print "dist: ",dist(xs[i],centers[len(centers)-1]),"i: " ,i
#  print centers
    cluster = [None] * len(xs)

    for _ in xrange(n_iter):
        for i, x in enumerate(xs):
		minn=dist(xs[i],centers[0]);
		mx=0;
#       cluster[i] = min(xrange(k), key=lambda j: dist(xs[i], centers[j]))
		for j in range(1,k):
			dd=dist(xs[i],centers[j]);
			if minn>=dd:
				minn=dd;
				mx=j;
		cluster[i]=mx;
#		print "set"
#		print "i " ,i,"cluster : " ,mx;
#	if(minn==0):
#		print "minn :",minn,"i:",i;
        for j, c in enumerate(centers):
            members = (x for i, x in enumerate(xs) if cluster[i] == j)
            centers[j] = mean(members, l)

    return cluster

worddict={};
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
#    args=sys.argv[2:];
    filename = sys.argv[2];
    file_path=os.path.abspath(filename)
    reader = csv.reader( open(file_path), delimiter="|")
    header = reader.next()
    i=0;	
    for row in reader:
        if len(row)<2:
		continue;
#	print row[0]
        row[0]=i;
	i=i+1;
    	args.append(row[0])
        x = defaultdict(float)
        for w in re.findall(r"\w+", row[2]):
                plen=len(vocab);
		vocab.setdefault(w, len(vocab))
		nlen=len(vocab)
		if(plen<nlen):
			worddict[plen]=w;
                x[vocab[w]] += 1
#	print "x==",x
#	print "vocab==",vocab
#	print "word==", worddict
        xs.append(x.items())
#   print xs
#   print vocab
    print "calling clustering"
    cluster_ind = kmeans(k, xs, len(vocab))
#    print cluster_ind
    clusters = [set() for _ in xrange(k)]
    for i, j in enumerate(cluster_ind):
        clusters[j].add(i)

    for j, c in enumerate(clusters):
        print("cluster %d:" % j)
        for i in c:
            print("\t%s" % args[i])
