DevTools Package Description
============================

The DevTools package is a simple set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

Current CMSSW version ``CMSSW_8_0_25``.

```bash
cmsrel CMSSW_8_0_25
cd CMSSW_8_0_25/src
cmsenv
git cms-init
scram b # necessary for EGamma MVA recipe
git clone --recursive git@github.com:dntaylor/DevTools.git -b 80X_PostICHEP
./DevTools/recipe/recipe.sh
``` 
