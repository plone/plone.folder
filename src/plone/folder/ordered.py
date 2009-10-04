from zope.interface import implements, alsoProvides
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.location.interfaces import ILocation

from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import access_contents_information
from AccessControl.Permissions import manage_properties
from OFS.interfaces import IOrderedContainer
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base, _marker
from Products.CMFCore.PortalFolder import PortalFolderBase
from Products.CMFCore.permissions import ModifyPortalContent

from plone.folder.interfaces import IOrderableFolder
from plone.folder.interfaces import IOrdering
from plone.folder.interfaces import IExplicitOrdering

from webdav.NullResource import NullResource

# XXX: Should move to zope.container in the future. However, a conditional
# import is dangerous. If we have zope.container, but not the version of
# zope.app.container that contains the requisite BBB aliases, we may end
# up checking the wrong IContained interface.
from zope.app.container.interfaces import IContainer
from zope.app.container.interfaces import IContained


class OrderedBTreeFolderBase(BTreeFolder2Base):
    """ BTree folder base class with ordering support. The ordering
        is done by adapter (to IOrdering), which makes the policy
        changeable. """
    implements(IContainer, IOrderedContainer, IOrderableFolder,
        IAttributeAnnotatable)

    security = ClassSecurityInfo()

    def __nonzero__(self):
        """ a folder is something, even if it's empty """
        return True

    # IObjectManager

    def _getOb(self, id, default=_marker):
        """ Return the named object from the folder. """
        try:
            return super(OrderedBTreeFolderBase, self)._getOb(id, default)
        except KeyError, e:
            raise AttributeError(e)

    def _setOb(self, id, object):
        """ Store the named object in the folder. """
        # Set __name__ and __parent__ if the object supports it
        if ILocation.providedBy(object):
            if not IContained.providedBy(object):
                alsoProvides(object, IContained)
            oldname = getattr(object, '__name__', None)
            oldparent = getattr(object, '__parent__', None)
            if id is not oldname:
                object.__name__ = id
            if self is not oldparent:
                object.__parent__ = self
        super(OrderedBTreeFolderBase, self)._setOb(id, object)
        IOrdering(self).notifyAdded(id)     # notify the ordering adapter

    def _delOb(self, id):
        """ Remove the named object from the folder. """
        # Unset __parent__ and __name__ prior to removing the object.
        # Note that there is a slight discrepancy with the Zope 3 behaviour
        # here: we do this before the IObjectRemovedEvent is fired. In
        # zope.container, IObjectRemovedEvent is fired before the object is
        # actually deleted and this information is unset. In Zope2's OFS,
        # there's a different IObjectWillBeRemovedEvent that is fired first,
        # then the object is removed, and then IObjectRemovedEvent is fired.
        try:
            obj = self._getOb(id, _marker)
            if obj is not _marker:
                if IContained.providedBy(obj):
                    obj.__parent__ = None
                    obj.__name__ = None
        except AttributeError:
            pass        # No need to fail if we can't set these
        super(OrderedBTreeFolderBase, self)._delOb(id)
        IOrdering(self).notifyRemoved(id)   # notify the ordering adapter

    def objectIds(self, spec=None, ordered=True):
        if not ordered:
            return super(OrderedBTreeFolderBase, self).objectIds(spec)
        ordering = IOrdering(self)
        if spec is None:
            return ordering.idsInOrder()
        else:
            ids = super(OrderedBTreeFolderBase, self).objectIds(spec)
            idxs = []
            for id in ids:
                idxs.append((ordering.getObjectPosition(id), id))
            return [x[1] for x in sorted(idxs, key=lambda a: a[0])]

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
    def moveObjectsByDelta(self, ids, delta, subset_ids=None,
            suppress_events=False):
        """ Move specified sub-objects by delta. """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsByDelta(ids, delta, subset_ids,
                suppress_events)
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

    def manage_renameObject(self, id, new_id, REQUEST=None):
        """ Rename a particular sub-object without changing its position. """
        old_position = self.getObjectPosition(id)
        result = super(OrderedBTreeFolderBase, self).manage_renameObject(id,
            new_id, REQUEST)
        if old_position is None:
            return result
        self.moveObjectToPosition(new_id, old_position, suppress_events=True)
        reindex = getattr(self._getOb(new_id), 'reindexObject', None)
        if reindex is not None:
            reindex(idxs=['getObjPositionInParent'])
        return result

    # Dict interface

    def __setitem__(self, key, value):
        self._setObject(key, value)

    def __contains__(self, key):
        return self.has_key(key)

    def __delitem__(self, key):
        self._delObject(key)

    def __getitem__(self, key):
        value = self._getOb(key, None)
        if value is not None:
            return value
        
        # WebDAV PUT support
        if hasattr(self, 'REQUEST'):
            request = self.REQUEST
            method = request.get('REQUEST_METHOD', 'GET')
            if getattr(request, 'maybe_webdav_client', False) and not method in ('GET', 'POST'):
                return NullResource(self, key, request).__of__(self)
        
        raise KeyError, key

    __iter__ = iterkeys
    keys = objectIds
    values = BTreeFolder2Base.objectValues
    items = BTreeFolder2Base.objectItems


class CMFOrderedBTreeFolderBase(OrderedBTreeFolderBase, PortalFolderBase):
    """ BTree folder for CMF sites, with ordering support. The ordering
        is done by adapter (to IOrdering), which makes the policy
        changeable. """

    def __init__(self, id, title=''):
        PortalFolderBase.__init__(self, id, title)
        BTreeFolder2Base.__init__(self, id)

    def _checkId(self, id, allow_dup=0):
        PortalFolderBase._checkId(self, id, allow_dup)
        BTreeFolder2Base._checkId(self, id, allow_dup)
