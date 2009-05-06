from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from plone.folder.tests.layer import IntegrationLayer


ptc.setupPloneSite()


class PloneFolderLayer(PloneSite):
    """ layer for plone integration tests """


class IntegrationTestCase(ptc.PloneTestCase):
    """ base class for integration tests """

    layer = IntegrationLayer


class FunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    layer = IntegrationLayer

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            user = ptc.default_user
            pwd = ptc.default_password
            browser.addHeader('Authorization', 'Basic %s:%s' % (user, pwd))
        return browser
