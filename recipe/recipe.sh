#!/usr/bin/env bash

# recipes for sub modules

# ntuplizer
source $CMSSW_BASE/src/DevTools/Ntuplizer/recipe/recipe.sh

# tag and probe
source $CMSSW_BASE/src/DevTools/TagAndProbe/recipe/recipe.sh

# python utilities
git clone --branch 15.0.0 https://github.com/pypa/virtualenv.git $CMSSW_BASE/src/DevTools/recipe/virtualenv
pushd $CMSSW_BASE/src/DevTools/recipe/virtualenv
python virtualenv.py $CMSSW_BASE/src/venv
popd

export VIRTUAL_ENV_DISABLE_PROMPT=1
source $CMSSW_BASE/src/venv/bin/activate
export PYTHONPATH=$CMSSW_BASE/src/venv/lib/python2.7/site-packages/:$PYTHONPATH

pip install progressbar # nice progressbars
pip install blessings   # simple terminal styling
pip install jupyter     # ipython notebook
pip install brilws      # brilcalc
