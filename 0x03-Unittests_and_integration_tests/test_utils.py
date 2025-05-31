#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        # Test 1: Single key, direct value
        ({"a": 1}, ("a",), 1),
        
        # Test 2: One level deep, value is a dict
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        
        # Test 3: Two levels deep
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
