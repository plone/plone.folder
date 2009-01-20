from unittest import TestCase, defaultTestLoader
from zope.component import provideAdapter
from zope.component import testing
from plone.folder.interfaces import IOrdering
from plone.folder.partial import PartialOrdering
from plone.folder.tests.utils import DummyContainer
from plone.folder.tests.utils import Orderable, Chaoticle


class Layer:

    @classmethod
    def setUp(cls):
        provideAdapter(PartialOrdering)

    @classmethod
    def tearDown(cls):
        testing.tearDown


class PartialOrderingTests(TestCase):
    """ tests regarding order-support for only items marked orderable """

    layer = Layer

    def create(self):
        container = DummyContainer()
        container.add('o1', Orderable('o1'))
        container.add('o2', Orderable('o2'))
        container.add('c1', Chaoticle('c1'))
        container.add('o3', Orderable('o3'))
        container.add('c2', Chaoticle('c2'))
        container.add('c3', Chaoticle('c3'))
        container.add('o4', Orderable('o4'))
        return container

    def testAdapter(self):
        container = DummyContainer()
        ordering = IOrdering(container)
        self.failUnless(ordering)

    def testNotifyAdded(self):
        container = self.create()
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4'])
        container.add('o5', Orderable('o5'))
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4', 'o5'])
        self.assertEqual(container.ids(),
            set(['o1', 'o2', 'o3', 'o4', 'o5', 'c1', 'c2', 'c3']))

    def testNotifyRemoved(self):
        container = self.create()
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4'])
        container.remove('o3')
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o1', 'o2', 'o4'])
        self.assertEqual(container.ids(),
            set(['o1', 'o2', 'o4', 'c1', 'c2', 'c3']))
        container.remove('o1')
        self.assertEqual(IOrdering(container).idsInOrder(),
            ['o2', 'o4'])
        self.assertEqual(container.ids(),
            set(['o2', 'o4', 'c1', 'c2', 'c3']))

    def runTableTests(self, action, tests):
        for args, order, rval in tests:
            container = self.create()
            ids = container.ids()
            ordering = IOrdering(container)
            method = getattr(ordering, action)
            if isinstance(rval, Exception):
                self.assertRaises(rval, method, *args)
            else:
                self.assertEqual(method(*args), rval)
            self.assertEqual(ordering.idsInOrder(), order)
            self.assertEqual(container.ids(), ids)

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
            ((('n2', 'o3'), 1 ),                          ['o1', 'o3', 'o2', 'o4'], 1),
            ((('o3', 'o1'), 1 ),                          ['o1', 'o3', 'o2', 'o4'], 1),
        ))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

