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
        # electrons
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

        # fake (not matched to gen prompt electron)
        self.addEfficiency('electron_cbidVeto_fake',      [100,0,500])
        self.addEfficiency('electron_cbidLoose_fake',     [100,0,500])
        self.addEfficiency('electron_cbidMedium_fake',    [100,0,500])
        self.addEfficiency('electron_cbidTight_fake',     [100,0,500])
        self.addEfficiency('electron_wzLoose_fake',       [100,0,500])
        self.addEfficiency('electron_wzMedium_fake',      [100,0,500])
        self.addEfficiency('electron_wzTight_fake',       [100,0,500])
        self.addEfficiency('electron_heepV60_fake',       [100,0,500])
        self.addEfficiency('electron_mvaNonTrigWP80_fake',[100,0,500])
        self.addEfficiency('electron_mvaNonTrigWP90_fake',[100,0,500])
        self.addEfficiency('electron_mvaTrigPre_fake',    [100,0,500])
        self.addEfficiency('electron_mvaTrigWP80_fake',   [100,0,500])
        self.addEfficiency('electron_mvaTrigWP90_fake',   [100,0,500])

        # matched to hadron 
        self.addEfficiency('electron_cbidVeto_jet',      [100,0,500])
        self.addEfficiency('electron_cbidLoose_jet',     [100,0,500])
        self.addEfficiency('electron_cbidMedium_jet',    [100,0,500])
        self.addEfficiency('electron_cbidTight_jet',     [100,0,500])
        self.addEfficiency('electron_wzLoose_jet',       [100,0,500])
        self.addEfficiency('electron_wzMedium_jet',      [100,0,500])
        self.addEfficiency('electron_wzTight_jet',       [100,0,500])
        self.addEfficiency('electron_heepV60_jet',       [100,0,500])
        self.addEfficiency('electron_mvaNonTrigWP80_jet',[100,0,500])
        self.addEfficiency('electron_mvaNonTrigWP90_jet',[100,0,500])
        self.addEfficiency('electron_mvaTrigPre_jet',    [100,0,500])
        self.addEfficiency('electron_mvaTrigWP80_jet',   [100,0,500])
        self.addEfficiency('electron_mvaTrigWP90_jet',   [100,0,500])

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
        self.addVariable('electron_absDz_barrel',          [100,0,0.5])
        self.addVariable('electron_absDz_endcap',          [100,0,0.5])
        self.addVariable('electron_missingHits_barrel',    [5,0,5])
        self.addVariable('electron_missingHits_endcap',    [5,0,5])
        self.addVariable('electron_conversionVeto_barrel', [2,0,2])
        self.addVariable('electron_conversionVeto_endcap', [2,0,2])

        # muons
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

        # not matched to gen prompt muon
        self.addEfficiency('muon_loose_fake',             [100,0,500])
        self.addEfficiency('muon_medium_fake',            [100,0,500])
        self.addEfficiency('muon_tight_fake',             [100,0,500])
        self.addEfficiency('muon_highPt_fake',            [100,0,500])
        self.addEfficiency('muon_loose_tightiso_fake',    [100,0,500])
        self.addEfficiency('muon_medium_tightiso_fake',   [100,0,500])
        self.addEfficiency('muon_tight_tightiso_fake',    [100,0,500])
        self.addEfficiency('muon_highPt_tightiso_fake',   [100,0,500])
        self.addEfficiency('muon_wzLoose_fake',           [100,0,500])
        self.addEfficiency('muon_wzMedium_fake',          [100,0,500])

        # matched to gen decay from hadron
        self.addEfficiency('muon_loose_jet',             [100,0,500])
        self.addEfficiency('muon_medium_jet',            [100,0,500])
        self.addEfficiency('muon_tight_jet',             [100,0,500])
        self.addEfficiency('muon_highPt_jet',            [100,0,500])
        self.addEfficiency('muon_loose_tightiso_jet',    [100,0,500])
        self.addEfficiency('muon_medium_tightiso_jet',   [100,0,500])
        self.addEfficiency('muon_tight_tightiso_jet',    [100,0,500])
        self.addEfficiency('muon_highPt_tightiso_jet',   [100,0,500])
        self.addEfficiency('muon_wzLoose_jet',           [100,0,500])
        self.addEfficiency('muon_wzMedium_jet',          [100,0,500])

        # add variables
        self.addVariable('muon_pt',           [100,0,500])
        self.addVariable('muon_absDxy',       [100,0,0.3])
        self.addVariable('muon_absDz',        [100,0,0.5])
        self.addVariable('muon_relIsoDB',     [100,0,0.25])
        self.addVariable('muon_trackRelIso',  [100,0,0.5])

        # taus
        self.addEfficiency('tau_vlooseElectronLooseMuonOld_tightIso', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonOld_tightIso', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonOld_tightIso',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonOld_tightIso',  [100,0,500])
        self.addEfficiency('tau_vlooseElectronLooseMuonNew_tightIso', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonNew_tightIso', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonNew_tightIso',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonNew_tightIso',  [100,0,500])
        self.addEfficiency('tau_vlooseElectronLooseMuonOld_vtightIso', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonOld_vtightIso', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonOld_vtightIso',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonOld_vtightIso',  [100,0,500])
        self.addEfficiency('tau_vlooseElectronLooseMuonNew_vtightIso', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonNew_vtightIso', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonNew_vtightIso',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonNew_vtightIso',  [100,0,500])

        # not matched to gen tau jet
        self.addEfficiency('tau_vlooseElectronLooseMuonOld_tightIso_fake', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonOld_tightIso_fake', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonOld_tightIso_fake',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonOld_tightIso_fake',  [100,0,500])
        self.addEfficiency('tau_vlooseElectronLooseMuonNew_tightIso_fake', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonNew_tightIso_fake', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonNew_tightIso_fake',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonNew_tightIso_fake',  [100,0,500])
        self.addEfficiency('tau_vlooseElectronLooseMuonOld_vtightIso_fake', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonOld_vtightIso_fake', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonOld_vtightIso_fake',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonOld_vtightIso_fake',  [100,0,500])
        self.addEfficiency('tau_vlooseElectronLooseMuonNew_vtightIso_fake', [100,0,500])
        self.addEfficiency('tau_vlooseElectronTightMuonNew_vtightIso_fake', [100,0,500])
        self.addEfficiency('tau_tightElectronLooseMuonNew_vtightIso_fake',  [100,0,500])
        self.addEfficiency('tau_tightElectronTightMuonNew_vtightIso_fake',  [100,0,500])

        # add tau variables
        self.addVariable('tau_pt',           [100,0,500])
        self.addVariable('tau_absDxy',       [100,0,0.3])
        self.addVariable('tau_absDz',        [100,0,0.5])

    def fill(self,rtrow):
        # first electrons
        for i in xrange(rtrow.electrons_count):
            cand = ('electrons',i)
            # get ids
            pt = self.getObjectVariable(rtrow,cand,'pt')
            passCutBasedVeto   = self.getObjectVariable(rtrow,cand,'cutBasedVeto') > 0.5
            passCutBasedLoose  = self.getObjectVariable(rtrow,cand,'cutBasedLoose') > 0.5
            passCutBasedMedium = self.getObjectVariable(rtrow,cand,'cutBasedMedium') > 0.5
            passCutBasedTight  = self.getObjectVariable(rtrow,cand,'cutBasedTight') > 0.5
            passWWLoose        = self.getObjectVariable(rtrow,cand,'wwLoose') > 0.5
            passHEEPV60        = self.getObjectVariable(rtrow,cand,'heepV60') > 0.5
            passMVANonTrigWP80 = self.getObjectVariable(rtrow,cand,'mvaNonTrigWP80') > 0.5
            passMVANonTrigWP90 = self.getObjectVariable(rtrow,cand,'mvaNonTrigWP90') > 0.5
            passMVATrigWP80    = self.getObjectVariable(rtrow,cand,'mvaTrigWP80') > 0.5
            passMVATrigWP90    = self.getObjectVariable(rtrow,cand,'mvaTrigWP90') > 0.5
            # require MVA trig preselection
            sceta = self.getObjectVariable(rtrow,cand,'superClusterEta')
            sigmaIEtaIEta = self.getObjectVariable(rtrow,cand,'sigmaIetaIeta')
            hcalOverEcal = self.getObjectVariable(rtrow,cand,'hcalOverEcal')
            ecalRelIso = self.getObjectVariable(rtrow,cand,'dr03EcalRecHitSumEt')/pt
            hcalRelIso = self.getObjectVariable(rtrow,cand,'dr03HcalTowerSumEt')/pt
            trackRelIso = self.getObjectVariable(rtrow,cand,'dr03TkSumPt')/pt
            dEtaSC = self.getObjectVariable(rtrow,cand,'deltaEtaSuperClusterTrackAtVtx')
            dPhiSC = self.getObjectVariable(rtrow,cand,'deltaPhiSuperClusterTrackAtVtx')
            relIsoRho = self.getObjectVariable(rtrow,cand,'relPFIsoRhoR03')
            passConversion = self.getObjectVariable(rtrow,cand,'passConversionVeto')
            dxy = self.getObjectVariable(rtrow,cand,'dxy')
            dz = self.getObjectVariable(rtrow,cand,'dz')
            ecalEnergy = self.getObjectVariable(rtrow,cand,'ecalEnergy')
            eSuperClusterOverP = self.getObjectVariable(rtrow,cand,'eSuperClusterOverP')
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
            else:
                if sigmaIEtaIEta>0.033: passMVATrigPre = False
                if hcalOverEcal>0.09:   passMVATrigPre = False
                if ecalRelIso>0.45:     passMVATrigPre = False
                if hcalRelIso>0.28:     passMVATrigPre = False
                if trackRelIso>0.18:    passMVATrigPre = False
            # match to gen particle
            if (self.getObjectVariable(rtrow,cand,'genMatch')>0.5
                and self.getObjectVariable(rtrow,cand,'genStatus')==1
                and self.getObjectVariable(rtrow,cand,'genIsPrompt')>0.5
                and self.getObjectVariable(rtrow,cand,'genIsFromTau')<0.5):
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
                # fill variables
                if sceta<1.479:
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
            # not matched to gen or non-prompt non-tau decay TODO: change to fake later
            if ((self.getObjectVariable(rtrow,cand,'genMatch')<0.5)          # not gen matched
                or (self.getObjectVariable(rtrow,cand,'genMatch')>0.5        # or gen matched
                and self.getObjectVariable(rtrow,cand,'genStatus')==1        # status 1
                and self.getObjectVariable(rtrow,cand,'genIsPrompt')<0.5     # non-prompt
                and self.getObjectVariable(rtrow,cand,'genIsFromTau')<0.5)): # non-tau
                # fill efficiencies
                self.fillEfficiency('electron_cbidVeto_fake',pt,passCutBasedVeto)
                self.fillEfficiency('electron_cbidLoose_fake',pt,passCutBasedLoose)
                self.fillEfficiency('electron_cbidMedium_fake',pt,passCutBasedMedium)
                self.fillEfficiency('electron_cbidTight_fake',pt,passCutBasedTight)
                self.fillEfficiency('electron_wzLoose_fake',pt,passWWLoose)
                self.fillEfficiency('electron_wzMedium_fake',pt,passCutBasedMedium and passWWLoose)
                self.fillEfficiency('electron_wzTight_fake',pt,passCutBasedTight and passWWLoose)
                self.fillEfficiency('electron_heepV60_fake',pt,passHEEPV60)
                self.fillEfficiency('electron_mvaNonTrigWP80_fake',pt,passMVANonTrigWP80)
                self.fillEfficiency('electron_mvaNonTrigWP90_fake',pt,passMVANonTrigWP90)
                self.fillEfficiency('electron_mvaTrigPre_fake',pt,passMVATrigPre)
                self.fillEfficiency('electron_mvaTrigWP80_fake',pt,passMVATrigWP80 and passMVATrigPre)
                self.fillEfficiency('electron_mvaTrigWP90_fake',pt,passMVATrigWP90 and passMVATrigPre)
            # match to jet
            if (self.getObjectVariable(rtrow,cand,'genMatch')>0.5
                and self.getObjectVariable(rtrow,cand,'genStatus')==1
                and self.getObjectVariable(rtrow,cand,'genIsFromHadron')>0.5):
                # fill efficiencies
                self.fillEfficiency('electron_cbidVeto_jet',pt,passCutBasedVeto)
                self.fillEfficiency('electron_cbidLoose_jet',pt,passCutBasedLoose)
                self.fillEfficiency('electron_cbidMedium_jet',pt,passCutBasedMedium)
                self.fillEfficiency('electron_cbidTight_jet',pt,passCutBasedTight)
                self.fillEfficiency('electron_wzLoose_jet',pt,passWWLoose)
                self.fillEfficiency('electron_wzMedium_jet',pt,passCutBasedMedium and passWWLoose)
                self.fillEfficiency('electron_wzTight_jet',pt,passCutBasedTight and passWWLoose)
                self.fillEfficiency('electron_heepV60_jet',pt,passHEEPV60)
                self.fillEfficiency('electron_mvaNonTrigWP80_jet',pt,passMVANonTrigWP80)
                self.fillEfficiency('electron_mvaNonTrigWP90_jet',pt,passMVANonTrigWP90)
                self.fillEfficiency('electron_mvaTrigPre_jet',pt,passMVATrigPre)
                self.fillEfficiency('electron_mvaTrigWP80_jet',pt,passMVATrigWP80 and passMVATrigPre)
                self.fillEfficiency('electron_mvaTrigWP90_jet',pt,passMVATrigWP90 and passMVATrigPre)
        # next muons
        for i in xrange(rtrow.muons_count):
            cand = ('muons',i)
            # get ids
            pt = self.getObjectVariable(rtrow,cand,'pt')
            iso = self.getObjectVariable(rtrow,cand,'relPFIsoDeltaBetaR04')
            trackRelIso = self.getObjectVariable(rtrow,cand,'trackIso')/pt
            dz = self.getObjectVariable(rtrow,cand,'dz')
            dxy = self.getObjectVariable(rtrow,cand,'dxy')
            passLoose  = self.getObjectVariable(rtrow,cand,'isLooseMuon') > 0.5
            passMedium = self.getObjectVariable(rtrow,cand,'isMediumMuon') > 0.5
            passTight  = self.getObjectVariable(rtrow,cand,'isTightMuon') > 0.5
            passHighPt = self.getObjectVariable(rtrow,cand,'isHighPtMuon') > 0.5
            # match to gen particle
            if (self.getObjectVariable(rtrow,cand,'genMatch')>0.5
                and self.getObjectVariable(rtrow,cand,'genStatus')==1
                and self.getObjectVariable(rtrow,cand,'genIsPrompt')>0.5
                and self.getObjectVariable(rtrow,cand,'genIsFromTau')<0.5):
                # fill variables
                self.fillVariable('muon_pt',pt)
                self.fillVariable('muon_absDxy',abs(dxy))
                self.fillVariable('muon_absDz',abs(dz))
                self.fillVariable('muon_relIsoDB',iso)
                self.fillVariable('muon_trackRelIso',trackRelIso)
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
            # not matched to gen or non-prompt non-tau decay TODO: change to be actual fake later
            if ((self.getObjectVariable(rtrow,cand,'genMatch')<0.5)          # not gen matched
                or (self.getObjectVariable(rtrow,cand,'genMatch')>0.5        # or gen matched
                and self.getObjectVariable(rtrow,cand,'genStatus')==1        # status 1
                and self.getObjectVariable(rtrow,cand,'genIsPrompt')<0.5     # non-prompt
                and self.getObjectVariable(rtrow,cand,'genIsFromTau')<0.5)): # non-tau
                self.fillEfficiency('muon_loose_fake',pt,passLoose)
                self.fillEfficiency('muon_medium_fake',pt,passMedium)
                self.fillEfficiency('muon_tight_fake',pt,passTight)
                self.fillEfficiency('muon_highPt_fake',pt,passHighPt)
                self.fillEfficiency('muon_loose_tightiso_fake',pt,passLoose and iso<0.15)
                self.fillEfficiency('muon_medium_tightiso_fake',pt,passMedium and iso<0.15)
                self.fillEfficiency('muon_tight_tightiso_fake',pt,passTight and iso<0.15)
                self.fillEfficiency('muon_highPt_tightiso_fake',pt,passHighPt and iso<0.15)
                self.fillEfficiency('muon_wzLoose_fake',pt,passMedium and iso<0.4 and trackRelIso<0.4)
                self.fillEfficiency('muon_wzMedium_fake',pt,passMedium and iso<0.15 and trackRelIso<0.4 and dz<0.1 and (dxy<0.01 if pt<20 else dxy<0.02))
            # match to jet
            if (self.getObjectVariable(rtrow,cand,'genMatch')>0.5
                and self.getObjectVariable(rtrow,cand,'genStatus')==1
                and self.getObjectVariable(rtrow,cand,'genIsFromHadron')>0.5):
                # fill efficiencies
                self.fillEfficiency('muon_loose_jet',pt,passLoose)
                self.fillEfficiency('muon_medium_jet',pt,passMedium)
                self.fillEfficiency('muon_tight_jet',pt,passTight)
                self.fillEfficiency('muon_highPt_jet',pt,passHighPt)
                self.fillEfficiency('muon_loose_tightiso_jet',pt,passLoose and iso<0.15)
                self.fillEfficiency('muon_medium_tightiso_jet',pt,passMedium and iso<0.15)
                self.fillEfficiency('muon_tight_tightiso_jet',pt,passTight and iso<0.15)
                self.fillEfficiency('muon_highPt_tightiso_jet',pt,passHighPt and iso<0.15)
                self.fillEfficiency('muon_wzLoose_jet',pt,passMedium and iso<0.4 and trackRelIso<0.4)
                self.fillEfficiency('muon_wzMedium_jet',pt,passMedium and iso<0.15 and trackRelIso<0.4 and dz<0.1 and (dxy<0.01 if pt<20 else dxy<0.02))
        # taus
        for i in xrange(rtrow.taus_count):
            cand = ('taus',i)
            # get the ids
            pt = self.getObjectVariable(rtrow,cand,'pt')
            dz = self.getObjectVariable(rtrow,cand,'dz')
            dxy = self.getObjectVariable(rtrow,cand,'dxy')
            # muon
            againstMuonLoose3 = self.getObjectVariable(rtrow,cand,'againstMuonLoose3')
            againstMuonTight3 = self.getObjectVariable(rtrow,cand,'againstMuonTight3')
            # electron
            againstElectronVLooseMVA6 = self.getObjectVariable(rtrow,cand,'againstElectronVLooseMVA6')
            againstElectronTightMVA6 = self.getObjectVariable(rtrow,cand,'againstElectronTightMVA6')
            # old
            decayModeFinding = self.getObjectVariable(rtrow,cand,'decayModeFinding')
            byTightIsolationMVArun2v1DBoldDMwLT = self.getObjectVariable(rtrow,cand,'byTightIsolationMVArun2v1DBoldDMwLT')
            byVTightIsolationMVArun2v1DBoldDMwLT = self.getObjectVariable(rtrow,cand,'byVTightIsolationMVArun2v1DBoldDMwLT')
            # new
            decayModeFindingNewDMs = self.getObjectVariable(rtrow,cand,'decayModeFindingNewDMs')
            byTightIsolationMVArun2v1DBnewDMwLT = self.getObjectVariable(rtrow,cand,'byTightIsolationMVArun2v1DBnewDMwLT')
            byVTightIsolationMVArun2v1DBnewDMwLT = self.getObjectVariable(rtrow,cand,'byVTightIsolationMVArun2v1DBnewDMwLT')
            # match to gen jet
            if (self.getObjectVariable(rtrow,cand,'genJetMatch')>0.5):
                # fill variables
                self.fillVariable('tau_pt',pt)
                self.fillVariable('tau_absDxy',abs(dxy))
                self.fillVariable('tau_absDz',abs(dz))
                # fill efficiencies
                self.fillEfficiency('tau_vlooseElectronLooseMuonOld_tightIso', pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonOld_tightIso', pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonOld_tightIso',  pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonOld_tightIso',  pt, decayModeFinding>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronLooseMuonOld_vtightIso',pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonOld_vtightIso',pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonOld_vtightIso', pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonOld_vtightIso', pt, decayModeFinding>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronLooseMuonNew_tightIso', pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonNew_tightIso', pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonNew_tightIso',  pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonNew_tightIso',  pt, decayModeFindingNewDMs>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronLooseMuonNew_vtightIso',pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonNew_vtightIso',pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonNew_vtightIso', pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonNew_vtightIso', pt, decayModeFindingNewDMs>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
            if (self.getObjectVariable(rtrow,cand,'genJetMatch')<0.5):
                # fill efficiencies
                self.fillEfficiency('tau_vlooseElectronLooseMuonOld_tightIso_fake', pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonOld_tightIso_fake', pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonOld_tightIso_fake',  pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonOld_tightIso_fake',  pt, decayModeFinding>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronLooseMuonOld_vtightIso_fake',pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonOld_vtightIso_fake',pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonOld_vtightIso_fake', pt, decayModeFinding>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonOld_vtightIso_fake', pt, decayModeFinding>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronLooseMuonNew_tightIso_fake', pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonNew_tightIso_fake', pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonNew_tightIso_fake',  pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonNew_tightIso_fake',  pt, decayModeFindingNewDMs>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronLooseMuonNew_vtightIso_fake',pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_vlooseElectronTightMuonNew_vtightIso_fake',pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronLooseMuonNew_vtightIso_fake', pt, decayModeFindingNewDMs>0.5 and againstElectronVLooseMVA6>0.5 and againstMuonLoose3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
                self.fillEfficiency('tau_tightElectronTightMuonNew_vtightIso_fake', pt, decayModeFindingNewDMs>0.5 and againstElectronTightMVA6>0.5 and againstMuonTight3>0.5 and byVTightIsolationMVArun2v1DBnewDMwLT>0.5)
