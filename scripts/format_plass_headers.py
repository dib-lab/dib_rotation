#! /usr/bin/env python
import screed
import sys
import os

input = sys.argv[1]
output = sys.argv[2]

with open(str(output), 'wt') as fp:
    for record in screed.open(str(input)):
        genome_name = str(input)
        genome_name = genome_name.split('/')[1]
        genome_name = genome_name.split('.')[0]
        seqname = record.name.split(' ')[0]
        newname = genome_name + '_' + seqname
        fp.write('>{}\n{}\n'.format(newname, record.sequence))
