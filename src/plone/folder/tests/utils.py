# -*- coding: utf-8 -*-
from plone.folder.interfaces import IOrderable
from zope.interface import implementer


class DummyObject(object):

    def __init__(self, id, meta_type=None):
        self.id = id
        self.meta_type = meta_type

    def __of__(self, obj):
        return self

    def manage_fixupOwnershipAfterAdd(self):
        pass

    def dummy_method(self):
        return self.id


@implementer(IOrderable)
class Orderable(DummyObject):
    """ orderable mock object """


class Chaoticle(DummyObject):
    """ non-orderable mock object;  this does not implement `IOrderable` """
