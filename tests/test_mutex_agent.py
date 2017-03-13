#!/usr/bin/env python

import unittest

from mutex_agent import mutex_agent # OY
from mutex_agent import MR_pb2
from mutex_agent import utils
from src import create_MRM


class TestMutexAgent(unittest.TestCase):

    good_endpoint = "http://localhost:9000/matrix"
    bad_endpoint = "http://localhost:9000/notavalidpath"

    empty_mrm = MR_pb2.MutexRun()   #good, we want it empty
    # maybe make a filled_mrm here? (bad)

    good_mrm_pbo = create_MRM.assign_param_to_pb("./tests/resources/parameters.txt", empty_mrm)
    good_mrm_pbo.matrixurl = good_endpoint

    #bad_mrm_pbo = pass

    good_storage_pre = "file://"
    #bad_storage_pre = pass

    good_mrm_dict = utils.pbo_to_dict(good_mrm_pbo)
    #good_mrm_dict['datapath'] = pass

    good_task_message = mutex_agent.format_tes_message(good_mrm_dict, good_storage_pre)
    #bad_task_message = pass


    def test_format_tes_message(self):
        try:
            mutex_agent.format_tes_message(self.good_mrm_dict, self.good_storage_pre)
        except Exception as ex:
            self.fail(
                "format_tes_message raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )

    '''
    def test_format_tes_message_fails(self):
        with self.assertRaises(AssertionError):  #   What kind of error will this be?
            mutex_agent.format_tes_message(self.good_mrm_dict, self.bad_storage_pre)
        with self.assertRaises(AssertionError):
            mutex_agent.format_tes_message(self.bad_mrm_dict, self.good_storage_pre)
        with self.assertRaises(AssertionError):
            mutex_agent.format_tes_message(self.bad_mrm_dict, self.bad_storage_pre)
    '''


    def test_post_task(self):
        try:
            mutex_agent.post_task(self.good_task_message, self.good_endpoint)
        except Exception as ex:
            self.fail(
                "post_task raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )

    '''
    def test_post_task_fails(self):
        with self.assertRaises(AssertionError):
            mutex_agent.post_task(self.good_task_message, self.bad_endpoint)
        with self.assertRaises(AssertionError):
            mutex_agent.post_task(self.bad_task_message, self.good_endpoint)
        with self.assertRaises(AssertionError):
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