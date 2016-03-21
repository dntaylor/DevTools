# common utilities for analyzers
import os
import sys
import ROOT

ZMASS = 91.1876

def deltaPhi(phi0,phi1):
    result = phi0-phi1
    while result>ROOT.TMath.Pi():
        result -= 2*ROOT.TMath.Pi()
    while result<=-ROOT.TMath.Pi():
        result += 2*ROOT.TMath.Pi()
    return result

def deltaR(eta0,phi0,eta1,phi1):
    deta = eta0-eta1
    dphi = deltaPhi(phi0,phi1)
    return ROOT.TMath.Sqrt(deta**2+dphi**2)

latestNtuples = {
    'DevTools' : '2016-03-19_DevTools_76X_v1',
}

def getNtupleDirectory(analysis):
    baseDir = '/hdfs/store/user/dntaylor'
    if analysis in latestNtuples and latestNtuples[analysis]:
        return os.path.join(baseDir,latestNtuples[analysis])

def getTestFile(type):
    if type=='MC':
        return '/store/user/dntaylor/2016-03-19_DevTools_76X_v1/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/2016-03-19_DevTools_76X_v1/160319_195847/0000/miniTree_1.root'
    elif type=='Data':
        return '/store/user/dntaylor/2016-03-19_DevTools_76X_v1/DoubleMuon/2016-03-19_DevTools_76X_v1/160319_200028/0000/miniTree_111.root'
    elif type=='hpp':
        return '/store/user/dntaylor/2016-03-19_DevTools_76X_v1/HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8/2016-03-19_DevTools_76X_v1/160320_073839/0000/miniTree_1.root'
    else:
        return ''
