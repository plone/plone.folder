# -*- coding: utf-8 -*-
from Acquisition import Explicit
from plone.folder.ordered import CMFOrderedBTreeFolderBase
from plone.folder.testing import PLONEFOLDER_INTEGRATION_TESTING
from plone.folder.tests.utils import DummyObject
from zope.publisher.browser import TestRequest

import pkg_resources
import unittest


HAS_ZSERVER = True
try:
    dist = pkg_resources.get_distribution('ZServer')
except pkg_resources.DistributionNotFound:
    HAS_ZSERVER = False

if HAS_ZSERVER:
    from webdav.NullResource import NullResource


class TestRequestContainer(Explicit):

    REQUEST = TestRequest()


class WebDAVTests(unittest.TestCase):
    """ tests regarding support for WebDAV NullResources """

    layer = PLONEFOLDER_INTEGRATION_TESTING

    def test_getitem_not_dav_request(self):
        root = TestRequestContainer()
        folder = CMFOrderedBTreeFolderBase("f1").__of__(root)

        root.REQUEST.maybe_webdav_client = False
        root.REQUEST._environ['REQUEST_METHOD'] = 'GET'

        foo = DummyObject('foo')
        folder['foo'] = foo

        self.assertEquals(folder['foo'], foo)
        try:
            folder['bar']
            self.fail()
        except KeyError:
            pass

    @unittest.skipUnless(HAS_ZSERVER, 'ZServer is optional')
    def test_getitem_dav_request(self):
        root = TestRequestContainer()
        folder = CMFOrderedBTreeFolderBase("f1").__of__(root)

        root.REQUEST.maybe_webdav_client = True
        root.REQUEST._environ['REQUEST_METHOD'] = 'PUT'

        foo = DummyObject('foo')
        folder['foo'] = foo

        self.assertEquals(folder['foo'], foo)
        self.assertTrue(isinstance(folder['bar'], NullResource))
