#!/usr/bin/env python
import os
import sys
import glob
import logging
import argparse
import re
from multiprocessing import Pool
from copy import deepcopy

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from DevTools.Plotter.histParams import getHistParams, getHistParams2D, getHistSelections
from DevTools.Plotter.utilities import getNtupleDirectory, getTreeName
from DevTools.Utilities.MultiProgress import MultiProgress
from DevTools.Plotter.FlattenTree import FlattenTree

try:
    from progressbar import ProgressBar, ETA, Percentage, Bar, SimpleProgress
    hasProgress = True
except:
    hasProgress = False

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def flatten(directory,**kwargs):
    sample = directory.split('/')[-1]
    if sample.endswith('.root'): sample = sample[:-5]
    analysis = kwargs.pop('analysis')
    histParams = kwargs.pop('histParams',{})
    histSelections = kwargs.pop('histSelections',{})
    if hasProgress:
        pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
    else:
        pbar = None

    #flattener = FlattenTree(
    #    ntupleDirectory=getNtupleDirectory(analysis),
    #    treeName=getTreeName(analysis),
    #)
    flattener = FlattenTree(analysis,sample)

    #flattener.initializeSample(sample,'flat/{0}/{1}.root'.format(analysis,sample))

    for histName, params in histParams.iteritems():
        flattener.addHistogram(histName,**params)

    for selName, sel in histSelections.iteritems():
        flattener.addSelection(selName,**sel['kwargs'])

    flattener.flattenAll(progressbar=pbar)

def getSampleDirectories(analysis,sampleList):
    source = getNtupleDirectory(analysis)
    directories = []
    for s in sampleList:
        for d in glob.glob(os.path.join(source,s)):
            directories += [d]
    return directories

def getSelectedHistParams(analysis,hists):
    allHistParams = getHistParams(analysis)
    if 'all' in hists: return allHistParams
    selectedHistParams = {}
    for h in hists:
        if h in allHistParams: selectedHistParams[h] = allHistParams[h]
    return selectedHistParams

def getSelectedHistSelections(analysis,sels,sample):
    allHistSelections = getHistSelections(analysis,sample)
    if 'all' in sels: return allHistSelections
    selectedHistSelections = {}
    for s in sels:
        if s in allHistSelections: selectedHistSelections[s] = allHistSelections[s]
    return selectedHistSelections

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Flatten Tree')

    parser.add_argument('analysis', type=str, choices=['WZ','DY','Charge','TauCharge','Hpp3l','Hpp4l','SingleElectron','SingleMuon','Electron','Muon','Tau','DijetFakeRate'], help='Analysis to process')
    parser.add_argument('--samples', nargs='+', type=str, default=['*'], help='Samples to flatten. Supports unix style wildcards.')
    parser.add_argument('--hists', nargs='+', type=str, default=['all'], help='Histograms to flatten.')
    parser.add_argument('--selections', nargs='+', type=str, default=['all'], help='Selections to flatten.')
    parser.add_argument('-j',type=int,default=16,help='Number of cores to use')

    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    logging.info('Preparing to flatten {0}'.format(args.analysis))

    directories = getSampleDirectories(args.analysis,args.samples)
    histParams = getSelectedHistParams(args.analysis,args.hists)

    logging.info('Will flatten {0} samples'.format(len(directories)))

    if args.j>1:
        multi = MultiProgress(args.j)
        for directory in directories:
            sample = directory.split('/')[-1]
            if sample.endswith('.root'): sample = sample[:-5]
            histSelections = getSelectedHistSelections(args.analysis,args.selections,sample)
            multi.addJob(sample,flatten,args=(directory,),kwargs={'analysis':args.analysis,'histParams':histParams,'histSelections':histSelections})
        multi.retrieve()
    else:
        for directory in directories:
            sample = directory.split('/')[-1]
            if sample.endswith('.root'): sample = sample[:-5]
            histSelections = getSelectedHistSelections(args.analysis,args.selections,sample)
            flatten(directory,
                    analysis=args.analysis,
                    histParams=histParams,
                    histSelections=histSelections,
                    )

    logging.info('Finished')

if __name__ == "__main__":
    status = main()
    sys.exit(status)

