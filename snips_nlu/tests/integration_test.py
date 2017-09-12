# coding=utf-8
from __future__ import unicode_literals

import os
import unittest

from nlu_metrics import compute_cross_val_metrics

from snips_nlu.nlu_engine import SnipsNLUEngine
from snips_nlu.tests.utils import TEST_PATH

INTENT_CLASSIFICATION_THRESHOLD = 0.8
SLOT_FILLING_THRESHOLD = 0.7


class IntegrationTestSnipsNLUEngine(unittest.TestCase):
    def test_engine_performance(self):
        # Given
        dataset_path = os.path.join(TEST_PATH, "resources",
                                    "performance_dataset.json")

        # When
        metrics = compute_cross_val_metrics(
            dataset=dataset_path, snips_nlu_rust_version="0.23.0",
            training_engine_class=SnipsNLUEngine)

        # Then
        for intent_name, intent_metrics in metrics.iteritems():
            if intent_name is None:
                continue
            classification_precision = intent_metrics["intent"]["precision"]
            classification_recall = intent_metrics["intent"]["recall"]
            self.assertGreaterEqual(
                classification_precision, INTENT_CLASSIFICATION_THRESHOLD,
                "Intent classification precision is too low (%.3f) for intent "
                "'%s'" % (classification_precision, intent_name))
            self.assertGreaterEqual(
                classification_recall, INTENT_CLASSIFICATION_THRESHOLD,
                "Intent classification recall is too low (%.3f) for intent "
                "'%s'" % (classification_recall, intent_name))
            for slot_name, slot_metrics in intent_metrics["slots"].iteritems():
                precision = slot_metrics["precision"]
                recall = slot_metrics["recall"]
                self.assertGreaterEqual(
                    precision, SLOT_FILLING_THRESHOLD,
                    "Slot precision is too low (%.3f) for slot '%s' of intent "
                    "'%s'" % (precision, slot_name, intent_name))
                self.assertGreaterEqual(
                    recall, SLOT_FILLING_THRESHOLD,
                    "Slot recall is too low (%.3f) for slot '%s' of intent "
                    "'%s'" % (recall, slot_name, intent_name))
