DevTools Package Description
============================

The DevTools package is a set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

```bash
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src
cmsenv
git cms-init
git clone --recursive git@github.com:dntaylor/DevTools.git -b 81X_combine
./DevTools/recipe/recipe.sh
``` 
