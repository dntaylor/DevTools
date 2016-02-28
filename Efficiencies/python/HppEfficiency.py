# HppEfficiency.pu

from Efficiency import Efficiency

import ROOT

class HppEfficiency(Efficiency):
    '''
    Efficiency for H++
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','hppEfficiency.root')
        super(HppEfficiency, self).__init__(outputFileName=outputFileName,**kwargs)

        # setup histograms
        self.addEfficiency('electron_cbidVeto',      [100,0,500])
        self.addEfficiency('electron_cbidLoose',     [100,0,500])
        self.addEfficiency('electron_cbidMedium',    [100,0,500])
        self.addEfficiency('electron_cbidTight',     [100,0,500])
        self.addEfficiency('electron_wzLoose',       [100,0,500])
        self.addEfficiency('electron_wzMedium',      [100,0,500])
        self.addEfficiency('electron_wzTight',       [100,0,500])
        self.addEfficiency('electron_heepV60',       [100,0,500])
        self.addEfficiency('electron_mvaNonTrigWP80',[100,0,500])
        self.addEfficiency('electron_mvaNonTrigWP90',[100,0,500])
        self.addEfficiency('electron_mvaTrigPre',    [100,0,500])
        self.addEfficiency('electron_mvaTrigWP80',   [100,0,500])
        self.addEfficiency('electron_mvaTrigWP90',   [100,0,500])
        self.addEfficiency('muon_loose',             [100,0,500])
        self.addEfficiency('muon_medium',            [100,0,500])
        self.addEfficiency('muon_tight',             [100,0,500])
        self.addEfficiency('muon_highPt',            [100,0,500])
        self.addEfficiency('muon_loose_tightiso',    [100,0,500])
        self.addEfficiency('muon_medium_tightiso',   [100,0,500])
        self.addEfficiency('muon_tight_tightiso',    [100,0,500])
        self.addEfficiency('muon_highPt_tightiso',   [100,0,500])
        self.addEfficiency('muon_wzLoose',           [100,0,500])
        self.addEfficiency('muon_wzMedium',          [100,0,500])

        # add variables
        self.addVariable('electron_pt_barrel',             [100,0,500])
        self.addVariable('electron_pt_endcap',             [100,0,500])
        self.addVariable('electron_sigmaIEtaIEta_barrel',  [100,0,0.05])
        self.addVariable('electron_sigmaIEtaIEta_endcap',  [100,0,0.05])
        self.addVariable('electron_absDEtaIn_barrel',      [100,0,0.02])
        self.addVariable('electron_absDEtaIn_endcap',      [100,0,0.02])
        self.addVariable('electron_absDPhiIn_barrel',      [100,0,0.25])
        self.addVariable('electron_absDPhiIn_endcap',      [100,0,0.25])
        self.addVariable('electron_hOverE_barrel',         [100,0,0.25])
        self.addVariable('electron_hOverE_endcap',         [100,0,0.25])
        self.addVariable('electron_relIsoEA_barrel',       [100,0,0.25])
        self.addVariable('electron_relIsoEA_endcap',       [100,0,0.25])
        self.addVariable('electron_ooEmooP_barrel',        [100,0,0.3])
        self.addVariable('electron_ooEmooP_endcap',        [100,0,0.3])
        self.addVariable('electron_absDxy_barrel',         [100,0,0.3])
        self.addVariable('electron_absDxy_endcap',         [100,0,0.3])
        self.addVariable('electron_absDz_barrel',          [100,0,1.0])
        self.addVariable('electron_absDz_endcap',          [100,0,1.0])
        self.addVariable('electron_missingHits_barrel',    [5,0,5])
        self.addVariable('electron_missingHits_endcap',    [5,0,5])
        self.addVariable('electron_conversionVeto_barrel', [2,0,2])
        self.addVariable('electron_conversionVeto_endcap', [2,0,2])

    def fill(self,rtrow):
        # first electrons
        for i in xrange(rtrow.electrons_count):
            # match to gen particle
            if self.getObjectVariable(rtrow,('electrons',i),'genMatch')<0.5: continue
            if self.getObjectVariable(rtrow,('electrons',i),'genStatus')!=1: continue
            if self.getObjectVariable(rtrow,('electrons',i),'genIsPrompt')<0.5: continue
            # get ids
            pt = self.getObjectVariable(rtrow,('electrons',i),'pt')
            passCutBasedVeto   = self.getObjectVariable(rtrow,('electrons',i),'cutBasedVeto') > 0.5
            passCutBasedLoose  = self.getObjectVariable(rtrow,('electrons',i),'cutBasedLoose') > 0.5
            passCutBasedMedium = self.getObjectVariable(rtrow,('electrons',i),'cutBasedMedium') > 0.5
            passCutBasedTight  = self.getObjectVariable(rtrow,('electrons',i),'cutBasedTight') > 0.5
            passWWLoose        = self.getObjectVariable(rtrow,('electrons',i),'wwLoose') > 0.5
            passHEEPV60        = self.getObjectVariable(rtrow,('electrons',i),'heepV60') > 0.5
            passMVANonTrigWP80 = self.getObjectVariable(rtrow,('electrons',i),'mvaNonTrigWP80') > 0.5
            passMVANonTrigWP90 = self.getObjectVariable(rtrow,('electrons',i),'mvaNonTrigWP90') > 0.5
            passMVATrigWP80    = self.getObjectVariable(rtrow,('electrons',i),'mvaTrigWP80') > 0.5
            passMVATrigWP90    = self.getObjectVariable(rtrow,('electrons',i),'mvaTrigWP90') > 0.5
            # require MVA trig preselection
            sceta = self.getObjectVariable(rtrow,('electrons',i),'superClusterEta')
            sigmaIEtaIEta = self.getObjectVariable(rtrow,('electrons',i),'sigmaIetaIeta')
            hcalOverEcal = self.getObjectVariable(rtrow,('electrons',i),'hcalOverEcal')
            ecalRelIso = self.getObjectVariable(rtrow,('electrons',i),'dr03EcalRecHitSumEt')/pt
            hcalRelIso = self.getObjectVariable(rtrow,('electrons',i),'dr03HcalTowerSumEt')/pt
            trackRelIso = self.getObjectVariable(rtrow,('electrons',i),'dr03TkSumPt')/pt
            dEtaSC = self.getObjectVariable(rtrow,('electrons',i),'deltaEtaSuperClusterTrackAtVtx')
            dPhiSC = self.getObjectVariable(rtrow,('electrons',i),'deltaPhiSuperClusterTrackAtVtx')
            relIsoRho = self.getObjectVariable(rtrow,('electrons',i),'relPFIsoRhoR03')
            passConversion = self.getObjectVariable(rtrow,('electrons',i),'passConversionVeto')
            dxy = self.getObjectVariable(rtrow,('electrons',i),'dxy')
            dz = self.getObjectVariable(rtrow,('electrons',i),'dz')
            ecalEnergy = self.getObjectVariable(rtrow,('electrons',i),'ecalEnergy')
            eSuperClusterOverP = self.getObjectVariable(rtrow,('electrons',i),'eSuperClusterOverP')
            ooEmooP = abs((1.-eSuperClusterOverP)*1./ecalEnergy)
            passMVATrigPre = True
            if pt<15: passMVATrigPre = False
            if sceta<1.479:
                if sigmaIEtaIEta>0.012: passMVATrigPre = False
                if hcalOverEcal>0.09:   passMVATrigPre = False
                if ecalRelIso>0.37:     passMVATrigPre = False
                if hcalRelIso>0.25:     passMVATrigPre = False
                if trackRelIso>0.18:    passMVATrigPre = False
                if abs(dEtaSC)>0.0095:  passMVATrigPre = False
                if abs(dPhiSC)>0.065:   passMVATrigPre = False
                self.fillVariable('electron_pt_barrel',pt)
                self.fillVariable('electron_sigmaIEtaIEta_barrel',sigmaIEtaIEta)
                self.fillVariable('electron_absDEtaIn_barrel',abs(dEtaSC))
                self.fillVariable('electron_absDPhiIn_barrel',abs(dPhiSC))
                self.fillVariable('electron_hOverE_barrel',hcalOverEcal)
                self.fillVariable('electron_relIsoEA_barrel',relIsoRho)
                self.fillVariable('electron_ooEmooP_barrel',ooEmooP)
                self.fillVariable('electron_absDxy_barrel',abs(dxy))
                self.fillVariable('electron_absDz_barrel',abs(dz))
                self.fillVariable('electron_conversionVeto_barrel',passConversion)
            else:
                if sigmaIEtaIEta>0.033: passMVATrigPre = False
                if hcalOverEcal>0.09:   passMVATrigPre = False
                if ecalRelIso>0.45:     passMVATrigPre = False
                if hcalRelIso>0.28:     passMVATrigPre = False
                if trackRelIso>0.18:    passMVATrigPre = False
                self.fillVariable('electron_pt_endcap',pt)
                self.fillVariable('electron_sigmaIEtaIEta_endcap',sigmaIEtaIEta)
                self.fillVariable('electron_absDEtaIn_endcap',abs(dEtaSC))
                self.fillVariable('electron_absDPhiIn_endcap',abs(dPhiSC))
                self.fillVariable('electron_hOverE_endcap',hcalOverEcal)
                self.fillVariable('electron_relIsoEA_endcap',relIsoRho)
                self.fillVariable('electron_ooEmooP_endcap',ooEmooP)
                self.fillVariable('electron_absDxy_endcap',abs(dxy))
                self.fillVariable('electron_absDz_endcap',abs(dz))
                self.fillVariable('electron_conversionVeto_endcap',passConversion)
            # fill efficiencies
            self.fillEfficiency('electron_cbidVeto',pt,passCutBasedVeto)
            self.fillEfficiency('electron_cbidLoose',pt,passCutBasedLoose)
            self.fillEfficiency('electron_cbidMedium',pt,passCutBasedMedium)
            self.fillEfficiency('electron_cbidTight',pt,passCutBasedTight)
            self.fillEfficiency('electron_wzLoose',pt,passWWLoose)
            self.fillEfficiency('electron_wzMedium',pt,passCutBasedMedium and passWWLoose)
            self.fillEfficiency('electron_wzTight',pt,passCutBasedTight and passWWLoose)
            self.fillEfficiency('electron_heepV60',pt,passHEEPV60)
            self.fillEfficiency('electron_mvaNonTrigWP80',pt,passMVANonTrigWP80)
            self.fillEfficiency('electron_mvaNonTrigWP90',pt,passMVANonTrigWP90)
            self.fillEfficiency('electron_mvaTrigPre',pt,passMVATrigPre)
            self.fillEfficiency('electron_mvaTrigWP80',pt,passMVATrigWP80 and passMVATrigPre)
            self.fillEfficiency('electron_mvaTrigWP90',pt,passMVATrigWP90 and passMVATrigPre)
        # next muons
        for i in xrange(rtrow.muons_count):
            # match to gen particle
            if self.getObjectVariable(rtrow,('muons',i),'genMatch')<0.5: continue
            if self.getObjectVariable(rtrow,('muons',i),'genStatus')!=1: continue
            if self.getObjectVariable(rtrow,('muons',i),'genIsPrompt')<0.5: continue
            # get ids
            pt = self.getObjectVariable(rtrow,('muons',i),'pt')
            iso = self.getObjectVariable(rtrow,('muons',i),'relPFIsoDeltaBetaR04')
            trackRelIso = self.getObjectVariable(rtrow,('muons',i),'trackIso')/pt
            dz = self.getObjectVariable(rtrow,('muons',i),'dz')
            dxy = self.getObjectVariable(rtrow,('muons',i),'dxy')
            passLoose  = self.getObjectVariable(rtrow,('muons',i),'isLooseMuon') > 0.5
            passMedium = self.getObjectVariable(rtrow,('muons',i),'isMediumMuon') > 0.5
            passTight  = self.getObjectVariable(rtrow,('muons',i),'isTightMuon') > 0.5
            passHighPt = self.getObjectVariable(rtrow,('muons',i),'isHighPtMuon') > 0.5
            # fill efficiencies
            self.fillEfficiency('muon_loose',pt,passLoose)
            self.fillEfficiency('muon_medium',pt,passMedium)
            self.fillEfficiency('muon_tight',pt,passTight)
            self.fillEfficiency('muon_highPt',pt,passHighPt)
            self.fillEfficiency('muon_loose_tightiso',pt,passLoose and iso<0.15)
            self.fillEfficiency('muon_medium_tightiso',pt,passMedium and iso<0.15)
            self.fillEfficiency('muon_tight_tightiso',pt,passTight and iso<0.15)
            self.fillEfficiency('muon_highPt_tightiso',pt,passHighPt and iso<0.15)
            self.fillEfficiency('muon_wzLoose',pt,passMedium and iso<0.4 and trackRelIso<0.4)
            self.fillEfficiency('muon_wzMedium',pt,passMedium and iso<0.15 and trackRelIso<0.4 and dz<0.1 and (dxy<0.01 if pt<20 else dxy<0.02))

