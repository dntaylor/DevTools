#!/usr/bin/env bash

# CMSSW packages

# electron smear corrections not yet availabel in 80X
#pushd $CMSSW_BASE/src
#git cms-merge-topic -u matteosan1:smearer_76X
git cms-merge-topic -u matteosan1:egm_tnp_80X
#popd

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
