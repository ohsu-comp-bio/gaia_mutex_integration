from __future__ import print_function

import google.protobuf.json_format
import os

from . import MR_pb2


def message_to_pbo(message):
    if os.path.exists(message):
        mrm_infh = open(message, "r")
        mrm_pbo = google.protobuf.json_format.Parse(
            mrm_infh.read(),
            MR_pb2.MutexRun(),
            ignore_unknown_fields=False
        )
        mrm_infh.close()
    else:
        mrm_pbo = google.protobuf.json_format.Parse(
            message,
            MR_pb2.MutexRun(),
            ignore_unknown_fields=False
        )
    return mrm_pbo

# def mrm_has_required_fields(mrm_pbo):


