#!/usr/bin/env python

# This script converts MutexRun json messages into these files:
#     parameters.txt  DataMatrix.txt
# And subsequently invokes mutex using those files as input
# It must be run from the file containing mutex.jar, MutexRun_pb2.py,
#     resources directory containing PC2v8.sif, MutexRunMsg.txt

# example bash command:
# python MutexRun_message_converter.py -mrm MutexRunMsg_DEVEL.txt
# mrm is mutex run message

import argparse
import MutexRun_pb2
import google.protobuf.json_format
import os
import subprocess

# allow use of command line arguments for input and output files
parser = argparse.ArgumentParser()
parser.add_argument("-mrm")
args = parser.parse_args()
mrm_in_file = args.mrm
mrm_in_fh = open(mrm_in_file, "r")

# separate parameters and data matrix messages
json_msg_list = mrm_in_fh.readlines()
param_msg = json_msg_list[0]
mat_msg = json_msg_list[1]
mrm_in_fh.close()

# make mutex input directory (don't write over if already exists)
os.makedirs("sample-input",exist_ok=True)

# convert parameters json messages to mutex input format
pm = google.protobuf.json_format.Parse(param_msg, MutexRun_pb2.Params())
params = []

for i in range(0,len(pm.paramnames)):
    params.append("{} {} {}{}".format(pm.paramnames[i], '=', pm.specifications[i], '\n'))

params[-1] = params[-1].strip('\n')

# write parameters out to file
param_out_fh = open("sample-input/parameters.txt", "w")

for line in params:
    param_out_fh.write(line)

param_out_fh.close()

# convert data matrix json messages to mutex input format
dmm = google.protobuf.json_format.Parse(mat_msg, MutexRun_pb2.Matrix())

headerline = '\t'.join(dmm.header)+'\n'
rowlist = []

for i in range(0,len(dmm.rows)):
    vals = '\t'.join(map(str,dmm.rows[i].values))
    row = "{}\t{}".format(dmm.rows[i].label, vals)
    rowlist.append(row + '\n')
    if i == len(dmm.rows)-1:
        rowlist[i] = rowlist[i].strip('\n')

# write data matrix out to file
matrix_out_fh = open("sample-input/DataMatrix.txt", "w")
matrix_out_fh.write(headerline)

for item in rowlist:
    matrix_out_fh.write(item)

matrix_out_fh.close()

# invoke mutex
subprocess.run(["java", "-jar", "mutex.jar", "./sample-input"])
# this would run the command:
#     $ java -jar mutex.jar sample-input