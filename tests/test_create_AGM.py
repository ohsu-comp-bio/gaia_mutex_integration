#!/usr/bin/env python

import unittest

from mutex_agent import create_AGM

class TestCreateAGM(unittest.TestCase):

    good_AGM_q = "tests/resources/ranked-groups.txt"
    good_AGM_no_q = "tests/resources/ranked-groups-no-q.txt"
    bad_AGM = "tests/resources/ranked-groups-bad.txt"

    def test_convert_rg_to_json(self):

        try:
            create_AGM.convert_rg_to_json(self.good_AGM_q)
        except Exception as ex1:
            self.fail(
                "convert_rg_to_json raised ExceptionType: {0} unexpectedly!".format(type(ex1).__name__)
            )

        try:
            create_AGM.convert_rg_to_json(self.good_AGM_no_q)
        except Exception as ex2:
            self.fail(
                "convert_rg_to_json raised ExceptionType: {0} unexpectedly!".format(type(ex2).__name__)
            )

    def test_convert_rg_to_json_fails(self):
        with self.assertRaises(AssertionError):
            create_AGM.convert_rg_to_json(self.bad_AGM)