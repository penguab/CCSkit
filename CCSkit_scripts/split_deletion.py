#!/usr/bin/env python
import sys,re

def split_deletion(split):
	deletion_file=open(split+".deletion","w")
	duplication_file=open(split+".duplication","w")
	deletion,duplication=[],[]
	with open(split) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if line[-1][0:2]=='hp':
				hp=line[-1]
			else:
				hp='hp0'
			if line[12]=='NA':
				continue
			sa=line[12].split(';')
			left=line[11].split(",")
			if len(sa)==1:
				right=sa[0].split(",")
				if left[0]!=right[0] or int(left[5])<60 or int(right[5])<60 or left[3]!=right[3] or left[-1]=='middle' or right[-1]=='middle':
					continue
				if left[-1]=='right' and right[-1]=='left':
					tmp=left
					left=right
					right=tmp
				if int(left[2])<=int(right[1]):
					deletion.append([left[0],left[2],right[1],'DEL',str(int(right[1])-int(left[2])),hp,line[11],sa[0]])
				else:
					duplication.append([left[0],right[1],left[2],'DUP',str(int(left[2])-int(right[1])),hp,line[11],sa[0]])
	deletion_sorted=sorted(deletion,key=lambda x: (x[5],x[0], int(x[1]),int(x[2])))
	for x in range(len(deletion_sorted)):
		deletion_file.write(('\t'.join(str(n) for n in deletion_sorted[x]))+'\n')
	duplication_sorted=sorted(duplication,key=lambda x: (x[5],x[0], int(x[1]),int(x[2])))
	for x in range(len(duplication_sorted)):
		duplication_file.write(('\t'.join(str(n) for n in duplication_sorted[x]))+'\n')
	
if __name__=='__main__':
	split_deletion(sys.argv[1])
	
