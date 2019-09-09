#!/usr/bin/env python
import sys,re

def breakpoint_sort(split):
	breakpoint_file=open(split+".sort","w")
	breakpoint=[]
	with open(split) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if line[-1][0:2]=='hp':
				hp=line[-1]
			else:
				hp='hp0'
			if int(line[9])<60:
				continue
			if line[11].split(',')[-1]=='middle':
				continue
			if line[4]=='left':
				left='1'
				right='0'
			elif line[4]=='right':
				left='0'
				right='1'
			breakpoint.append([line[0],line[1],line[2],'INS','-',hp,left,right,'1'])
	breakpoint_sorted=sorted(breakpoint,key=lambda x: (x[5],x[0],int(x[1])))
	pre=[]
	for x in range(len(breakpoint_sorted)):
		if len(pre)==0:
			pre=breakpoint_sorted[x]
			continue
		if breakpoint_sorted[x][5]==pre[5] and breakpoint_sorted[x][0]==pre[0] and int(breakpoint_sorted[x][1])-int(pre[1])<=20 and breakpoint_sorted[x][3]==pre[3]:
			pre[6]=str(int(pre[6])+int(breakpoint_sorted[x][6]))
			pre[7]=str(int(pre[7])+int(breakpoint_sorted[x][7]))
			pre[8]=str(int(pre[8])+int(breakpoint_sorted[x][8]))
		else:
			if int(pre[6])>=3 and int(pre[7])>=3:
				breakpoint_file.write(('\t'.join(str(n) for n in pre[0:6]+[pre[8]]))+'\n')
			pre=breakpoint_sorted[x]
	if int(pre[6])>=3 and int(pre[7])>=3:
		breakpoint_file.write(('\t'.join(str(n) for n in pre[0:6]+[pre[8]]))+'\n')
	
if __name__=='__main__':
	breakpoint_sort(sys.argv[1])
	
