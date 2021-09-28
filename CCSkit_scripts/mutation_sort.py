#!/usr/bin/env python	
import sys,re
	
def mutation_sort(breakpoint):
	out=open('Candidate_mutation.bed','w')	
	total=[]
	with open(breakpoint) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			if line[-1][0:2]=='hp':
				hp=line[-1]
			else:
				hp='hp0'
			m=re.search(r'^\d|X|Y|M',line[0])
			if not m:
				continue
			total.append([line[0],line[1],line[2],"Mutation",line[3],hp])
	total_sort=sorted(total,key=lambda x: (x[5],x[3],x[0], int(x[1]),int(x[4])))
	pre=[]
	for x in range(len(total_sort)):
		if x==0:
			pre=total_sort[x]+['1']
			continue
		if total_sort[x][5]==pre[5] and  total_sort[x][0]==pre[0] and int(total_sort[x][1])-int(pre[1])<=50 and total_sort[x][3]==pre[3] and int(total_sort[x][4])/int(pre[4])>=0.8 and int(total_sort[x][4])/int(pre[4])<=1.2:
			pre[6]=str(int(pre[6])+1)
		else:
			if int(pre[6])>=3:
				out.write(("\t".join(str(n) for n in pre))+"\n")
			pre=total_sort[x]+['1']
	if int(pre[6])>=3:
		out.write(("\t".join(str(n) for n in pre))+"\n")

if __name__=="__main__":
	mutation_sort(sys.argv[1])

