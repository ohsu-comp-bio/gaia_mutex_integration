#!/usr/bin/env python

import argparse
import MR_pb2
import google.protobuf.json_format
import os
import subprocess

# allow use of command line arguments for input and output files
parser = argparse.ArgumentParser()
parser.add_argument("-mrm")
args = parser.parse_args()
mrm_infile = args.mrm

#convert the json message back into protobuf object
mrm_infh = open(mrm_infile, "r")
mrm = google.protobuf.json_format.Parse(mrm_infh.readlines()[0],MR_pb2.MutexRun())
mrm_infh.close()

# make mutex input directory (don't write over if already exists)
os.makedirs("sample-input",exist_ok=True)

#build parameters.txt
#Note that this is not ordered in any way
p_outfh = open("sample-input/parameters.txt","w")
for key in mrm.parameters:
    p_outfh.write("{}{}{}{}".format(key, " = ", mrm.parameters[key], '\n'))
p_outfh.close()

#build DataMatrix.txt
m_outfh = open("sample-input/DataMatrix.txt","w")
m_outfh.write(str('\t'.join(mrm.matrix.header)+'\n'))

for row in mrm.matrix.rows:
    row = "{}\t{}{}".format(row.label, '\t'.join([str(i) for i in row.values]), '\n')
    m_outfh.write(row)

m_outfh.close()

# invoke mutex
subprocess.run(["java", "-jar", "mutex.jar", "./sample-input"])
# this would run the command:
#     $ java -jar mutex.jar ./sample-input