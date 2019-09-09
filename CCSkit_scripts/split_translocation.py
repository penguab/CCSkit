#!/usr/bin/env python
import sys,re

def split_translocation(split):
	translocation_file=open(split+".translocation","w")
	translocation=[]
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
				if left[0]==right[0] or int(left[5])<60 or int(right[5])<60 or left[-1]=='middle' or right[-1]=='middle':
					continue
				m1=re.search(r'^(chr)*[\dXY]',left[0])
				if not m1:
					continue
				m2=re.search(r'^(chr)*[\dXY]',right[0])
				if not m2:
					continue
				translocation.append([left[0],left[2],right[0]+':'+right[2],'TRANS','0',hp,line[11],sa[0],right[0],right[2]])
	translocation_sorted=sorted(translocation,key=lambda x: (x[5],x[0],int(x[1]),x[8],int(x[9])))
	for x in range(len(translocation_sorted)):
		translocation_file.write(('\t'.join(str(n) for n in translocation_sorted[x][0:8]))+'\n')
	
if __name__=='__main__':
	split_translocation(sys.argv[1])
	
