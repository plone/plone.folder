from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc


ptc.setupPloneSite()


class IntegrationTestCase(ptc.PloneTestCase):
    """ base class for integration tests """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            user = ptc.default_user
            pwd = ptc.default_password
            browser.addHeader('Authorization', 'Basic %s:%s' % (user, pwd))
        return browser
