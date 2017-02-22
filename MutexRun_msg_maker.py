#!/usr/bin/env python

# This script generates a file containing json messages.
# Output file is similar to the not-yet-developed MutexRun message.
# The purpose of this output is to stand in for MutexRun messages during
# development until MutexRun messages are built.

# example bash command:
# python MutexRun_message_maker.py -inparam parameters.txt -inmat DataMatrix.txt -outf MutexRunMessage_DEVEL.txt

import argparse
import google.protobuf.json_format
import MutexRun_pb2

# allow use of command line arguments for input and output files
parser = argparse.ArgumentParser()
parser.add_argument("-inparam")      # The parameters file to be converted
parser.add_argument("-inmat")   # The data matrix file to be converted
parser.add_argument("-outf") # The desired name of the outfile (json messages)
args = parser.parse_args()

m_in_file = args.inmat
p_in_file = args.inparam
outfile = args.outf

p_in_fh = open(p_in_file, "r")

pm = MutexRun_pb2.Params()
parlist = []
speclist = []

for line in p_in_fh:
    line = line.strip('\n')
    parts = line.split(' = ')
    parlist.append(parts[0])
    speclist.append(parts[1])

pm.paramname.extend(parlist)
pm.specification.extend(speclist)

p_in_fh.close()
m_in_fh = open(m_in_file, "r")

linecounter = sum(1 for line in m_in_fh) - 1
m_in_fh.seek(0)

dmm = MutexRun_pb2.Matrix()
dmv = MutexRun_pb2.Vector()

count = 0
dmvcount = 0
dmv_list = [None] * linecounter

for i in m_in_fh:
    i = i.strip('\n')
    parts = i.split('\t')
    if count == 0:
        dmm.header.extend(parts)
    if count > 0:
        dmv.label = parts[0]
        intcount = 1
        for v in parts[1:]:
            parts[intcount] = int(v)
            intcount += 1
        dmv.values.extend(parts[1:])
        dmv_list[dmvcount] = dmv
        dmv = MutexRun_pb2.Vector()
        dmvcount += 1
    count += 1

dmm.rows.extend(dmv_list)

out_fh = open(outfile, "w")

p_json_string = google.protobuf.json_format.MessageToJson(pm).replace('\n','')+'\n'
m_json_string = google.protobuf.json_format.MessageToJson(dmm).replace('\n', '')

out_fh.write("{}{}".format(p_json_string, m_json_string))

out_fh.close()
