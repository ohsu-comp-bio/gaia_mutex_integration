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


# won't allow:
#  for i in mrm_pbo.DESCRIPTOR.fields_by_name:
#   mrm_pbo.i ...
#   ("mrm_pbo has no field i" )
def assert_reqd_fields(mrm_pbo):

    assert "matrixurl" and \
           "maxgroupsize" and \
           "firstlevelrandomiteration" and \
           "searchonsignalingnetwork" in mrm_pbo.DESCRIPTOR.fields_by_name

    for i in mrm_pbo.DESCRIPTOR.fields_by_name:
        if i == "matrixurl":
            assert type(mrm_pbo.matrixurl) is str
            assert mrm_pbo.matrixurl != ''
        if i == "maxgroupsize":
            assert type(mrm_pbo.maxgroupsize) is int
            assert mrm_pbo.maxgroupsize != (0 or 1)
        if i == "firstlevelrandomiteration":
            assert type(mrm_pbo.firstlevelrandomiteration) is int
            assert mrm_pbo.firstlevelrandomiteration != 0
        if i == "searchonsignalingnetwork":
            assert type(mrm_pbo.searchonsignalingnetwork) is bool


