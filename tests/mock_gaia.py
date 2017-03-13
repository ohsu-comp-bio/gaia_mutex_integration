#!/usr/bin/env python

import argparse
import json
import google.protobuf.json_format
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from mutex_agent import MR_pb2
from flask import Flask

global matrix

app = Flask(__name__)


@app.route('/matrix', methods=['GET'])
def get_matrix():
    return matrix


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("gaiamsg")  # MatM.json (generated with MRM_Maker.assign_mat_to_pb)
    args = parser.parse_args()

    infh = open(args.gaiamsg, "r")
    json_msg = json.loads(infh.read())

    matrix_pbo = google.protobuf.json_format.Parse(json.dumps(json_msg), MR_pb2.Matrix(), ignore_unknown_fields=False)

    matrix = google.protobuf.json_format.MessageToJson(matrix_pbo).replace('\n','')

    app.run(host='0.0.0.0', port=9000)

