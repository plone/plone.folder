# -*- coding: utf-8 -*-
from Acquisition import Implicit
from plone.folder.interfaces import IOrderable
from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.testing import PLONEFOLDER_FUNCTIONAL_TESTING
from six import StringIO
from transaction import savepoint
from zope.interface import implementer

import unittest


@implementer(IOrderable)
class DummyFolder(OrderedBTreeFolderBase, Implicit):
    """ we need to mix in acquisition """

    meta_type = 'DummyFolder'


class IntegrationTests(unittest.TestCase):

    layer = PLONEFOLDER_FUNCTIONAL_TESTING

    def testExportDoesntIncludeParent(self):
        self.app = self.layer['app']
        self.app._setOb('foo', DummyFolder('foo'))
        foo = self.app.foo
        foo['bar'] = DummyFolder('bar')
        savepoint(optimistic=True)      # savepoint assigns oids
        # now let's export to a buffer and check the objects...
        exp = StringIO()
        self.app._p_jar.exportFile(foo.bar._p_oid, exp)
        self.failUnless('bar' in exp.getvalue())
        self.failIf('foo' in exp.getvalue())
