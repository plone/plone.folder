#!/bin/bash

cd $( dirname $0 )
bin/instance test --nowarn -s Products.CMFPlone
bin/instance test --nowarn -s Products.ATContentTypes
bin/instance test --nowarn -s Products.Archetypes
