DevTools Package Description
============================

The DevTools package is a set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_1
cd CMSSW_10_6_1/src
cmsenv
git cms-init
scram b # need for EGamma recipes
git clone --recursive git@github.com:dntaylor/DevTools.git -b 106X
./DevTools/recipe/recipe.sh
scram b -j 16
``` 
