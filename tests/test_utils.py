#!/usr/bin/env python

import unittest
from mutex_agent import utils
import google.protobuf.json_format

from mutex_agent import MR_pb2


class TestUtils(unittest.TestCase):

    good_pbo = MR_pb2.MutexRun()

    good_pbo.matrixurl = "http://localhost:9000/matrix"
    good_pbo.searchonsignalingnetwork = "true"
    good_pbo.networkfile = "../resources/PC2v8.sif"
    good_pbo.firstlevelrandomiteration = 10000
    good_pbo.genelimit = 500
    good_pbo.generankingfile = "../resources/RankedGenes.txt"
    good_pbo.maxgroupsize = 5

    bad_pbo = MR_pb2.MutexRun()

    bad_pbo.fdrcutoff = -1
    bad_pbo.scorecutoff = -1

    def test_pbo_to_json(self):
        try:
            utils.pbo_to_json(self.good_pbo)
        except EXCEPTION as ex:
            #do this part



    def test_pbo_to_json_fails(self):
        pass


    def test_pbo_to_dict(self):
        pass


    def test_pbo_to_dict_fails(self):
        pass