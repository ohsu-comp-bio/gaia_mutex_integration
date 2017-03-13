#!/usr/bin/env python

import unittest
import google.protobuf.json_format
import json

from mutex_agent import parse_MRM


class TestParseMRM(unittest.TestCase):

    good_mrm = {
        "matrixurl": "http://localhost:9000/matrix",
        "maxgroupsize": 5,
        "firstlevelrandomiteration": 10000,
        "secondlevelrandomiteration": 100,
        "searchonsignalingnetwork": True,
        "networkfile": "/Users/strucka/Projects/gaia_mutex_integration/tests/resources/PC2v8.sif",
        "genesfile": None,
        "generankingfile": "/Users/strucka/Projects/gaia_mutex_integration/tests/resources/RankedGenes.txt",
        "genelimit": None,
        "scorecutoff": -1,
        "fdrcutoff": -1,
        "sampletotissuemappingfile": None,
        "minimumalterationcountthreshold": None,
        "randomizedatamatrix" : False
    }

    bad_mrm = {
        "badkey": "test",
        "scorecutoff": -1,
        "fdrcutoff": -1,
    }

    def test_message_to_pbo(self):
        try:
            parse_MRM.message_to_pbo(json.dumps(self.good_mrm))
        except Exception as ex:
            self.fail(
                "message_to_pbo() raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )

    def test_message_to_pbo_fails(self):
        with self.assertRaises(google.protobuf.json_format.ParseError):
            parse_MRM.message_to_pbo(json.dumps(self.bad_mrm))