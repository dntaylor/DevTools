#!/usr/bin/env bash

# submodules
source $CMSSW_BASE/src/DevTools/recipe/setupSubmodules.sh
#source $CMSSW_BASE/src/DevTools/Ntuplizer/recipe/recipe.sh
#source $CMSSW_BASE/src/DevTools/TagAndProbe/recipe/recipe.sh

# install combine
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
pushd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.1
popd

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
