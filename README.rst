plone.folder
============

Overview
--------

This package provides a base class for folderish content types based on `B-trees`_,
a.k.a. "large folders" in Plone_.
Storing content in such folders provides significant `performance benefits`_ over regular folders.
However, "large folders" do not support explicit ordering of their contents out-of-the box.
That is, you cannot manually specify the order of items within the folder,
you can only sort things according to a given criteria after fetching items from the folder.

  .. _`B-tree`: http://en.wikipedia.org/wiki/B-tree
  .. _`B-trees`: http://en.wikipedia.org/wiki/B-tree
  .. _`Plone`: http://plone.org/
  .. _`performance benefits`: http://plone.org/products/plone/roadmap/191
  .. |---| unicode:: U+2014  .. em dash

Many times, though, it is desirable to be able to explicitly order a folder's content,
for example for items that are related to site navigation.
Sorting alphabetically often doesn't make sense here.

To compensate ``plone.folder`` provides ordering support for `B-tree`_ folders via the above mentioned base class,
which can make use of an adapter to store the actual order information.
It also comes with two sample adapter implementations:

* A default adapter handling order information for all objects contained in a folder.
  This adapter can be used to build fully backwards-compatible drop-in replacements for folderish content.
  In other words, when using this adapter `B-tree`_-based folders should behave just like the "regular" folder implementation,
  but provide some of the performance benefits at the same time.

* An alternative adapter implementation that is targeted towards sites with only a relatively small percentage of content for which (explicit) order matters.
  It'll only manage order information for certain content types (via a marker interface).

The latter allows to not having to separate such content from "non-orderable" content.
Up to now many large sites ended up storing "orderable" items |---|
for example everything related to navigation and typically only a few |---|
in regular folders and the bulk of the content in "large" folders,
most of the time solely for performance reasons.
This adapter will hopefully help avoid having to make this distinction in the future
and still provide the better performance characteristics of `B-tree`_ folders.

Source Code
===========

Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.folder>`_.
