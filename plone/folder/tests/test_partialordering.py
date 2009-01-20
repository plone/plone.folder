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

    def setUp(self):
        self.container = DummyContainer()
        self.container.add('o1', Orderable('o1'))
        self.container.add('o2', Orderable('o2'))
        self.container.add('c1', Chaoticle('c1'))
        self.container.add('o3', Orderable('o3'))
        self.container.add('c2', Chaoticle('c2'))
        self.container.add('c3', Chaoticle('c3'))
        self.container.add('o4', Orderable('o4'))

    def testAdapter(self):
        ordering = IOrdering(self.container)
        self.failUnless(ordering)

    def testNotifyAdded(self):
        self.assertEqual(IOrdering(self.container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4'])
        self.container.add('o5', Orderable('o5'))
        self.assertEqual(IOrdering(self.container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4', 'o5'])
        self.assertEqual(self.container.ids(),
            set(['o1', 'o2', 'o3', 'o4', 'o5', 'c1', 'c2', 'c3']))

    def testNotifyRemoved(self):
        self.assertEqual(IOrdering(self.container).idsInOrder(),
            ['o1', 'o2', 'o3', 'o4'])
        self.container.remove('o3')
        self.assertEqual(IOrdering(self.container).idsInOrder(),
            ['o1', 'o2', 'o4'])
        self.assertEqual(self.container.ids(),
            set(['o1', 'o2', 'o4', 'c1', 'c2', 'c3']))
        self.container.remove('o1')
        self.assertEqual(IOrdering(self.container).idsInOrder(),
            ['o2', 'o4'])
        self.assertEqual(self.container.ids(),
            set(['o2', 'o4', 'c1', 'c2', 'c3']))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

