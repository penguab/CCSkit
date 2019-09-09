#!/usr/bin/env python
import subprocess,re,sys,warnings

def header(bam):
	command=subprocess.Popen(['samtools','view','-H',bam], stdout=subprocess.PIPE)
	chromosomes=[]
	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l: break
		line=l.split('\t')
		if line[0]!="@SQ":
			continue
		length=line[2].split(':')[1]
		if int(length)<=40000000:
			continue
		name=line[1].split(':')[1]
		chromosomes.append(name)
	chro_filter=[]
	for i in range(len(chromosomes)):
		test=subprocess.Popen(['samtools','view',bam,chromosomes[i]], stdout=subprocess.PIPE)
		while True:
			l= test.stdout.readline().decode('utf-8').rstrip()
			if not l: break
			chro_filter.append(chromosomes[i])
			break
	return chro_filter

if __name__=="__main__":
	bam=sys.argv[1]
	chromosomes=header(bam)
	print('\t'.join(chromosomes))

