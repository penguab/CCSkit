#!/usr/bin/env python
import sys,re

def split_inversion(split):
	out_file=open(split+".inversion","w")
	total=[]
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
			for i in range(len(sa)):
				right=sa[i].split(",")
				if left[0]!=right[0] or int(left[5])<60 or int(right[5])<60 or left[3]==right[3]:
					continue
				if left[-1]=='left':
					if right[-1]=='left':
						site1=min(int(left[2]),int(right[2]))
						site2=max(int(left[2]),int(right[2]))
						total.append([left[0],str(site1),str(site2),'INV',str(site2-site1),hp,line[11],sa[i]])
					elif right[-1]=='middle' and abs(int(right[1])-int(left[2]))<=100 and int(right[2])>int(left[2]):
						total.append([left[0],right[1],right[2],'INV',str(int(right[2])-int(right[1])),hp,line[11],sa[i]])
				elif  left[-1]=='right':
					if right[-1]=='right':
						site1=min(int(left[1]),int(right[1]))
						site2=max(int(left[1]),int(right[1]))
						total.append([left[0],str(site1),str(site2),'INV',str(site2-site1),hp,line[11],sa[i]])
					elif right[-1]=='middle' and abs(int(right[2])-int(left[1]))<=100 and int(right[1])<int(left[1]):
						total.append([left[0],right[1],right[2],'INV',str(int(right[2])-int(right[1])),hp,line[11],sa[i]])
				elif left[-1]=='middle':
					if right[-1]=='left' and abs(int(right[2])-int(left[1]))<=100 and int(left[2])>int(right[2]):
						total.append([left[0],left[1],left[2],'INV',str(int(left[2])-int(left[1])),hp,line[11],sa[i]])
					if right[-1]=='right' and abs(int(right[1])-int(left[2]))<=100 and int(right[1])>int(left[1]):
						total.append([left[0],left[1],left[2],'INV',str(int(left[2])-int(left[1])),hp,line[11],sa[i]])
	total_sorted=sorted(total,key=lambda x: (x[5],x[0], int(x[1]),int(x[2])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
	
	
if __name__=='__main__':
	split_inversion(sys.argv[1])
	
