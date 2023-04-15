from Acquisition import aq_base
from App.special_dtml import DTMLFile
from inspect import currentframe
from logging import getLogger
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.interfaces import ISiteRoot
from Products.PluginIndexes.interfaces import IPluggableIndex
from Products.PluginIndexes.interfaces import ISortIndex
from zope.component import getUtility
from zope.interface import implementer


logger = getLogger(__name__)


def traverse(base, path):
    """simplified fast unrestricted traverse.
    base: the app-root to start from
    path: absolute path from app root as string
    returns: content at the end or None
    """
    current = base
    for cid in path.split("/"):
        if not cid:
            continue
        try:
            current = current[cid]
        except KeyError:
            return None
    return current


@implementer(IPluggableIndex)
class StubIndex(SimpleItem):
    """stub catalog index doing nothing"""

    def __init__(self, id, *args, **kw):
        self.id = id

    def getId(self):
        return self.id

    def getEntryForObject(self, *args, **kw):
        return []

    def getIndexSourceNames(self):
        return [self.id]

    def index_object(self, *args, **kw):
        return 0

    def unindex_object(self, *args, **kw):
        pass

    def _apply_index(self, *args, **kw):
        return None

    def numObjects(self):
        return 0

    def clear(self):
        pass


@implementer(ISortIndex)
class GopipIndex(StubIndex):
    """fake index for sorting against `getObjPositionInParent`"""

    meta_type = "GopipIndex"
    manage_options = (dict(label="Settings", action="manage_main"),)

    keyForDocument = 42

    def __init__(self, id, extra=None, caller=None):
        super().__init__(id)
        self.catalog = aq_base(caller._catalog)

    def __len__(self):
        # with python 2.4 returning `sys.maxint` gives:
        # OverflowError: __len__() should return 0 <= outcome < 2**31
        # so...
        return 2**31 - 1

    def documentToKeyMap(self):
        # we need to get the containers in order to get the respective
        # positions of the search results, but before that we need those
        # results themselves.  luckily this is only ever called from
        # `sortResults`, so we can get it form there.  oh, and lurker
        # says this won't work in jython, though! :)
        rs = currentframe().f_back.f_locals["rs"]
        rids = {}
        items = []
        containers = {}
        getpath = self.catalog.paths.get
        root = getUtility(ISiteRoot).getPhysicalRoot()
        for rid in rs:
            path = getpath(rid)
            parent, id = path.rsplit("/", 1)
            container = containers.get(parent)
            if container is None:
                containers[parent] = container = traverse(root, parent)
            rids[id] = rid  # remember in case of single folder
            items.append((rid, container, id))  # or else for deferred lookup
        pos = {}
        if len(containers) == 1:
            # the usual "all from one folder" case can be optimized
            folder = list(containers.values())[0]
            if getattr(aq_base(folder), "getOrdering", None):
                ids = folder.getOrdering().idsInOrder()
            else:
                # site root or old folders
                ids = folder.objectIds()
            for idx, id in enumerate(ids):
                rid = rids.get(id)
                if rid:
                    pos[rid] = idx
            return pos
        # otherwise the entire map needs to be constructed...
        for rid, container, id in items:
            if getattr(aq_base(container), "getObjectPosition", None):
                pos[rid] = container.getObjectPosition(id)
            else:
                # fallback for unordered folders
                pos[rid] = 0
        return pos


manage_addGopipForm = DTMLFile("dtml/addGopipIndex", globals())


def manage_addGopipIndex(self, identifier, REQUEST=None, RESPONSE=None, URL3=None):
    """add a fake gopip index"""
    return self.manage_addIndex(
        identifier, "GopipIndex", REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3
    )
