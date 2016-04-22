# common utilities for plotting
import os
import sys
import hashlib

from DevTools.Utilities.utilities import python_mkdir, ZMASS

def hashFile(*filenames,**kwargs):
    BUFFSIZE = kwargs.pop('BUFFSIZE',65536)
    hasher = hashlib.md5()
    for filename in filenames:
        with open(filename,'rb') as f:
            buff = f.read(BUFFSIZE)
            while len(buff)>0:
                hasher.update(buff)
                buff = f.read(BUFFSIZE)
    return hasher.hexdigest()

def hashString(*strings):
    hasher = hashlib.md5()
    for string in strings:
        hasher.update(string)
    return hasher.hexdigest()



def isData(sample):
    '''Test if sample is data'''
    dataSamples = ['DoubleMuon','DoubleEG','MuonEG','SingleMuon','SingleElectron','Tau']
    return sample in dataSamples

def getLumi():
    '''Get the integrated luminosity to scale monte carlo'''
    #return 2263 # december jamboree golden json
    return 2318 # moriond golden json


latestNtuples = {
    'Hpp3l'          : '',
    'Hpp4l'          : '',
    'WZ'             : '',
    'Electron'       : '2016-04-14_ElectronAnalysis_v1-merge',
    'Muon'           : '2016-04-14_MuonAnalysis_v1-merge',
    'Tau'            : '2016-04-14_TauAnalysis_v1-merge',
    'Charge'         : '',
    'TauCharge'      : '',
    'SingleElectron' : '',
    'SingleMuon'     : '',
    'DijetFakeRate'  : '',
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
    ''               : 'Tree',
    'Electron'       : 'ETree',
    'Muon'           : 'MTree',
    'Tau'            : 'TTree',
    'SingleElectron' : 'ETree',
    'SingleMuon'     : 'MTree',
    'WZ'             : 'WZTree',
    'Hpp3l'          : 'Hpp3lTree',
    'Hpp4l'          : 'Hpp4lTree',
    'DY'             : 'DYTree',
    'Charge'         : 'ChargeTree',
    'TauCharge'      : 'TauChargeTree',
    'DijetFakeRate'  : 'DijetFakeRateTree',
}

def getTreeName(analysis):
    return treeMap[analysis] if analysis in treeMap else ''
