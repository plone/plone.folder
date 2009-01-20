from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable

from AccessControl import ClassSecurityInfo, Unauthorized
from AccessControl.Permissions import access_contents_information
from AccessControl.Permissions import manage_properties
from AccessControl.Permissions import delete_objects
from AccessControl.Permissions import view
from OFS.interfaces import IOrderedContainer
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base, _marker
from Products.CMFCore.PortalFolder import PortalFolderBase
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore import permissions
from Products.CMFCore.utils import _checkPermission

from plone.folder.interfaces import IOrderableFolder
from plone.folder.interfaces import IOrdering
from plone.folder.interfaces import IExplicitOrdering


class OrderedBTreeFolderBase(BTreeFolder2Base, PortalFolderBase):
    """ BTree folder for CMF sites, with ordering support. The ordering
        is done by adapter (to IOrdering), which makes the policy
        changeable. """
    implements(IOrderedContainer, IOrderableFolder, IAttributeAnnotatable)

    security = ClassSecurityInfo()

    def __init__(self, id, title=''):
        PortalFolderBase.__init__(self, id, title)
        BTreeFolder2Base.__init__(self, id)

    def _checkId(self, id, allow_dup=0):
        PortalFolderBase._checkId(self, id, allow_dup)
        BTreeFolder2Base._checkId(self, id, allow_dup)

    # IObjectManager

    def _getOb(self, id, default=_marker):
        """ Return the named object from the folder. """
        try:
            return super(OrderedBTreeFolderBase, self)._getOb(id, default)
        except KeyError, e:
            raise AttributeError(e)

    def _setOb(self, id, object):
        """ Store the named object in the folder. """
        super(OrderedBTreeFolderBase, self)._setOb(id, object)
        IOrdering(self).notifyAdded(id)     # notify the ordering adapter

    def _delOb(self, id):
        """ Remove the named object from the folder. """
        super(OrderedBTreeFolderBase, self)._delOb(id)
        IOrdering(self).notifyRemoved(id)   # notify the ordering adapter

    def objectIds(self, spec=None):
        ordering = IOrdering(self)

        if spec is None:
            return ordering.idsInOrder()
        else:
            ids = super(OrderedBTreeFolderBase, self).objectIds(spec)
            idxs = []
            for id in ids:
                idxs.append((ordering.getObjectPosition(id), id))
            return [ x[1] for x in sorted(idxs, cmp=lambda a,b: cmp(a[0], b[0])) ]

    # IOrderSupport - mostly deprecated, use the adapter directly instead

    security.declareProtected(access_contents_information, 'getObjectPosition')
    def getObjectPosition(self, id):
        """ Get the position of an object by its id. """
        return IOrdering(self).getObjectPosition(id)

    security.declareProtected(manage_properties, 'moveObjectsUp')
    def moveObjectsUp(self, ids, delta=1, subset_ids=None):
        """ Move specified sub-objects up by delta in container. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsUp(ids, delta, subset_ids)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsDown')
    def moveObjectsDown(self, ids, delta=1, subset_ids=None):
        """ Move specified sub-objects down by delta in container. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsDown(ids, delta, subset_ids)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsToTop')
    def moveObjectsToTop(self, ids, subset_ids=None):
        """ Move specified sub-objects to top of container. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsToTop(ids, subset_ids)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsToBottom')
    def moveObjectsToBottom(self, ids, subset_ids=None):
        """ Move specified sub-objects to bottom of container. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsToBottom(ids, subset_ids)
        else:
            return 0

    security.declareProtected(ModifyPortalContent, 'moveObject')
    def moveObject(self, id, position):
        """ Move specified object to absolute position. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectToPosition(id, position)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectToPosition')
    def moveObjectToPosition(self, id, position, suppress_events=False):
        """ Move specified object to absolute position. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectToPosition(id, position, suppress_events)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsByDelta')
    def moveObjectsByDelta(self, ids, delta, subset_ids=None, suppress_events=False):
        """ Move specified sub-objects by delta. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsByDelta(ids, delta, subset_ids, suppress_events)
        else:
            return 0

    security.declareProtected(manage_properties, 'orderObjects')
    def orderObjects(self, key, reverse=None):
        """ Order sub-objects by key and direction. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.orderObjects(key, reverse)
        else:
            return 0

    # Overrides for Plone-ish behaviour

    def iterkeys(self):
        return iter(self.objectIds())

    __iter__ = iterkeys

    def manage_renameObject(self, id, new_id, REQUEST=None):
        """ Rename a particular sub-object without changing its position. """
        old_position = self.getObjectPosition(id)
        result = super(OrderedBTreeFolderBase, self).manage_renameObject(id, new_id, REQUEST)
        self.moveObjectToPosition(new_id, old_position, suppress_events=True)
        reindex = getattr(self._getOb(new_id), 'reindexObject', None)
        if reindex is not None:
            reindex(idxs=('getObjPositionInParent',))
        return result

    security.declareProtected(view, 'getId')
    def getId(self):
        """ Ensure that getId() is protected by the View permission """
        return super(OrderedBTreeFolderBase, self).getId()

    security.declareProtected(delete_objects, 'manage_delObjects')
    def manage_delObjects(self, ids=[], REQUEST=None):
        """ Delete objects with the given id, but raise Unauthorized if
            the user does not have the "Delete objects" permission on
            each of them. """
        if isinstance(ids, basestring):
            ids = [ids]
        for id in ids:
            item = self._getOb(id)
            if not _checkPermission(permissions.DeleteObjects, item):
                raise Unauthorized, (
                    "Do not have permissions to remove this object")
        return super(OrderedBTreeFolderBase, self).manage_delObjects(ids, REQUEST=REQUEST)

