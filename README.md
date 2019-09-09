# CCSkit (A tool kit to analyze genomic mutations from CCS long reads)

Author: Peng Xu

Email: pxu@uabmc.edu

Draft date: Sep. 8, 2019

## Description

CCSkit was developed to comprehensively characterize genomic mutations (SNPs, Indels, Structural variations) from CCS long reads.

## System requirements and dependency

The program was tested on a x86_64 Linux system with 12 cores, each with a 4GB physical memory. The work can be usually finished within an hour for a 60x CCS long read sample.

Dependency: Python3, samtools should be installed in current path.


## Installation

```
git clone git@github.com:penguab/CCSkit.git
```
Then, please also add this directory to your PATH:
```
export PATH=$PWD/CCSkit/:$PATH
```

## Usage

CCSkit needs two files as inputs. The first is a bam file from CCS long read alignment. The second is the genome reference (FASTA format).
```
python CCSkit.py -b <bam file> -g <genome.fa>
```


## News

9/8/2019: First version released.

