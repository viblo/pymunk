#!/bin/bash
set -e

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update
    brew install python;
    brew install python3;
    PATH=/usr/local/bin:$PATH;
fi; 
