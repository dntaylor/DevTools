DevTools Package Description
============================

The DevTools package is a set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

```bash
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_9_2_3_patch1
cd CMSSW_9_2_3_patch1/src
cmsenv
git cms-init
git clone --recursive git@github.com:dntaylor/DevTools.git -b 92X
./DevTools/recipe/recipe.sh
``` 
