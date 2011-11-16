#!/usr/bin/env python

import unittest
import logging

import ecks

from pprint import pprint

logging.basicConfig(level=logging.FATAL)

class TestEcks(unittest.TestCase):
    def test_plugins_with_responding_host(self):
        e = ecks.Ecks(5)
        for plugin in e.plugins:
            data = e.get_data("localhost", "public", plugin)
            #self.assertTrue((data != None) and (data != []))
            self.assertTrue(data)

    def test_plugins_with_unresponding_host(self):
        e = ecks.Ecks()
        for plugin in e.plugins:
            data = e.get_data("localhost", "private", plugin)

            #self.assertTrue((data == None) or (data == []))
            self.assertTrue(not data)

    def test_plugins_with_unreachable_host(self):
        e = ecks.Ecks()
        for plugin in e.plugins:
            data = e.get_data("127.1.1.1", "public", plugin)

            #self.assertTrue((data == None) or (data == []))
            self.assertTrue(not data)

if __name__ == '__main__':
    unittest.main()
