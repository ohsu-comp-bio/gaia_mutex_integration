#!/usr/bin/env python

import unittest

from mutex_agent import parse_MRM


class TestParseMRM(unittest.TestCase):

    good_mrm = {
        "data_file": "/Users/strucka/Projects/gaia_mutex_integration/tests/resources/DataMatrix.txt",
        "max_group_size": 5,
        "first_level_random_iteration": 10000,
        "second_level_random_iteration": 100,
        "search_on_signaling_network": True,
        "network_file": "/Users/strucka/Projects/gaia_mutex_integration/tests/resources/PC2v8.sif",
        "genes_file": None,
        "gene_ranking_file": "/Users/strucka/Projects/gaia_mutex_integration/tests/resources/RankedGenes.txt",
        "gene_limit": None,
        "score_cutoff": -1,
        "fdr_cutoff": -1,
        "sample_to_tissue_mapping_file": None,
        "minimum_alteration_count_threshold": None
    }

    bad_mrm = {
        "badkey": "test",
        "score_cutoff": -1,
        "fdr_cutoff": -1,
    }

    good_json = '{"foo": "bar"}'

    bad_json = '{"foo": "bar", bad: val}'

    def testLoad(self):
        try:
            parse_MRM.loadMessage(self.good_json)
        except Exception as ex:
            self.fail(
                "loadMessage() raised ExceptionType: {0} unexpectedly!".format(type(ex).__name__)
            )

    def testLoadFails(self):
        with self.assertRaises(RuntimeError):
            parse_MRM.loadMessage(self.bad_json)

    def testValidate(self):
        self.assertTrue(parse_MRM.validateMessage(self.good_mrm))
        self.assertFalse(parse_MRM.validateMessage(self.bad_mrm))
