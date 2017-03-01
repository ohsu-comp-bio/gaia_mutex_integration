#!/usr/bin/env python

from __future__ import print_function

import json
import google.protobuf.json_format
import os

from . import MR_pb2


def loadMessage(message):
    try:
        if os.path.exists(message):
            mrm_infh = open(message, "rb")
            mrm_json = json.loads(mrm_infh.read())
        else:
            mrm_json = json.loads(message)
        return mrm_json
    except:
        raise RuntimeError("Failed to parse json message")


# validate the json message on protobuf schema
def validateMessage(mrm_json):
    try:
        google.protobuf.json_format.Parse(
            json.dumps(mrm_json),
            MR_pb2.MutexRun(),
            ignore_unknown_fields=False
        )
        return True
    except:
        return False
