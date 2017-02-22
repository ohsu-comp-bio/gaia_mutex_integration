#!/usr/bin/env python

# This script converts ranked-groups.txt (output by Mutex) into json messages

# example bash command:
# python ranked_groups_converter.py -rg ranked-groups.txt -outfile rg_json_messages.txt

import argparse
import google.protobuf.json_format
import AlterationGroupSchema_pb2    # Can I make this a parameter using argparse?

# allow use of command line arguments for input and output files
parser = argparse.ArgumentParser()
parser.add_argument("-rg")      # The ranked groups file to be converted
parser.add_argument("-outfile") # The desired name of the outfile (json messages)
args = parser.parse_args()

# parser.add_argument("-schema")  # The protoc-compiled schema (output of running protoc on .proto file)

in_file = args.rg
in_fh = open(in_file, "r")

count = 0
altgroups = []

# convert input file lines into json objects
# prepare for possibility that q-val column is not present in input file
for line in in_fh:
    line = line.strip('\n')
    parts = line.split('\t')
    if count == 0:
        if parts[1] == "q-val":
            qexists = True
        else:
            qexists = False
    else:
        ag = AlterationGroupSchema_pb2.AlterationGroup()
        ag.score = float(parts[0])
        if qexists:
            ag.q = float(parts[1])
            ag.members.extend(parts[2:])
        else:
            ag.members.extend(parts[1:])
        altgroups.append(ag)
    count += 1

in_fh.close()
out_file = args.outfile
out_fh = open(out_file, "w")

# write to file with 1 json message per line
for i in altgroups:
    json_string = google.protobuf.json_format.MessageToJson(i).replace('\n','') + '\n'
    out_fh.write("%s" % json_string)

out_fh.close()