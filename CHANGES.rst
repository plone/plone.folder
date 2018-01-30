Changelog
=========


1.0.10 (2018-01-30)
-------------------

Bug fixes:

- Add Python 2 / 3 compatibility
  [vincero]


1.0.9 (2016-08-08)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


1.0.8 (2016-04-26)
------------------

Fixes:

- Update testing layers to use best practices and remove ZopeTestCase dependency,
  which should fix its test isolation problems.
  [gforcada]


1.0.7 (2015-07-29)
------------------

- Depend on ``Products.CMFCore`` and remove fake-cmf, because this confuses
  more than it helps to reduce complexcity.
  [jensens]

- Cleanup: PEP8 and do not use ``id`` built-in as identifier.
  [jensens]


1.0.6 (2015-05-11)
------------------

- Whitespace cleanup, git ignores, cleanup package info.
  [gforcada, rnixx, maurits]


1.0.5 (2013-12-07)
------------------

- Allow reversing the current order, without specifying a key for
  sorting.
  [maurits]

- Allow ordering by a method instead of an attribute.
  [maurits]


1.0.4 (2012-08-30)
------------------

- Update manifest.in to fix packaging error.
  [esteele]


1.0.3 (2012-08-29)
------------------

- In setup.py, name more dependencies explicitly.
  [thet]


1.0.2 (2012-07-02)
------------------

- Update notifyContainerModified import location.
  [hannosch]

- Add MANIFEST.in.
  [WouterVH]


1.0.1 - 2010-08-08
------------------

- Added objectValues and objectItems method to the ordered folder
  implementation, which use objectIds and thus the ordering information. In
  Zope 2.13 BTreeFolder2 was optimized to loop over the internal _tree data
  structure avoiding the objectIds indirection.
  [hannosch]


1.0 - 2010-07-18
----------------

- Avoid dangerous memoization in the DefaultOrdering adapter.
  [hannosch]

- Update license to GPL version 2 only.
  [hannosch]


1.0b5 - 2010-03-06
------------------

- Remove support for setting ``__parent__`` and ``__name__`` for content
  providing ``IContained`` as it can cause severe performance issues when
  used on Zope 2.x.
  [witsch]


1.0b4 - 2010-02-17
------------------

- Register all ordering adapter by default now that they can co-exist.
  [witsch]

- Add `__getitem__` support to the default ordering adapter to help
  previous/next support in `plone.app.folder`.
  [witsch]


1.0b3 - 2010-02-09
------------------

- Make sure order changes are persisted when using the partial ordering
  adapter.
  [hannosch, witsch]


1.0b2 - 2010-01-28
------------------

- Make the dependency on `Products.CMFCore` a soft one.
  [witsch]

- Added an 'unordered' adapter which can be used when no explicit ordering
  is needed.
  [davisagli]

- Allow the use of different named adapters to ``IOrdering``, with the name
  determined by the folder's ``_ordering`` attribute.
  [davisagli]


1.0b1 - 2009-10-10
------------------

- Fix the WebDAV content creation process by properly returning a
  ``NullResource`` when required.
  [optilude]


1.0a3 - 2009-05-11
------------------

- Let ``objectIds`` always return all object ids, even with partial ordering.
  [witsch]


1.0a2 - 2009-05-07
------------------

- Fix a bug in the default ordering that would cause the ``pos`` dict to get
  out of sync when an item is deleted.
  [optilude]

- Declare ``IContainer`` support.
  [optilude]

- Properly set ``__parent__`` and ``__name__`` for ``IContained`` in
  ``_setOb()``.
  [optilude]

- Add ``__getitem__``, needed when not using the CMF mix-in.
  [optilude]

- Added ``__setitem__``, ``__contains__`` and ``__delitem__`` to support a
  dict-like API.
  [optilude]

- Fix issue with removing non-orderable content for partial ordering suppport.
  [witsch]

- Fix ``getObjectPosition`` to return a value representing "no position" for
  non-orderable content instead of raising an error.
  [witsch]

- Fix boolean value of the btree-based folder base class.
  [witsch]

- Factor CMF out of the base classes for the new btree-based folder class
  and simplify things a bit afterwards.
  [witsch]

- Add adapter providing explicit ordering only for "orderable" content.
  [witsch]

- Clean up tests and their setup.
  [witsch]


1.0a1 - 2008-05-27
------------------

- Initial release
  [optilude, tesdal, witsch]
