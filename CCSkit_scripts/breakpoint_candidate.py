#!/usr/bin/env python
import subprocess,sys,os

def breakpoint_candidate(chromosome,fold,min_insert_size,bam):
	root_path=os.getcwd()
	os.chdir(chromosome+"_dir")
	path=os.getcwd()
	from CCSkit_scripts.sv_cigar_sort import sv_cigar_sort
	sv_cigar_sort(chromosome+"_sv")
	from CCSkit_scripts.mutation_sort import mutation_sort
	mutation_sort(chromosome+"_mutation")
	split=chromosome+"_breakpoint"
	from CCSkit_scripts.split_deletion import split_deletion
	split_deletion(split)
	from CCSkit_scripts.sv_sort import sv_sort
	sv_sort(split+".deletion")
	sv_sort(split+".duplication")
	from CCSkit_scripts.split_inversion import split_inversion
	split_inversion(split)
	sv_sort(split+".inversion")
	from CCSkit_scripts.split_translocation import split_translocation
	split_translocation(split)
	sv_sort(split+".translocation")
	from CCSkit_scripts.breakpoint_sort import breakpoint_sort
	breakpoint_sort(split)
	from CCSkit_scripts.sv_vcf import sv_vcf
	sv_vcf(chromosome)
	from CCSkit_scripts.high_coverage import high_coverage
	high_coverage(bam,chromosome,fold)
	os.chdir(root_path)

if __name__ == "__main__":
	chromosome,fold,min_insert_size=sys.argv[1:]
	breakpoint_candidate(chromosome,fold,min_insert_size)

