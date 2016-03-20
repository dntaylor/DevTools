# common utilities for analyzers

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

def getTestFile(type):
    if type=='MC':
        return '/store/user/dntaylor/2016-03-19_DevTools_76X_v1/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/2016-03-19_DevTools_76X_v1/160319_195847/0000/miniTree_1.root'
    elif type=='Data':
        return '/store/user/dntaylor/2016-03-19_DevTools_76X_v1/DoubleMuon/2016-03-19_DevTools_76X_v1/160319_200028/0000/miniTree_111.root'
    return ''
