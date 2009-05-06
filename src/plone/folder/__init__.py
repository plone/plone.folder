from Products.CMFCore.permissions import setDefaultRoles


packageName = __name__

AddFolder = 'ATContentTypes: Add Folder'
setDefaultRoles(AddFolder, ('Manager', 'Owner',))


def initialize(context):
    """ initializer called when used as a zope2 product """

    from Products.Archetypes import atapi
    from Products.CMFCore import utils

    from plone.folder.content import folder
    folder.__name__    # make pyflakes happy...

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(packageName), packageName)

    assert len(content_types) == 1, 'only a new folder, please!'

    for atype, constructor, fti in zip(content_types, constructors, ftis):
        utils.ContentInit('%s: %s' % (packageName, atype.portal_type),
            content_types = (atype,),
            permission = AddFolder,
            extra_constructors = (constructor,),
            fti = (fti,),
            ).initialize(context)
