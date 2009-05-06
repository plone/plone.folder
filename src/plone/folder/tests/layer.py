from zope.component import provideAdapter

from Testing.ZopeTestCase import app, close, installPackage
from Products.Five import fiveconfigure
from Products.Five.zcml import load_config
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.layer import PloneSite
from transaction import commit

from zope.annotation.attribute import AttributeAnnotations
from plone.folder.default import DefaultOrdering
from plone.folder.partial import PartialOrdering


class PloneFolderLayer:

    @classmethod
    def setUp(cls):
        provideAdapter(DefaultOrdering)
        provideAdapter(AttributeAnnotations)

    @classmethod
    def tearDown(cls):
        pass


class PartialOrderingLayer:

    @classmethod
    def setUp(cls):
        provideAdapter(PartialOrdering)

    @classmethod
    def tearDown(cls):
        pass


class IntegrationLayer(PloneSite):
    """ layer for integration tests using the folder replacement type """

    @classmethod
    def setUp(cls):
        root = app()
        portal = root.plone
        # load zcml & install the package
        fiveconfigure.debug_mode = True
        import plone.folder
        load_config('configure.zcml', plone.folder)
        fiveconfigure.debug_mode = False
        installPackage('plone.folder', quiet=True)
        # import replacement profile
        profile = 'profile-plone.folder:default'
        tool = getToolByName(portal, 'portal_setup')
        tool.runAllImportStepsFromProfile(profile, purge_old=False)
        # make sure it's loaded...
        types = getToolByName(portal, 'portal_types')
        assert types.getTypeInfo('Folder').product == 'plone.folder'
        # and commit the changes
        commit()
        close(root)

    @classmethod
    def tearDown(cls):
        pass


class PartialOrderingIntegrationLayer(IntegrationLayer):
    """ layer for integration tests using the partial ordering adapter """

    @classmethod
    def setUp(cls):
        provideAdapter(PartialOrdering)

    @classmethod
    def tearDown(cls):
        pass
