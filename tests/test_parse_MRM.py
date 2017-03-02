#!/usr/bin/env python

import unittest
import google.protobuf.json_format
import json

from mutex_agent import parse_MRM


class TestParseMRM(unittest.TestCase):

    good_mrm = {
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

    # def a test that looks for none or null values in parameters (TES won't handle them well)
    # make new test files for other (non parse_MRM.py) files
