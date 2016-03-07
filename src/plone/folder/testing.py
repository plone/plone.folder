# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import plone.folder


class PloneFolderLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=plone.folder)


PLONEFOLDER_FIXTURE = PloneFolderLayer()

PLONEFOLDER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEFOLDER_FIXTURE,),
    name='PloneFolderLayer:IntegrationTesting'
)

PLONEFOLDER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEFOLDER_FIXTURE,),
    name='PloneFolderLayer:FunctionalTesting'
)
