#!/usr/bin/env python

import unittest
from mutex_agent import utils

from mutex_agent import MR_pb2


class TestUtils(unittest.TestCase):

    bad_pbo = MR_pb2.MutexRun()

    # pbo doesn't need to be a mrm_pbo
    good_pbo = MR_pb2.MutexRun()
    good_pbo.matrixurl = "http://localhost:9000/matrix"
    good_pbo.searchonsignalingnetwork = bool("true")
    good_pbo.networkfile = "../resources/PC2v8.sif"
    good_pbo.firstlevelrandomiteration = 10000
    good_pbo.genelimit = 500
    good_pbo.generankingfile = "../resources/RankedGenes.txt"
    good_pbo.maxgroupsize = 5



    def test_pbo_to_json(self):
        try:
            utils.pbo_to_json(self.good_pbo)
        except Exception as ex:
            self.fail(
                "pbo_to_json raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )


    def test_pbo_to_json_fails(self):
        with self.assertRaises(AssertionError):
            utils.pbo_to_json(self.bad_pbo)


    def test_pbo_to_dict(self):
        try:
            utils.pbo_to_dict(self.good_pbo)
        except Exception as ex:
            self.fail(
                "pbo_to_dict raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )


    def test_pbo_to_dict_fails(self):
        with self.assertRaises(AssertionError):
            utils.pbo_to_dict(self.bad_pbo)