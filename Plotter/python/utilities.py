# common utilities for plotting
import os
import sys
import errno

from DevTools.Analyzer.utilities import ZMASS

def python_mkdir(dir):
    '''A function to make a unix directory as well as subdirectories'''
    try:
        os.makedirs(dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else: raise

def isData(sample):
    '''Test if sample is data'''
    dataSamples = ['DoubleMuon','DoubleEG','MuonEG','SingleMuon','SingleElectron','Tau']
    return sample in dataSamples

def getLumi():
    '''Get the integrated luminosity to scale monte carlo'''
    #return 2263 # december jamboree golden json
    return 2318 # moriond golden json


latestNtuples = {
    'Hpp3l'          : '2016-03-21_Hpp3lAnalysis_v1',
    'Hpp4l'          : '2016-03-21_Hpp4lAnalysis_v1',
    'WZ'             : '2016-03-20_WZAnalysis_v1',
    'Electron'       : '2016-03-20_ElectronAnalysis_v2',
    'Muon'           : '2016-03-20_MuonAnalysis_v2',
    'SingleElectron' : '',
    'SingleMuon'     : '',
    'DijetFakeRate'  : '2016-03-20_DijetFakeRateAnalysis_v1',
}

def getNtupleDirectory(analysis):
    # first grad the local one
    ntupleDir = 'ntuples/{0}'.format(analysis)
    if os.path.exists(ntupleDir):
        return ntupleDir
    # if not read from hdfs
    baseDir = '/hdfs/store/user/dntaylor'
    if analysis in latestNtuples and latestNtuples[analysis]:
        return os.path.join(baseDir,latestNtuples[analysis])

treeMap = {
    'Electron'       : 'ETree',
    'Muon'           : 'MTree',
    'SingleElectron' : 'ETree',
    'SingleMuon'     : 'MTree',
    'WZ'             : 'WZTree',
    'Hpp3l'          : 'Hpp3lTree',
    'Hpp4l'          : 'Hpp4lTree',
    'DY'             : 'DYTree',
    'Charge'         : 'ChargeTree',
    'DijetFakeRate'  : 'DijetFakeRateTree',
}

def getTreeName(analysis):
    return treeMap[analysis] if analysis in treeMap else ''
