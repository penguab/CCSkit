#!/usr/bin/env python
	
import subprocess,sys,re,os
	
def extract_breakpoints (chromosome,bam):
	def sa_code(sa):
		if sa=='NA':
			return sa
		whole_p=re.compile(r'^(\d+)([MDISH])(\d+[MDI])*(\d+)([MDISH])$')
		match_p=re.compile(r'^(\d+)([MDISH])')
		line=sa.split(',')
		chromosome=line[0].split(':')[-1]
		cigar=line[3]
		pos= line[1]
		while True:
			m=match_p.search(cigar)
			if not m: break
			if m.group(2)=="M" or m.group(2)=="D":
				pos=str(int(pos)+int(m.group(1)))
			cigar=cigar[len(m.group(0)):]
		direction=''
		whole=whole_p.search(line[3])
		if not whole:
			direction='NA'
		elif (whole.group(2)=='S' or whole.group(2)=='H') and int(whole.group(1))>=500 and (whole.group(5)=='S' or whole.group(5)=='H') and int(whole.group(4))>=500:
			direction='middle'
		elif (whole.group(2)=='S' or whole.group(2)=='H') and int(whole.group(1))>=500:
			direction='right'
		elif (whole.group(5)=='S' or whole.group(5)=='H') and int(whole.group(4))>=500:
			 direction='left'
		return ','.join([chromosome,line[1],pos,line[2],line[3],line[4],line[5],direction])

	os.mkdir(chromosome+"_dir")
	os.chdir(chromosome+"_dir")
	out_snp=open(chromosome+"_snp","w")
	out_indel=open(chromosome+"_indel","w")
	out_sv=open(chromosome+"_sv","w")
	out_break=open(chromosome+"_breakpoint","w")
	out_mutation=open(chromosome+"_mutation","w")

	XA_p=re.compile(r'XA:Z:([^,]+),[-+]([^,]+),([^,]+),[^\t]+')
	SA_p=re.compile(r'SA:Z:([^,]+),([^,]+),[+-],([^,]+),[^\t]+')
	whole_p=re.compile(r'^(\d+)([X=DISH])(\d+[X=DI])*(\d+)([X=DISH])$')
	match_p=re.compile(r'^(\d+)([X=DISH])')

	mark_test=0
	command= subprocess.Popen(['samtools','view',bam,chromosome], stdout=subprocess.PIPE)
	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l: break
		line=l.split('\t')
		if int(line[1])%2048>=1024 : continue
		SA=SA_p.search(l)
		if SA:
			sa=SA.group(0)
			sa=re.sub('chr','',sa)
		else:
			sa='NA;'
		XA=XA_p.search(l)
		if XA:
			xa=XA.group(0)
		else:
			xa='NA'
		line[2]=re.sub('chr','',line[2])
		if mark_test==0:
			test=re.search(r'=',line[5])
			if not test:
				exit('Please use "X=" for CIGAR system')
			mark_test=1
		cigar=line[5]
		seq=line[9]
		total_len=len(line[9])
		first_m=re.search(r'^(\d+)[SH]',line[5])
		if first_m:
			first_site=int(first_m.group(1))
		else:
			first_site=0
		last_m=re.search(r'(\d+)[SH]$',line[5])
		if last_m:
			last_site=total_len-int(last_m.group(1))
		else:
			last_site=total_len
		site='0'
		pos= line[3]
		mark=0
		mutation_start,mutation_end,mutation_num,mutation_cigar,mutation_pre_site,mutation_pre_pos='','',0,[],site,pos
		first_clip,last_clip,match,mismatch,sv='','',0,0,0
		while True:
			m=match_p.search(cigar)
			if not m: break
			if m.group(2)=="S" or  m.group(2)=="H":
				site=str(int(site)+int(m.group(1)))
				first_clip_m=re.search(r'^\d+[SH]\d+',cigar)
				if first_clip_m:
					first_clip=m.group(1)+m.group(2)
				else:
					last_clip=m.group(1)+m.group(2)
			if m.group(2)=="X":
				if int(site)>=first_site+1500 and int(site)<=last_site-1500:
					out_snp.write(line[2]+'\t'+pos+'\t'+str(int(pos)+int(m.group(1)))+'\t'+m.group(1)+'X\t'+seq[int(site):(int(site)+int(m.group(1)))]+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\n')
				pos=str(int(pos)+int(m.group(1)))
				site=str(int(site)+int(m.group(1)))
				match=match+int(m.group(1))
				mismatch=mismatch+int(m.group(1))
			if m.group(2)=="=" :
				pos=str(int(pos)+int(m.group(1)))
				site=str(int(site)+int(m.group(1)))
				if int(line[1])<2048 and int(line[1])%512 <256 and int(site)>=first_site+1500 and int(site)<=last_site-1500: 
					if int(site)-int(mutation_pre_site)<=10 and int(pos)-int(mutation_pre_pos)<=10:
						if mutation_start=='':
							mutation_start=pos
						mutation_end=pos
						mutation_num=mutation_num+1
						mutation_cigar.append(m.group(1)+m.group(2))
					else:
						if mutation_num>=5:
							out_mutation.write(line[2]+'\t'+mutation_start+'\t'+mutation_end+'\t'+str(mutation_num)+'\t'+'_'.join(mutation_cigar)+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\n')
						mutation_start,mutation_end,mutation_num,mutation_cigar='','',0,[]
					mutation_pre_site=site
					mutation_pre_pos=pos
				match=match+int(m.group(1))
			if m.group(2)=="D":
				if int(m.group(1))<50 and int(site)>=first_site+1500 and int(site)<=last_site-1500:
					out_indel.write(line[2]+'\t'+pos+'\t'+str(int(pos)+int(m.group(1)))+'\t'+m.group(1)+'D\t'+'-'+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\n')
				if int(m.group(1))>=50 and int(site)>=first_site+1500 and int(site)<=last_site-1500:
					out_sv.write(line[2]+'\t'+pos+'\t'+str(int(pos)+int(m.group(1)))+'\t'+m.group(1)+'D\t'+'-'+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\n')
				pos=str(int(pos)+int(m.group(1)))
				sv=sv-int(m.group(1))
			if m.group(2)=="I":
				if int(m.group(1))<50 and int(site)>=first_site+1500 and int(site)<=last_site-1500:
					out_indel.write(line[2]+'\t'+pos+'\t'+str(int(pos)+1)+'\t'+m.group(1)+'I\t'+seq[int(site):(int(site)+int(m.group(1)))]+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\n')
				if int(m.group(1))>=50 and int(site)>=first_site+1500 and int(site)<=last_site-1500:
					out_sv.write(line[2]+'\t'+pos+'\t'+str(int(pos)+1)+'\t'+m.group(1)+'I\t'+seq[int(site):(int(site)+int(m.group(1)))]+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\n')
				site=str(int(site)+int(m.group(1)))
				sv=sv+int(m.group(1))
			cigar=cigar[len(m.group(0)):]
		if int(line[1])<2048 and int(line[1])%512 <256 and mutation_num>=5 and int(site)>=first_site+1500 and int(site)<=last_site-1500:
			out_mutation.write(line[2]+'\t'+mutation_start+'\t'+mutation_end+'\t'+str(mutation_num)+'\t'+'_'.join(mutation_cigar)+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\n')
		if int(line[1])%32 <16:
			direction='+'
		else:
			direction='-'
		if sv>0:
			new_cigar=','.join(['SA:Z:'+line[2],line[3],direction,first_clip+str(match)+'M'+str(sv)+'I'+last_clip,line[4],str(mismatch)])
		elif sv<0:
			new_cigar=','.join(['SA:Z:'+line[2],line[3],direction,first_clip+str(match)+'M'+str(abs(sv))+'D'+last_clip,line[4],str(mismatch)])
		else:
			new_cigar=','.join(['SA:Z:'+line[2],line[3],direction,first_clip+str(match)+'M'+last_clip,line[4],str(mismatch)])
		total_sa=sa.split(';')
		new_total_sa=[]
		for i in range(len(total_sa)-1):
			new_total_sa.append(sa_code(total_sa[i]))
		whole=whole_p.search(line[5])
		if not whole: continue
		if (whole.group(2)=='S' or whole.group(2)=='H') and int(whole.group(1))>=500:
			out_break.write(line[2]+'\t'+str(int(line[3]))+'\t'+str(int(line[3])+1)+'\t'+whole.group(1)+'S\t'+'right'+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\t'+sa_code(new_cigar)+'\t'+';'.join(new_total_sa)+'\t'+xa+'\t'+line[5]+'\n')
		if (whole.group(5)=='S' or whole.group(5)=='H') and int(whole.group(4))>=500:
			out_break.write(line[2]+'\t'+str(int(pos))+'\t'+str(int(pos)+1)+'\t'+whole.group(4)+'S\t'+'left'+'\t'+'\t'.join(line[0:5])+'\t'+str(total_len)+'\t'+sa_code(new_cigar)+'\t'+';'.join(new_total_sa)+'\t'+xa+'\t'+line[5]+'\n')
	
