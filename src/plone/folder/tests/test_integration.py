from unittest import defaultTestLoader
from plone.folder.tests.base import IntegrationTestCase
from plone.folder.tests.layer import IntegrationLayer
from plone.folder.content.base import BaseBTreeFolder


class FolderReplacementTests(IntegrationTestCase):

    layer = IntegrationLayer

    def afterSetUp(self):
        self.setRoles(['Manager'])

    def testCreateFolder(self):
        self.folder.invokeFactory('Folder', 'foo')
        self.failUnless(self.folder['foo'])
        self.assertEqual(self.folder['foo'].getPortalTypeName(), 'Folder')
        self.failUnless(isinstance(self.folder['foo'], BaseBTreeFolder))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
