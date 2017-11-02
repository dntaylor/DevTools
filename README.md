DevTools Package Description
============================

The DevTools package is a set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

```bash
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_9_4_0_pre3
cd CMSSW_9_4_0_pre3/src
cmsenv
git cms-init
git clone --recursive git@github.com:dntaylor/DevTools.git -b 94X
./DevTools/recipe/recipe.sh
``` 
