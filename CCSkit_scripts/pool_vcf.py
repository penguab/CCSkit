#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def pool_vcf(Chromosomes):
	path=os.getcwd()
	SV_out=open("CCSkit_SV.vcf","w")
	Mutation_out=open("CCSkit_Mutation.bed","w")
	HighCov_out=open("CCSkit_HighCov.bed","w")
	SV,Mutation,HighCov=[],[],[]
	for chromosome in Chromosomes:
		os.chdir(chromosome+"_dir")
		f1=open("Candidate_mutation.bed",'r')
		while True:
			l=f1.readline().rstrip()
			if not l: break
			Mutation.append(l.split("\t"))
		f1.close()
		f2=open("Candidate_SV.vcf",'r')
		while True:
			l=f2.readline().rstrip()
			if not l: break
			SV.append(l.split("\t"))
		f2.close()
		f3=open("HighCov_region.bed",'r')
		while True:
			l=f3.readline().rstrip()
			if not l: break
			HighCov.append(l.split("\t"))
		f3.close()
		os.chdir(path)
	SV_sort=sorted(SV,key=lambda x: (x[0], int(x[1])))
	SV_out.write("##fileformat=VCFv4.2\n")
	SV_out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n")
	for y in range(len(SV_sort)):
		SV_out.write(("\t".join(str(n) for n in SV_sort[y]))+"\n")
	Mutation_sort=sorted(Mutation,key=lambda x: (x[0], int(x[1])))
	for x in range(len(Mutation_sort)):
		Mutation_out.write(("\t".join(str(n) for n in Mutation_sort[x]))+"\n")
	HighCov_sort=sorted(HighCov,key=lambda x: (x[0], int(x[1])))
	for x in range(len(HighCov_sort)):
		HighCov_out.write(("\t".join(str(n) for n in HighCov_sort[x]))+"\n")

if __name__=="__main__":
	pool_vcf(sys.argv[1])
