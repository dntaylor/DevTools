DevTools Package Description
============================

The DevTools package is a simple set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

Current CMSSW version ``CMSSW_7_6_3_patch2``.

```bash
cmsrel CMSSW_7_6_3_patch2
cd CMSSW_7_6_3_patch2/src
cmsenv
git cms-init
git clone --recursive git@github.com:dntaylor/DevTools.git -b 76X
./DevTools/recipe/recipe.sh
``` 
