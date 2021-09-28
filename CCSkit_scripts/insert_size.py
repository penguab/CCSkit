#!/usr/bin/env python
import subprocess,re,sys,warnings
from math import sqrt

def insert_size(bam,chr1):
	def stddev(lst):
		mean = float(sum(lst)) / len(lst)
		return mean, sqrt(sum((x - mean)**2 for x in lst) / (len(lst)-1))
	if chr1=="chrM" or chr1=="M":
		start = '1'
		end = '10000'
	else:
		start = '20000000'
		end = '21000000'
	para1=chr1+':'+start+'-'+end
	size=[]
	number=0
	length='0'
	out = subprocess.Popen(['samtools','view',bam,para1],stdout=subprocess.PIPE)
	while True:
		line = out.stdout.read()
		if not line:break
		for array in line.decode('utf-8').split('\n'):
			if not array: continue
			cont=array.split('\t')
			if int(cont[1])%2048>=1024 or int(cont[1])>=2048 or int(cont[1])%512>=256:continue
			number+=1
			if int(cont[4])<60 : continue
			size.append(len(cont[9]))
			if int(length)< len(cont[9]):
				length=len(cont[9])
	coverage=sum(size)/(float(end)-float(start)+1)
	fold=int(round(float(coverage)/10))
	if fold<3:
		warnings.warn('Warnings: Coverage was estimated lower than 30. May cause more false positives!\n')
	if fold<2:
		sys.exit('\nCoverage was estimated lower than 20. Exist!\n')
	mean,sd=stddev(size)
	min_size=max(int(mean-200),int(mean-int(sd)))
	max_size=min(int(mean+300),int(mean+int(sd)))
	return min_size,max_size,length,fold

if __name__=="__main__":
	bam=sys.argv[1]
	min_size,max_size,length,fold=insert_size(bam,"chrM")
	print(fold)

