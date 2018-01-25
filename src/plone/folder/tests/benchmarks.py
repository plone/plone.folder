# -*- coding: utf-8 -*-
# simple benchmarking tests related to plip191
# to run individual tests using:
# $ bin/instance test -s plone.folder --tests-pattern=benchmarks -t <testName>
# where <testName> is something like "testDeleteSpeed"

from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.tests.layer import PloneFolderLayer
from plone.folder.tests.utils import DummyObject
from profilehooks import timecall
from six.moves import range
from unittest import defaultTestLoader
from unittest import TestCase


class BenchmarkTests(TestCase):

    layer = PloneFolderLayer

    def testDeleteSpeed(self):
        folder = OrderedBTreeFolderBase("f1")
        for idx in range(100000):
            id = 'foo-%s' % idx
            folder[id] = DummyObject(id, 'bar')
        last = reversed(folder.keys()[-100:])

        @timecall
        def delete():
            for id in last:
                del folder[id]
        delete()


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
