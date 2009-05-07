from Globals import InitializeClass
from ComputedAttribute import ComputedAttribute
from OFS.interfaces import IOrderedContainer as IOrderedContainer
from OFS.IOrderSupport import IOrderedContainer as Z2IZopeOrderedContainer
from OFS.ObjectManager import REPLACEABLE
from webdav.NullResource import NullResource
from zope.interface import implements
from Products.CMFPlone.interfaces.OrderedContainer import IOrderedContainer as Z2IOrderedContainer
from Products.Archetypes.atapi import BaseFolder
from plone.folder.ordered import OrderedBTreeFolderBase


# to keep backward compatibility
has_btree = 1


class BaseBTreeFolder(OrderedBTreeFolderBase, BaseFolder):
    """ a base class for btree-based folders supporting ordering """
    implements(IOrderedContainer)

    __implements__ = (BaseFolder.__implements__,
                      Z2IOrderedContainer, Z2IZopeOrderedContainer)

    def __init__(self, oid, **kwargs):
        OrderedBTreeFolderBase.__init__(self, oid)
        BaseFolder.__init__(self, oid, **kwargs)

    def _checkId(self, id, allow_dup=0):
        OrderedBTreeFolderBase._checkId(self, id, allow_dup)
        BaseFolder._checkId(self, id, allow_dup)

    def __getitem__(self, key):
        """ Override BTreeFolder __getitem__ """
        if key in self.Schema().keys() and key[:1] != "_": #XXX 2.2
            accessor = self.Schema()[key].getAccessor(self)
            if accessor is not None:
                return accessor()
        return super(BaseBTreeFolder, self).__getitem__(key)

    # override the version from `CMFDynamicViewFTI/browserdefault.py:72`
    __call__ = BaseFolder.__call__.im_func

    def index_html(self):
        """ Allow creation of . """
        if self.has_key('index_html'):
            return self._getOb('index_html')
        request = getattr(self, 'REQUEST', None)
        if request and request.has_key('REQUEST_METHOD'):
            if (request.maybe_webdav_client and
                request['REQUEST_METHOD'] in ['PUT']):
                # Very likely a WebDAV client trying to create something
                nr = NullResource(self, 'index_html')
                nr.__replaceable__ = REPLACEABLE
                return nr
        return None

    index_html = ComputedAttribute(index_html, 1)


InitializeClass(BaseBTreeFolder)

BaseBTreeFolderSchema = BaseBTreeFolder.schema
