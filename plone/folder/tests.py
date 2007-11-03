import unittest

from plone.folder.ordered import OrderedBTreeFolder

from OFS.CopySupport import CopySource

# Much of this code is borrowed from OFS.tests.testOrderSupport

class DummyObject(CopySource):
    
    def __init__(self, id, meta_type):
        self.id = id
        self.meta_type = meta_type
        
    def cb_isMoveable(self):
        return 1
        
    def manage_afterAdd(self, item, container):
        return
        
    def manage_beforeDelete(self, item, container):
        return
        
    manage_afterAdd.__five_method__ = True
    manage_beforeDelete.__five_method__ = True
    
    def wl_isLocked(self):
        return 0

class TestCase(unittest.TestCase):
        
    def create(self):
        folder = OrderedBTreeFolder("f1")
        
        folder._setOb('o1', DummyObject('o1', 'mt1'))
        folder._setOb('o2', DummyObject('o2', 'mt1'))
        folder._setOb('o3', DummyObject('o3', 'mt1'))
        folder._setOb('o4', DummyObject('o4', 'mt1'))
        
        return folder
        
    # Test for ordering of basic methods
    
    def test_objectIdsOrdered(self):
        pass
    
    def test_objectValuesOrdered(self):
        pass
        
    def test_objectItemsOrdered(self):
        pass
        
    def test_contentIdsOrdered(self):
        pass
        
    def test_contentValuesOrdered(self):
        pass
        
    def test_contentItemsOrdered(self):
        pass
        
    # Tests borrowed from OFS.tests.testsOrderSupport
        
    def _doCanonTest(self, methodname, table):
        for args, order, rval in table:
            f = self.create()
            method = getattr(f, methodname)
            if rval == 'ValueError':
                self.failUnlessRaises( ValueError, method, *args )
            else:
                self.failUnlessEqual( method(*args), rval )
            self.failUnlessEqual( list(f.objectIds()), order )

    def test_moveObjectsUp(self):
        self._doCanonTest( 'moveObjectsUp',
              ( ( ( 'o4', 1 ),         ['o1', 'o2', 'o4', 'o3'], 1 )
              , ( ( 'o4', 2 ),         ['o1', 'o4', 'o2', 'o3'], 1 )
              , ( ( ('o1', 'o3'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o1', 'o3'), 9 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), 1 ), ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o1', 'o2', 'o3', 'o4') ),
                                       ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o2', 'o3', 'o4') ),
                                       ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), 1 ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o3', 'o1'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              )
            )

    def test_moveObjectsDown(self):
        self._doCanonTest( 'moveObjectsDown',
              ( ( ( 'o1', 1 ),         ['o2', 'o1', 'o3', 'o4'], 1 )
              , ( ( 'o1', 2 ),         ['o2', 'o3', 'o1', 'o4'], 1 )
              , ( ( ('o2', 'o4'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o4'), 9 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), 1 ), ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o1', 'o2', 'o3', 'o4') ),
                                       ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o1', 'o2', 'o3') ),
                                       ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), 1 ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o4', 'o2'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              )
            )

    def test_moveObjectsToTop(self):
        self._doCanonTest( 'moveObjectsToTop',
              ( ( ( 'o4', ),         ['o4', 'o1', 'o2', 'o3'], 1 )
              , ( ( ('o1', 'o3'), ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), ), ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), ('o1', 'o2', 'o3', 'o4') ),
                                     ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), ('o2', 'o3', 'o4') ),
                                     ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o3', 'o1'), ), ['o3', 'o1', 'o2', 'o4'], 1 )
              )
            )

    def test_moveObjectsToBottom(self):
        self._doCanonTest( 'moveObjectsToBottom',
              ( ( ( 'o1', ),         ['o2', 'o3', 'o4', 'o1'], 1 )
              , ( ( ('o2', 'o4'), ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), ), ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), ('o1', 'o2', 'o3', 'o4') ),
                                     ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), ('o1', 'o2', 'o3') ),
                                     ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o4', 'o2'), ), ['o1', 'o3', 'o4', 'o2'], 1 )
              )
            )

    def test_orderObjects(self):
        self._doCanonTest( 'orderObjects',
              ( ( ( 'id', 'id' ),       ['o4', 'o3', 'o2', 'o1'], 3)
              , ( ( 'meta_type', '' ),  ['o1', 'o3', 'o2', 'o4'], 1)
              , ( ( 'meta_type', 'n' ), ['o4', 'o2', 'o3', 'o1'], 3)
              , ( ( 'position', 0 ),    ['o1', 'o2', 'o3', 'o4'], 0)
              , ( ( 'position', 1 ),    ['o4', 'o3', 'o2', 'o1'], 3)
              )
            )

    def test_getObjectPosition(self):
        self._doCanonTest( 'getObjectPosition',
              ( ( ( 'o2', ), ['o1', 'o2', 'o3', 'o4'], 1)
              , ( ( 'o4', ), ['o1', 'o2', 'o3', 'o4'], 3)
              , ( ( 'n2', ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              )
            )

    def test_moveObjectToPosition(self):
        self._doCanonTest( 'moveObjectToPosition',
              ( ( ( 'o2', 2 ), ['o1', 'o3', 'o2', 'o4'], 1)
              , ( ( 'o4', 2 ), ['o1', 'o2', 'o4', 'o3'], 1)
              , ( ( 'n2', 2 ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              )
            )

def test_suite():
    return unittest.TestSuite([unittest.makeSuite(TestCase)])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')