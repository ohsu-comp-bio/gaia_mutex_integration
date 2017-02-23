#!/usr/bin/env python

# The purpose of this output is to stand in for MutexRun messages during
# development until MutexRun messages are built.

# example bash command:
# python MRM_Maker.py -inparam parameters.txt -inmat DataMatrix.txt -outf MutexRunMessage_DEVEL.txt

import argparse
import google.protobuf.json_format
import MR_pb2

# allow use of command line arguments for input and output files
parser = argparse.ArgumentParser()
parser.add_argument("-inparam")      # The parameters file to be converted
parser.add_argument("-inmat")   # The data matrix file to be converted
parser.add_argument("-outf") # The desired name of the outfile (json messages)
args = parser.parse_args()

m_infile = args.inmat
p_infile = args.inparam
outfile = args.outf

p_infh = open(p_infile, "r")

#initialize protobuf objects
dmv = MR_pb2.Vector()
dmm = MR_pb2.Matrix()
mrm = MR_pb2.MutexRun()

#assign the parameters to protobuf
for line in p_infh:
    line = line.strip('\n')
    parts = line.split(' = ')
    mrm.parameters[parts[0]]=parts[1]

p_infh.close()

#assign the matrix to protobuf
m_infh = open(m_infile, "r")

# determine number of rows in matrix file
# len(m_in_fh) does not work
nlines = sum(1 for line in m_infh) - 1
m_infh.seek(0)

#initialize counters and empty list of known size
count = 0
dmv_list = [None] * nlines

# parse matrix file and begin protobuf assignment
# i is a row in matrix
for line in m_infh:
    line = line.strip('\n')
    parts = line.split('\t')
    if count == 0:
        dmm.header.extend(parts)
    if count > 0:
        dmv.label = parts[0]
        intcount = 1
        for v in parts[1:]:
            parts[intcount] = int(v)
            intcount += 1
        dmv.values.extend(parts[1:])
        dmv_list[count-1] = dmv
        dmv = MR_pb2.Vector()
    count += 1
dmm.rows.extend(dmv_list)

m_infh.close()

#now all we have left to assign is mrm.matrix
mrm.matrix.MergeFrom(dmm)
mrm_json = google.protobuf.json_format.MessageToJson(mrm).replace('\n', '')

outfh = open(outfile, "w")
outfh.write(mrm_json)
outfh.close()