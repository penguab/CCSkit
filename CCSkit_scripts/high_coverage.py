#!/usr/bin/env python
import subprocess,re,sys,warnings,os
from math import sqrt

def high_coverage(bam,chromo,fold):
	out_file=open("HighCov_region.bed",'w')
	devnull=open(os.devnull, 'w')
	chromosome,start,end,total='','','',''
	command= subprocess.Popen(['samtools','mpileup',bam,'-r',chromo], stdout=subprocess.PIPE,stderr=devnull)
	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l: break
		line=l.split('\t')
		if int(line[3])<=fold:
			continue
		if not chromosome:
			chromosome=line[0]
			start=line[1]
			end=line[1]
			total='1'
			continue
		if chromosome==line[0] and int(line[1])-int(end)<=10:
			end=line[1]
			total=str(int(total)+1)
			continue
		elif int(total)>=10:
			out_file.write('\t'.join([chromosome,start,end,str(int(end)-int(start)+1)])+"\n")
		chromosome=line[0]
		start=line[1]
		end=line[1]
		total='1'
	if int(total)>=10:
		out_file.write('\t'.join([chromosome,start,end,str(int(end)-int(start)+1)])+"\n")
	command.communicate()
	
if __name__=="__main__":
	high_coverage(sys.argv[1],sys.argv[2],sys.argv[3])

