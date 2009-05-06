#!/bin/bash

cd $( dirname $0 )
cat test-patches/* | patch -Nsp0
bin/instance test --nowarn -s Products.CMFPlone
bin/instance test --nowarn -s Products.ATContentTypes
bin/instance test --nowarn -s Products.Archetypes
cat test-patches/* | patch -Rsp0
find extras/ -name \*.orig | xargs rm
