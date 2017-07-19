DevTools Package Description
============================

The DevTools package is a simple set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

Current CMSSW version ``CMSSW_8_0_26_patch1``.

```bash
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src
cmsenv
git cms-init
scram b # necessary for EGamma MVA recipe
git clone --recursive git@github.com:dntaylor/DevTools.git -b 80X_PostICHEP
./DevTools/recipe/recipe.sh
``` 
