#!/usr/bin/env bash

# submodules

# utilities
pushd $CMSSW_BASE/src/DevTools/Utilities
git checkout master
git pull
popd

# limits
pushd $CMSSW_BASE/src/DevTools/Limits
git checkout master
git pull
popd

# plotter
pushd $CMSSW_BASE/src/DevTools/Plotter
git checkout master
git pull
popd

# analyzer
pushd $CMSSW_BASE/src/DevTools/Analyzer
git checkout master
git pull
popd

# ntuplizer
pushd $CMSSW_BASE/src/DevTools/Ntuplizer
git checkout 80X_PostICHEP
git pull
popd
source $CMSSW_BASE/src/DevTools/Ntuplizer/recipe/recipe.sh

# tag and probe
pushd $CMSSW_BASE/src/DevTools/TagAndProbe
git checkout 80X_PostICHEP
git pull
popd
source $CMSSW_BASE/src/DevTools/TagAndProbe/recipe/recipe.sh

# python utilities
git clone --branch 15.0.0 https://github.com/pypa/virtualenv.git $CMSSW_BASE/src/DevTools/recipe/virtualenv
pushd $CMSSW_BASE/src/DevTools/recipe/virtualenv
python virtualenv.py $CMSSW_BASE/src/venv
popd

export VIRTUAL_ENV_DISABLE_PROMPT=1
source $CMSSW_BASE/src/venv/bin/activate
export PYTHONPATH=$CMSSW_BASE/src/venv/lib/python2.7/site-packages/:$PYTHONPATH

pip install -U pip      # new version
pip install -U ipython  # doesnt have the backspace problem in 80X
pip install progressbar # nice progressbars
pip install blessings   # simple terminal styling
pip install jupyter     # ipython notebook
pip install brilws      # for brilcalc
