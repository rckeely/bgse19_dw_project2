#!/bin/sh

cp *.py container/
cp -r assets container/
cp -r data container/
rm -rf container/configs
mkdir container/configs
