import os
import sys
import logging

import ROOT

class LeptonScales(object):
    '''Class to access the lepton scales for a given ID.'''

    def __init__(self):
        # EGamma POG
        self.egamma_pog_scales = {}
        self.egamma_pog_rootfiles = {}
        for cbid in ['Veto','Loose','Medium','Tight']:
            path = '{0}/src/DevTools/Analyzer/data/CutBasedID_{1}WP_76X_18Feb.txt_SF2D.root'.format(os.environ['CMSSW_BASE'],cbid)
            name = 'Cutbased{0}'.format(cbid)
            self.egamma_pog_rootfiles[name] = ROOT.TFile(path)
            self.egamma_pog_scales[name] = self.egamma_pog_rootfiles[name].Get('EGamma_SF2D')
        for wp in ['TrigWP80','TrigWP90']:
            path = '{0}/src/DevTools/Analyzer/data/ScaleFactor_GsfElectronToRECO_passing{1}.txt.egamma_SF2D.root'.format(os.environ['CMSSW_BASE'],wp)
            name = wp
            self.egamma_pog_rootfiles[name] = ROOT.TFile(path)
            self.egamma_pog_scales[name] = self.egamma_pog_rootfiles[name].Get('EGamma_SF2D')
        # Muon POG
        self.muon_pog_scales = {}
        idpath = '{0}/src/DevTools/Analyzer/data/MuonID_Z_RunCD_Reco76X_Feb15.root'.format(os.environ['CMSSW_BASE'])
        isopath = '{0}/src/DevTools/Analyzer/data/MuonIso_Z_RunCD_Reco76X_Feb15.root'.format(os.environ['CMSSW_BASE'])
        self.muon_pog_id_rootfile = ROOT.TFile(idpath)
        self.muon_pog_iso_rootfile = ROOT.TFile(isopath)
        for mid in ['LooseID','MediumID','SoftID','TightID']:
            idname = mid + 'andIPCut' if mid=='TightID' else mid
            self.muon_pog_scales[mid] = self.muon_pog_id_rootfile.Get('MC_NUM_{0}_DEN_genTracks_PAR_pt_spliteta_bin1/abseta_pt_ratio'.format(idname))
            for iso in ['LooseRelIso','TightRelIso']:
                if mid=='SoftID': continue
                if mid=='LooseID' and iso=='LooseRelIso': continue
                name = '{0}{1}'.format(iso,mid)
                self.muon_pog_scales[name] = self.muon_pog_iso_rootfile.Get('MC_NUM_{0}_DEN_{1}_PAR_pt_spliteta_bin1/abseta_pt_ratio'.format(iso,mid))

    def __exit__(self, type, value, traceback):
        self.__finish()

    def __del__(self):
        self.__finish()

    def __finish(self):
        for name,rootfile in self.egamma_pog_rootfiles.iteritems():
            rootfile.Close()
        self.muon_pog_id_rootfile.Close()
        self.muon_pog_iso_rootfile.Close()

    def __getElectronScale(self,rtrow,leptonId,cand):
        pt  = getattr(rtrow,'{0}_pt'.format(cand[0]))[cand[1]]
        eta = getattr(rtrow,'{0}_superClusterEta'.format(cand[0]))[cand[1]]
        if leptonId in self.egamma_pog_scales:
            if pt>200: pt = 199.
            if pt<10: pt = 11.
            if 'Trig' in leptonId and pt<15: pt = 16.
            hist = self.egamma_pog_scales[leptonId]
            val = hist.GetBinContent(hist.FindBin(abs(eta),pt))
        else:
            val = 1.
        return val

    def __getMuonScale(self,rtrow,leptonId,cand):
        pt  = getattr(rtrow,'{0}_pt'.format(cand[0]))[cand[1]]
        eta = getattr(rtrow,'{0}_eta'.format(cand[0]))[cand[1]]
        if leptonId in self.muon_pog_scales:
            if pt>120: pt = 119.
            if pt<20: pt = 21.
            hist = self.muon_pog_scales[leptonId]
            val = hist.GetBinContent(hist.FindBin(abs(eta),pt))
        else:
            val = 1.
        return val

    def __getTauScale(self,rtrow,leptonId,cand):
        #pt  = getattr(rtrow,'{0}_pt'.format(cand[0]))[cand[1]]
        #eta = getattr(rtrow,'{0}_eta'.format(cand[0]))[cand[1]]
        return 1. # simple recommendation, 6% error

    def getScale(self,rtrow,leptonId,cand):
        '''Get the scale to apply to MC (eff_data/eff_mc)'''
        if cand[0]=='electrons':
            val = self.__getElectronScale(rtrow,leptonId,cand)
        elif cand[0]=='muons':
            if leptonId == 'TightIDTightIso':
                idname, isoname = 'TightID', 'TightRelIsoTightID'
            elif leptonId == 'MediumIDTightIso':
                idname, isoname = 'MediumID', 'TightRelIsoMediumID'
            elif leptonId == 'MediumIDLooseIso':
                idname, isoname = 'MediumID', 'LooseRelIsoMediumID'
            else:
                idname, isoname = '', ''
            if idname and isoname:
                idval = self.__getMuonScale(rtrow,idname,cand)
                isoval = self.__getMuonScale(rtrow,isoname,cand)
            else:
                idval, isoval = 1., 1.
            val = idval*isoval
        elif cand[0]=='taus':
            val = self.__getTauScale(rtrow,leptonId,cand)
        else:
            val = 1.
        return val
