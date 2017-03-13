#!/usr/bin/env python

import unittest

from mutex_agent import create_matrix


class TestCreateMatrix(unittest.TestCase):

    good_endpoint = "http://localhost:9000/matrix"
    #bad_endpoint = pass
    # what can i do to mock a bad endpoint?
    # mock_gaia accepts everything as good right now

    # should i set good and bad matjson and mat_pb here to eliminate redundancy?
    # or does that eliminate the effects of self.fail etc.?

    def test_get_matrix_from_gaia(self):
        try:
            create_matrix.get_matrix_from_gaia(self.good_endpoint)
        except Exception as ex:
            self.fail(
                "get_matrix_from_gaia raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )
    '''
    def test_get_matrix_from_gaia_fails(self)
        with self.assertRaises(AssertionError):     # is this the right kind of error?
            create_matrix.get_matrix_from_gaia(self.bad_endpoint)
    '''

    def test_convert_matrix_to_pb(self):
        good_json = create_matrix.get_matrix_from_gaia(self.good_endpoint)

        try:
            create_matrix.convert_matrix_to_pb(good_json)
        except Exception as ex:
            self.fail(
                "convert_matrix_to_pb raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )

    '''
    def test_convert_matrix_to_pb_fails(self,matjson):
        with self.assertRaises(AssertionError):     # is this the right kind of error?
            create_matrix.convert_matrix_to_pb(self.bad_endpoint)
    '''

    def test_build_matrix_outfile(self):
        good_json = create_matrix.get_matrix_from_gaia(self.good_endpoint)
        good_pb = create_matrix.convert_matrix_to_pb(good_json)

        try:
            create_matrix.build_matrix_outfile("./dm_testout.txt", good_pb)
        except Exception as ex:
            self.fail(
                "build_matrix_outfile raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__))

    '''
    def test_build_matrix_outfile_fails(self):
        good_json = create_matrix.get_matrix_from_gaia(self.good_endpoint)
        good_pb = create_matrix.convert_matrix_to_pb(good_json)
        bad_pb = #do something bad to good_pb
        with self.assertRaises(AssertionError):
            build_matrix_outfile(bad_pb)
    '''