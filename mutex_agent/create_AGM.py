#!/usr/bin/env python

from __future__ import print_function

import argparse
import google.protobuf.json_format

from mutex_agent import AlterationGroupSchema_pb2


def convert_rg_to_json(infile):
    in_fh = open(infile, "r")
    count = 0
    altgroups = []
    for line in in_fh:
        line = line.strip('\n')
        parts = line.split('\t')
        # allow for possibility that q-val column is not present in input file
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
    return altgroups


def write_out_json(outfile, altg):
    out_fh = open(outfile, "w")
    # write to file with 1 json message per line
    for i in altg:
        json_string = google.protobuf.json_format.MessageToJson(
            i).replace('\n', '') + '\n'
        out_fh.write("%s" % json_string)
    out_fh.close()


if __name__ == '__main__':
    # allow use of command line arguments for input and output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-ranked-groups", "-r",
                        help="The ranked groups file to be converted")
    parser.add_argument("--outfile", "-o",
                        help="The desired name of the outfile (json messages)")
    args = parser.parse_args()

    in_file = args.ranked_groups
    out_file = args.outfile

    rg_json = convert_rg_to_json(in_file)
    write_out_json(out_file, rg_json)
