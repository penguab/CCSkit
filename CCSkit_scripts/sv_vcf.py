#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def sv_vcf(chromosome):
	SV_out=open("Candidate_SV.vcf","w")
	SV=[]
	f1=open(chromosome+"_sv.sort",'r')
	while True:
		l=f1.readline().rstrip()
		if not l: break
		line=l.split("\t")
		SV.append(line)
	f1.close()
	f2=open(chromosome+"_breakpoint.deletion.sort",'r')
	while True:
		l=f2.readline().rstrip()
		if not l: break
		line=l.split("\t")
		SV.append(line)
	f2.close()
	f3=open(chromosome+"_breakpoint.duplication.sort",'r')
	while True:
		l=f3.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f3.close()
	f5=open(chromosome+"_breakpoint.translocation.sort",'r')
	while True:
		l=f5.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f5.close()
	f6=open(chromosome+"_breakpoint.inversion.sort",'r')
	while True:
		l=f6.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f6.close()
	f7=open(chromosome+"_breakpoint.sort",'r')
	while True:
		l=f7.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f7.close()
	SV_sort=sorted(SV,key=lambda x: (x[0], int(x[1])))
	for y in range(len(SV_sort)):
		if SV_sort[y][3]=="DEL":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=DEL;SVLEN="+SV_sort[y][4]+";Depth="+SV_sort[y][6]+"\tHP:GT"+"\t"+SV_sort[y][5]+"\n")
		elif SV_sort[y][3]=="INS" or SV_sort[y][3]=="DUP":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=INS;SVLEN="+SV_sort[y][4]+";Depth="+SV_sort[y][6]+"\tHP:GT"+"\t"+SV_sort[y][5]+"\n")
		elif SV_sort[y][3]=="INV":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=INV;SVLEN="+SV_sort[y][4]+";Depth="+SV_sort[y][6]+"\tHP:GT"+"\t"+SV_sort[y][5]+"\n")
		elif SV_sort[y][3]=="TRANS":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t"+SV_sort[y][2]+"\t.\t.\t"+"SVTYPE=TRANS;SVLEN=-"+";Depth="+SV_sort[y][6]+"\tHP:GT"+"\t"+SV_sort[y][5]+"\n")

if __name__=="__main__":
	sv_vcf(sys.argv[1])
