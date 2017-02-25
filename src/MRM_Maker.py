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

#initialize protobuf objects
dmv = MR_pb2.Vector()
dmm = MR_pb2.Matrix()
mrm = MR_pb2.MutexRun()

def assign_param_to_pb(pinfl, mrmessage):
    p_infh = open(pinfl, "r")
    for line in p_infh:
        line = line.strip('\n')
        parts = line.split(' = ')
        mrmessage.parameters[parts[0]]=parts[1]
    p_infh.close()
    return mrmessage

def assign_matrix_to_pb(minfl,dmvector,dmmatrix):
    m_infh = open(minfl, "r")

    # determine number of rows in matrix file
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
            dmmatrix.header.extend(parts)
        if count > 0:
            dmvector.label = parts[0]
            intcount = 1
            for v in parts[1:]:
                parts[intcount] = int(v)
                intcount += 1
            dmvector.values.extend(parts[1:])
            dmv_list[count-1] = dmvector
            dmvector = MR_pb2.Vector()
        count += 1
    dmmatrix.rows.extend(dmv_list)
    m_infh.close()
    return dmmatrix

def assign_all_to_mrm(outfl,mrmessage,dmmatrix):
    mrmessage.matrix.MergeFrom(dmmatrix)
    mrm_json = google.protobuf.json_format.MessageToJson(mrmessage).replace('\n', '')
    outfh = open(outfl, "w")
    outfh.write(mrm_json)
    outfh.close()

if __name__ == '__main__':
    mrm = assign_param_to_pb(p_infile,mrm)
    dmm = assign_matrix_to_pb(m_infile,dmv,dmm)
    assign_all_to_mrm(outfile,mrm,dmm)