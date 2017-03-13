#!/usr/bin/env python

import unittest

from mutex_agent import create_matrix


class TestCreateMatrix(unittest.TestCase):

    good_endpoint = "http://localhost:9000/matrix"
    bad_endpoint = "http://localhost:9000/nothingtoseehere"

    # should i set good and bad matjson and mat_pb here to eliminate redundancy?
    # or does that eliminate the effects of self.fail etc.?


    def test_get_matrix_from_gaia(self):
        try:
            create_matrix.get_matrix_from_gaia(self.good_endpoint)
        except Exception as ex:
            self.fail(
                "get_matrix_from_gaia raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )


    def test_get_matrix_from_gaia_fails(self):
        with self.assertRaises(RuntimeError):
            create_matrix.get_matrix_from_gaia(self.bad_endpoint)


    def test_convert_matrix_to_pb(self):
        good_json = create_matrix.get_matrix_from_gaia(self.good_endpoint)
        try:
            create_matrix.convert_matrix_to_pb(good_json)
        except Exception as ex:
            self.fail(
                "convert_matrix_to_pb raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )


    '''
    # Won't be able to make a bad_json because the bad url will get a RunTime error...
    # Don't write this test until we know if and how gaia could send a bad matrix json back
    def test_convert_matrix_to_pb_fails(self,matjson):
        with self.assertRaises(???):     # is this the right kind of error?
            create_matrix.convert_matrix_to_pb(???)
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
    # Don't write this test until we know if and how gaia could send a bad matrix back
    def test_build_matrix_outfile_fails(self):
        good_json = create_matrix.get_matrix_from_gaia(self.good_endpoint)
        good_pb = create_matrix.convert_matrix_to_pb(good_json)
        bad_pb = create_matrix.convert_matrix_to_pb
        with self.assertRaises(AssertionError):
            build_matrix_outfile(bad_pb)
    '''