import os
import sys
import logging
import math

import ROOT

import operator

class FakeRates(object):
    '''Class to access the fakerates for a given lepton ID.'''

    def __init__(self):
        self.fakehists = {'electrons':{},'muons':{},'taus':{}}
        self.fakekey = '{num}_{denom}'
        # WZ fakerates
        fake_path = '{0}/src/DevTools/Analyzer/data/fakerates_dijet_13TeV_Run2015D.root'.format(os.environ['CMSSW_BASE'])
        self.fake_rootfile = ROOT.TFile(fake_path)
        self.fakehists['electrons'][self.fakekey.format(num='WZMedium',denom='WZLoose')] = self.fake_rootfile.Get('e/medium/fakeratePtEta')
        self.fakehists['electrons'][self.fakekey.format(num='WZTight',denom='WZLoose')] = self.fake_rootfile.Get('e/tight/fakeratePtEta')
        self.fakehists['muons'][self.fakekey.format(num='WZMedium',denom='WZLoose')] = self.fake_rootfile.Get('m/medium/fakeratePtEta')
        self.fakehists['muons'][self.fakekey.format(num='WZTight',denom='WZLoose')] = self.fake_rootfile.Get('m/tight/fakeratePtEta')

    def __exit__(self, type, value, traceback):
        self.__finish()

    def __del__(self):
        self.__finish()

    def __finish(self):
        self.fake_rootfile.Close()

    def __get_fakerate(self,cand,pt,eta,num,denom):
        if cand[0] not in self.fakehists: return 0.
        key = self.fakekey.format(num=num,denom=denom)
        if key not in self.fakehists[cand[0]]: return 0.
        hist = self.fakehists[cand[0]][key]
        if pt > 100.: pt = 99.
        return hist.GetBinContent(hist.FindBin(pt,abs(eta)))

    def getFakeRate(self,rtrow,cand,num,denom):
        pt  = getattr(rtrow,'{0}_rochesterPt'.format(cand[0]))[cand[1]] if cand[0]=='muons' else getattr(rtrow,'{0}_pt'.format(cand[0]))[cand[1]]
        eta = getattr(rtrow,'{0}_rochesterEta'.format(cand[0]))[cand[1]] if cand[0]=='muons' else getattr(rtrow,'{0}_eta'.format(cand[0]))[cand[1]]
        return self.__get_fakerate(cand,pt,eta,num,denom)

