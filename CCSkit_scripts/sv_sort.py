#!/usr/bin/env python	
import sys,re
	
def sv_sort(breakpoint):
	out=open(breakpoint+'.sort','w')	
	pre=[]
	with open(breakpoint) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			if line[3]!='TRANS' and  int(line[4])<50:
				continue
			if len(pre)==0:
				pre=line[0:6]+['1']
				continue
			if line[3]=='TRANS' and  line[5]==pre[5] and  int(line[1])-int(pre[1])<=50 and line[3]==pre[3]:
				pre[6]=str(int(pre[6])+1)
			elif line[5]==pre[5] and  line[0]==pre[0] and int(line[1])-int(pre[1])<=50 and line[3]==pre[3] and int(line[4])/int(pre[4])>=0.8 and int(line[4])/int(pre[4])<=1.2:
				pre[6]=str(int(pre[6])+1)
			else:
				if int(pre[6])>=3:
					out.write(("\t".join(str(n) for n in pre))+"\n")
				pre=line[0:6]+['1']
	if int(pre[6])>=3:
		out.write(("\t".join(str(n) for n in pre))+"\n")

if __name__=="__main__":
	sv_sort(sys.argv[1])

