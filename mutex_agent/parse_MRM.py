from __future__ import print_function

import google.protobuf.json_format
import os

from . import MR_pb2


def message_to_pbo(message):

    if os.path.exists(message):     # if "message" is a file...
        mrm_infh = open(message, "r")
        mrm_pbo = google.protobuf.json_format.Parse(
            mrm_infh.read(),
            MR_pb2.MutexRun(),
            ignore_unknown_fields=False
        )
        mrm_infh.close()

    else:                           # if raw "message" is provided, i.e. copied and pasted...
        mrm_pbo = google.protobuf.json_format.Parse(
            message,
            MR_pb2.MutexRun(),
            ignore_unknown_fields=False
        )

    assert_reqd_fields(mrm_pbo)

    return mrm_pbo


def assert_reqd_fields(mrm_pbo):

    reqd_fields = {'matrixurl': str,
                   'maxgroupsize': int,
                   'firstlevelrandomiteration': int,
                   'searchonsignalingnetwork': bool}

    for k, v in reqd_fields.items():
        paramval = mrm_pbo.__getattribute__(k)
        assert type(paramval) is v
        assert paramval != ('' or 0)
        if k == "maxgroupsize":
            assert paramval != 1