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

# nanoanalyzer
pushd $CMSSW_BASE/src/DevTools/NanoAnalyzer
git checkout master
git pull
popd

# ntuplizer
pushd $CMSSW_BASE/src/DevTools/Ntuplizer
git checkout 94X
git pull
popd

# tag and probe
pushd $CMSSW_BASE/src/DevTools/TagAndProbe
git checkout 92X
git pull
popd

