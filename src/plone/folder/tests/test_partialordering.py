from unittest import TestCase, defaultTestLoader
from plone.folder.interfaces import IOrdering
from plone.folder.tests.utils import DummyContainer
from plone.folder.tests.utils import Orderable, Chaoticle
from plone.folder.tests.layer import PartialOrderingLayer


class PartialOrderingTests(TestCase):
    """ tests regarding order-support for only items marked orderable """

    layer = PartialOrderingLayer

    def create(self):
        container = DummyContainer()
        container.add('o1', Orderable('o1', 'mt1'))
        container.add('o2', Orderable('o2', 'mt2'))
        container.add('c1', Chaoticle('c1', 'mt3'))
        container.add('o3', Orderable('o3', 'mt1'))
        container.add('c2', Chaoticle('c2', 'mt2'))
        container.add('c3', Chaoticle('c3', 'mt1'))
        container.add('o4', Orderable('o4', 'mt2'))
        self.unordered = ['c3', 'c2', 'c1']
        return container

    def testAdapter(self):
        container = DummyContainer()
        ordering = IOrdering(container)
        self.failUnless(ordering)

    def testNotifyAdded(self):
        container = self.create()
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4'] + self.unordered)
        container.add('o5', Orderable('o5'))
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4', 'o5'] + self.unordered)
        self.assertEqual(container.objectIds(),
            set(['o1', 'o2', 'o3', 'o4', 'o5', 'c1', 'c2', 'c3']))

    def testNotifyRemoved(self):
        container = self.create()
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4'] + self.unordered)
        container.remove('o3')
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o4'] + self.unordered)
        self.assertEqual(container.objectIds(),
            set(['o1', 'o2', 'o4', 'c1', 'c2', 'c3']))
        container.remove('o1')
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o2', 'o4'] + self.unordered)
        self.assertEqual(container.objectIds(),
            set(['o2', 'o4', 'c1', 'c2', 'c3']))

    def runTableTests(self, action, tests):
        for args, order, rval in tests:
            container = self.create()
            ids = container.objectIds()
            ordering = IOrdering(container)
            method = getattr(ordering, action)
            if type(rval) == type(Exception):
                self.assertRaises(rval, method, *args)
            else:
                self.assertEqual(method(*args), rval)
            self.assertEqual(ordering.idsInOrder(), order + self.unordered)
            self.assertEqual(container.objectIds(), ids)

    def testMoveObjectsByDelta(self):
        self.runTableTests('moveObjectsByDelta', (
            (('o1', 1),                                   ['o2', 'o1', 'o3', 'o4'], 1),
            (('o1', 2),                                   ['o2', 'o3', 'o1', 'o4'], 1),
            ((('o2', 'o4'), 1),                           ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o2', 'o4'), 9),                           ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o2', 'o3'), 1),                           ['o1', 'o4', 'o2', 'o3'], 2),
            ((('o2', 'o3'), 1, ('o1', 'o2', 'o3', 'o4')), ['o1', 'o4', 'o2', 'o3'], 2),
            ((('o2', 'o3'), 1, ('o1', 'o2', 'o3')),       ['o1', 'o2', 'o3', 'o4'], 0),
            ((('c1', 'o1'), 2),                           ['o2', 'o3', 'o1', 'o4'], 1),
            ((('c1', 'o3'), 1),                           ['o1', 'o2', 'o4', 'o3'], 1),
            ((('n2', 'o2'), 1),                           ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o4', 'o2'), 1),                           ['o1', 'o3', 'o2', 'o4'], 1),
        ))

    def testMoveObjectsDown(self):
        self.runTableTests('moveObjectsDown', (
            (('o1',),                                     ['o2', 'o1', 'o3', 'o4'], 1),
            (('o1', 2),                                   ['o2', 'o3', 'o1', 'o4'], 1),
            ((('o2', 'o4'),),                             ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o2', 'o4'), 9),                           ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o2', 'o3'),),                             ['o1', 'o4', 'o2', 'o3'], 2),
            ((('o2', 'o3'), 1, ('o1', 'o2', 'o3', 'o4')), ['o1', 'o4', 'o2', 'o3'], 2),
            ((('o2', 'o3'), 1, ('o1', 'o2', 'o3')),       ['o1', 'o2', 'o3', 'o4'], 0),
            ((('c1', 'o1'), 2),                           ['o2', 'o3', 'o1', 'o4'], 1),
            ((('c1', 'o3'),),                             ['o1', 'o2', 'o4', 'o3'], 1),
            ((('n2', 'o2'),),                             ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o4', 'o2'),),                             ['o1', 'o3', 'o2', 'o4'], 1),
        ))

    def testMoveObjectsUp(self):
        self.runTableTests('moveObjectsUp', (
            (('o4',),                                     ['o1', 'o2', 'o4', 'o3'], 1),
            (('o4', 1),                                   ['o1', 'o2', 'o4', 'o3'], 1),
            (('o4', 2),                                   ['o1', 'o4', 'o2', 'o3'], 1),
            ((('o1', 'o3'), 1),                           ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o1', 'o3'), 9),                           ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o2', 'o3'), 1),                           ['o2', 'o3', 'o1', 'o4'], 2),
            ((('o2', 'o3'), 1, ('o1', 'o2', 'o3', 'o4')), ['o2', 'o3', 'o1', 'o4'], 2),
            ((('o2', 'o3'), 1, ('o2', 'o3', 'o4')),       ['o1', 'o2', 'o3', 'o4'], 0),
            ((('c1', 'o4'), 2),                           ['o1', 'o4', 'o2', 'o3'], 1),
            ((('c1', 'o3'),),                             ['o1', 'o3', 'o2', 'o4'], 1),
            ((('n2', 'o3'), 1),                           ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o3', 'o1'), 1),                           ['o1', 'o3', 'o2', 'o4'], 1),
        ))

    def testMoveObjectsToTop(self):
        self.runTableTests('moveObjectsToTop', (
            (('o4',),                                  ['o4', 'o1', 'o2', 'o3'], 1),
            ((('o1', 'o3'),),                          ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o2', 'o3'),),                          ['o2', 'o3', 'o1', 'o4'], 2),
            ((('o2', 'o3'), ('o1', 'o2', 'o3', 'o4')), ['o2', 'o3', 'o1', 'o4'], 2),
            ((('o2', 'o3'), ('o2', 'o3', 'o4')),       ['o1', 'o2', 'o3', 'o4'], 0),
            ((('c1', 'o4'),),                          ['o4', 'o1', 'o2', 'o3'], 1),
            ((('c1', 'o3'),),                          ['o3', 'o1', 'o2', 'o4'], 1),
            ((('n2', 'o3'),),                          ['o3', 'o1', 'o2', 'o4'], 1),
            ((('o3', 'o1'),),                          ['o3', 'o1', 'o2', 'o4'], 1),
        ))

    def testMoveObjectsToBottom(self):
        self.runTableTests('moveObjectsToBottom', (
            (('o1',),                                  ['o2', 'o3', 'o4', 'o1'], 1),
            ((('o2', 'o4'),),                          ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o2', 'o3'),),                          ['o1', 'o4', 'o2', 'o3'], 2),
            ((('o2', 'o3'), ('o1', 'o2', 'o3', 'o4')), ['o1', 'o4', 'o2', 'o3'], 2),
            ((('o2', 'o3'), ('o1', 'o2', 'o3')),       ['o1', 'o2', 'o3', 'o4'], 0),
            ((('c1', 'o1'),),                          ['o2', 'o3', 'o4', 'o1'], 1),
            ((('c1', 'o2'),),                          ['o1', 'o3', 'o4', 'o2'], 1),
            ((('n2', 'o3'),),                          ['o1', 'o2', 'o4', 'o3'], 1),
            ((('o4', 'o2'),),                          ['o1', 'o3', 'o4', 'o2'], 1),
        ))

    def testMoveObjectToPosition(self):
        self.runTableTests('moveObjectToPosition', (
            (('o2', 2), ['o1', 'o3', 'o2', 'o4'], 1),
            (('o4', 2), ['o1', 'o2', 'o4', 'o3'], 1),
            (('c1', 2), ['o1', 'o2', 'o3', 'o4'], None),    # existent, but non-orderable
            (('n2', 2), ['o1', 'o2', 'o3', 'o4'], ValueError),
        ))

    def testOrderObjects(self):
        self.runTableTests('orderObjects', (
            (('id', 'id'),       ['o4', 'o3', 'o2', 'o1'], -1),
            (('meta_type', ''),  ['o1', 'o3', 'o2', 'o4'], -1),
            # for the next line the sort order is different from the
            # original test in OFS, since the current implementation
            # keeps the original order as much as possible, i.e. minimize
            # exchange operations within the list;  this is correct as
            # far as the test goes, since it didn't specify a secondary
            # sort key...
            (('meta_type', 'n'), ['o2', 'o4', 'o1', 'o3'], -1),
        ))

    def testGetObjectPosition(self):
        self.runTableTests('getObjectPosition', (
            (('o2',), ['o1', 'o2', 'o3', 'o4'], 1),
            (('o4',), ['o1', 'o2', 'o3', 'o4'], 3),
            (('n2',), ['o1', 'o2', 'o3', 'o4'], ValueError),
            (('c2',), ['o1', 'o2', 'o3', 'o4'], None),      # existent, but non-orderable
        ))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
