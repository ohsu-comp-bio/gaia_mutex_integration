#!/usr/bin/env python

# This builds stand-in files for the development of gaia-mutex integration
# The purpose of the mrm output is to stand in for a real MRM
# The purpose of the mat output is to stand in for the data matrix json that
#   gaia would provide in response to a url query included in an MRM

# example bash command
# python gaia_mutex_integration/src/MRM_Maker.py -ip parameters.txt -im DataMatrix.txt -mro MRM_DEVEL.json -mto MatM_DEVEL.json

import argparse
import google.protobuf.json_format
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from mutex_agent import MR_pb2

parser = argparse.ArgumentParser()
parser.add_argument("--inparam", "-ip")     # The parameters file to be converted
parser.add_argument("--inmat", "-im")       # The data matrix file to be converted (for matrix json)
parser.add_argument("-maturl", "-U",        # The url string to request the matrix from gaia (for mrm json)
                    default='rows=label+and+values&header=Special') #a 100% fake placeholder URL
parser.add_argument("--mrmoutf", "-mro")   # The desired name of the mrm json outfile
parser.add_argument("--matoutf", "-mto")   # The desired name of the matrix json outfile
args = parser.parse_args()

p_infile = args.inparam
m_infile = args.inmat
mrm_outfile = args.mrmoutf
mat_outfile = args.matoutf

#initialize protobuf objects
dmv = MR_pb2.Vector()
dmm = MR_pb2.Matrix()
mrm = MR_pb2.MutexRun()

#mrmessage is MR_pb2.MutexRun() aka mrm
def assign_param_to_pb(pinfl, mrmessage):
    p_infh = open(pinfl, "r")
    for line in p_infh:
        line = line.strip('\n')
        parts = line.split(' = ')
        if parts[0] == 'search-on-signaling-network':
            mrm.searchonsignalingnetwork = bool(parts[1])
        elif parts[0] == 'network-file':
            mrm.networkfile = str(parts[1])
        elif parts[0] == 'first-level-random-iteration':
            mrm.firstlevelrandomiteration = int(parts[1])
        elif parts[0] == 'second-level-random-iteration':
            mrm.secondlevelrandomiteration = int(parts[1])
        elif parts[0] == 'max-group-size':
            mrm.maxgroupsize = int(parts[1])
        elif parts[0] == 'fdr-cutoff':
            mrm.fdrcutoff = float(parts[1])
        elif parts[0] == 'gene-limit':
            mrm.genelimit = int(parts[1])
        elif parts[0] == 'gene-ranking-file':
            mrm.generankingfile = str(parts[1])
            # elif parts[0] == ???:
            #   mrm.score_cutoff = float(parts[1])
            # elif parts[0] == ???:
            #   mrm.genes_file = str(parts[1])
            # elif parts[0] == ???:
            #   mrm.sample_to_tissue_mapping_file = str(parts[1])
            # elif parts[0] == ???:
            #   mrm.randomize_data_matrix = bool(parts[1])
        #mrmessage.parameters[parts[0]]=parts[1]

    p_infh.close()
    return mrmessage

def assign_matrix_to_pb(minfl, dmvector, dmmatrix):
    m_infh = open(minfl, "r")

    #determine number of rows in matrix file
    nlines = sum(1 for line in m_infh) - 1
    m_infh.seek(0)

    #initialize counters and empty list of known size
    count = 0
    dmv_list = [None] * nlines

    #parse matrix file and begin protobuf assignment
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
            dmv_list[count - 1] = dmvector
            dmvector = MR_pb2.Vector()
        count += 1
    dmmatrix.rows.extend(dmv_list)
    m_infh.close()
    return dmmatrix

def write_pbo_to_json(outfile, message):
    json_str = google.protobuf.json_format.MessageToJson(message).replace('\n','')
    outfh = open(outfile, "w")
    outfh.write(json_str)
    outfh.close()

if __name__ == '__main__':
    mrm = assign_param_to_pb(p_infile,mrm)
    dmm = assign_matrix_to_pb(m_infile,dmv,dmm)
    mrm.matrixurl = args.maturl
    write_pbo_to_json(mrm_outfile, mrm)
    write_pbo_to_json(mat_outfile, dmm)