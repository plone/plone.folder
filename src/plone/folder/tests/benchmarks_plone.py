# simple benchmarking tests related to plip191
# to run individual tests using:
# $ bin/instance test -s plone.folder --tests-pattern=benchmarks_plone -t <testName>
# where <testName> is something like "testObjectValuesOrdered"

from unittest import defaultTestLoader, main
from profilehooks import timecall
from random import randint

from transaction import commit
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.PloneBatch import Batch

# setup plone site
ptc.setupPloneSite()

# number of objects to create
SIZE = 500


class TestBenchmarkCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            app = ztc.app()
            portal = app.plone

            def create(container, nr):
                obj = _createObjectByType('Document', container, 'doc.%d' % nr)
                obj.setTitle('Title for %d' % nr)
                obj.setDescription('A long description for %d' % nr)
                obj.setText('This is the <b>HTML</b> text for item with id %d' % nr)
                obj.reindexObject(idxs=('Title', 'Description', 'SearchableText'))

            regular = _createObjectByType('Old Folder', portal, 'regular')
            large = _createObjectByType('Large Plone Folder', portal, 'large')
            ordered = _createObjectByType('Folder', portal, 'ordered')

            @timecall
            def testCreateContentRegular():
                for x in range(SIZE):
                    create(regular, x)
            @timecall
            def testCreateContentLarge():
                for x in range(SIZE):
                    create(large, x)
            @timecall
            def testCreateContentOrdered():
                for x in range(SIZE):
                    create(ordered, x)

            testCreateContentRegular()
            testCreateContentLarge()
            testCreateContentOrdered()

            commit()
            ztc.close(app)

        @classmethod
        def tearDown(cls):
            pass

    def afterSetUp(self):
        self.regular = self.portal.regular
        self.large = self.portal.large
        self.ordered = self.portal.ordered


    # basic content ids
    @timecall
    def testObjectIDsRegular(self):
        for x in range(5000):
            self.regular.objectIds(spec='ATDocument')
    @timecall
    def testObjectIDsLarge(self):
        for x in range(5000):
            self.large.objectIds(spec='ATDocument')
    @timecall
    def testObjectIDsOrdered(self):
        for x in range(5000):
            self.ordered.objectIds(spec='ATDocument')

    # basic content values -- read all
    @timecall
    def testObjectValuesRegular(self):
        for x in range(500):
            self.regular.objectValues()
    @timecall
    def testObjectValuesLarge(self):
        for x in range(500):
            self.large.objectValues()
    @timecall
    def testObjectValuesOrdered(self):
        for x in range(500):
            self.ordered.objectValues()

    # object positions
    @timecall
    def testObjectPositionRegular(self):
        id = 'doc.%d' % (SIZE / 2)
        for x in range(100 ** 2):
            self.regular.getObjectPosition(id)
    @timecall
    def testObjectPositionLarge(self):
        id = 'doc.%d' % (SIZE / 2)
        for x in range(100 ** 2):
            self.large.getObjectPosition(id)
    @timecall
    def testObjectPositionOrdered(self):
        id = 'doc.%d' % (SIZE / 2)
        for x in range(100 ** 2):
            self.ordered.getObjectPosition(id)

    # batching
    @timecall
    def testBatchRegular(self):
        for x in range(500):
            Batch(sequence=self.regular.objectValues(), size=SIZE / 10, start=SIZE * 4 / 5)
    @timecall
    def testBatchLarge(self):
        for x in range(500):
            Batch(sequence=self.large.objectValues(), size=SIZE / 10, start=SIZE * 4 / 5)
    @timecall
    def testBatchOrdered(self):
        for x in range(500):
            Batch(sequence=self.ordered.objectValues(), size=SIZE / 10, start=SIZE * 4 / 5)

    # random access
    @timecall
    def testRandomRegular(self):
        for x in range(1000):
            self.regular['doc.%d' % randint(0, SIZE-1)]
    @timecall
    def testRandomLarge(self):
        for x in range(1000):
            self.large['doc.%d' % randint(0, SIZE-1)]
    @timecall
    def testRandomOrdered(self):
        for x in range(1000):
            self.ordered['doc.%d' % randint(0, SIZE-1)]


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    main(defaultTest='test_suite')
