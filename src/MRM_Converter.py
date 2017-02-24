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

#convert the json message into protobuf object
def convert_MRM_to_pb(infile):
    mrm_infh = open(infile, "r")
    mrm = google.protobuf.json_format.Parse(mrm_infh.readlines()[0],MR_pb2.MutexRun())
    mrm_infh.close()
    return mrm

def make_samp_in():  # make mutex input directory (don't write over if already exists)
    os.makedirs("sample-input",exist_ok=True)

def build_param_outfile(message):
    p_outfh = open("sample-input/parameters.txt","w")
    for key in message.parameters:
        p_outfh.write("{}{}{}{}".format(key, " = ", mrm.parameters[key], '\n'))
    p_outfh.close()

def build_matrix_outfile(message):
    m_outfh = open("sample-input/DataMatrix.txt","w")
    m_outfh.write(str('\t'.join(message.matrix.header)+'\n'))

    for row in message.matrix.rows:
        row = "{}\t{}{}".format(row.label, '\t'.join([str(i) for i in row.values]), '\n')
        m_outfh.write(row)

    m_outfh.close()


def invoke_mutex():
    subprocess.run(["java", "-jar", "mutex.jar", "./sample-input"])

if __name__ == '__main__':
    mrm = convert_MRM_to_pb(mrm_infile)
    make_samp_in()
    build_param_outfile(mrm)
    build_matrix_outfile(mrm)
    invoke_mutex()
