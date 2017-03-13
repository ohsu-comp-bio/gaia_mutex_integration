#!/usr/bin/env python

import unittest
import requests

from mutex_agent import mutex_agent # OY
from mutex_agent import MR_pb2
from mutex_agent import utils


class TestMutexAgent(unittest.TestCase):

    good_endpoint = "http://localhost:9000/matrix"
    bad_endpoint = "http://localhost:9000/notavalidpath"

    empty_mrm_pbo = MR_pb2.MutexRun()

    # make and fill good pbo
    good_mrm_pbo = MR_pb2.MutexRun()
    good_mrm_pbo.matrixurl = good_endpoint
    good_mrm_pbo.maxgroupsize = 5
    good_mrm_pbo.firstlevelrandomiteration = 10000
    good_mrm_pbo.searchonsignalingnetwork = True

    # make and fill bad pbo
    bad_mrm_pbo = MR_pb2.MutexRun()
    bad_mrm_pbo.matrixurl = bad_endpoint
    bad_mrm_pbo.scorecutoff = -1
    bad_mrm_pbo.fdrcutoff = -1

    # is this what a bad storage_pre might look like?
    good_storage_pre = "file://"
    bad_storage_pre = "bad"

    # wait until we know what a good/bad datapath will look like
    good_mrm_dict = utils.pbo_to_dict(good_mrm_pbo)
    # good_mrm_dict['datapath'] = pass

    # the following won't pass an assertion within utils.pbo_to_json
    # bad_mrm_dict = utils.pbo_to_dict(bad_mrm_pbo)

    good_task_message = mutex_agent.format_tes_message(good_mrm_dict, good_storage_pre)
    bad_task_message = mutex_agent.format_tes_message(good_mrm_dict, bad_storage_pre)


    def test_format_tes_message(self):
        try:
            mutex_agent.format_tes_message(self.good_mrm_dict, self.good_storage_pre)
        except Exception as ex:
            self.fail(
                "format_tes_message raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )


    def test_format_tes_message_fails(self):
        with self.assertRaises(AssertionError):  #   What kind of error will this be?
            mutex_agent.format_tes_message(self.good_mrm_dict, self.bad_storage_pre)

        #no bad_mrm_dict
        '''
        with self.assertRaises(AssertionError):
            mutex_agent.format_tes_message(self.bad_mrm_dict, self.good_storage_pre)
        with self.assertRaises(AssertionError):
            mutex_agent.format_tes_message(self.bad_mrm_dict, self.bad_storage_pre)
        '''

    # with a good task message and good endpoint it's throwing 405 errors
    # uncomment this part when this problem is understood
    '''
    def test_post_task(self):
        try:
            mutex_agent.post_task(self.good_task_message, self.good_endpoint)
        except Exception as ex:
            self.fail(
                "post_task raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )

    def test_post_task_fails(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            mutex_agent.post_task(self.good_task_message, self.bad_endpoint)
        with self.assertRaises(requests.exceptions.HTTPError):
            mutex_agent.post_task(self.bad_task_message, self.good_endpoint)
        with self.assertRaises(requests.exceptions.HTTPError):
            mutex_agent.post_task(self.bad_task_message, self.bad_endpoint)
    '''


    '''
    def test_main(self): #how do you run a test on a main function? it asks for argparse stuff
        try:
            mutex_agent.main()
        except Exception as ex:
            self.fail(
                "main raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )
    '''