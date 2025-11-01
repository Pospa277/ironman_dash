"""Tests for Apple Health Parser"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.apple_health_parser import AppleHealthParser


class TestAppleHealthParser(unittest.TestCase):
    """Test cases for AppleHealthParser"""

    def test_normalize_workout_type(self):
        """Test workout type normalization"""
        parser = AppleHealthParser("test.xml")

        self.assertEqual(parser._normalize_workout_type("HKWorkoutActivityTypeRunning"), "Running")
        self.assertEqual(parser._normalize_workout_type("HKWorkoutActivityTypeCycling"), "Cycling")
        self.assertEqual(parser._normalize_workout_type("HKWorkoutActivityTypeSwimming"), "Swimming")

    def test_parser_initialization(self):
        """Test parser initialization"""
        parser = AppleHealthParser("test.xml")
        self.assertEqual(parser.xml_path, "test.xml")
        self.assertEqual(parser.workouts, [])
        self.assertEqual(parser.records, [])


if __name__ == '__main__':
    unittest.main()
