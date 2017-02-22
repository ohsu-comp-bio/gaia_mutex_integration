#!/usr/bin/env python

# This script convertS MutexRun json messages into these files:
#   parameters.txt  DataMatrix.txt
# It will soon also invoke Mutex

# example bash command:
# python MutexRun_message_converter.py -mrm MutexRunMsg_smalldevel.txt
# mrm for mutex run message

import argparse
import MutexRun_pb2
import google.protobuf.json_format
import subprocess

# allow use of command line arguments for input and output files
parser = argparse.ArgumentParser()
parser.add_argument("-mrm")
args = parser.parse_args()

mrm_in_file = args.mrm
mrm_in_fh = open(mrm_in_file, "r")

json_msg_list = mrm_in_fh.readlines()
mrm_in_fh.close()

param_msg = json_msg_list[0]
mat_msg = json_msg_list[1]

pm = google.protobuf.json_format.Parse(param_msg, MutexRun_pb2.Params())

params = []

for i in range(0,len(pm.paramnames)):
    params.append("{} {} {}{}".format(pm.paramnames[i], '=', pm.specifications[i], '\n'))

params[-1] = params[-1].strip('\n')
param_out_fh = open("parameters.txt", "w")

for line in params:
    param_out_fh.write(line)

param_out_fh.close()

#matrix conversion below

dmm = google.protobuf.json_format.Parse(mat_msg, MutexRun_pb2.Matrix())

headerline = '\t'.join(dmm.header)+'\n'
rowlist = []

for i in range(0,len(dmm.rows)):
    vals = '\t'.join(map(str,dmm.rows[i].values))
    row = "{}\t{}".format(dmm.rows[i].label, vals)
    rowlist.append(row + '\n')
    if i == len(dmm.rows)-1:
        rowlist[i] = rowlist[i].strip('\n')

matrix_out_fh = open("DataMatrix.txt", "w")
matrix_out_fh.write(headerline)

for item in rowlist:
    matrix_out_fh.write(item)

matrix_out_fh.close()

#have to move a jarfile into working dir first
#subprocess.run(["java", "-jar", "mutex.jar", "./"])