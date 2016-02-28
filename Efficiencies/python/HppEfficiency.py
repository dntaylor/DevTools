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

        # matched to hadron TODO: need new ntuples
        #self.addEfficiency('electron_cbidVeto_jet',      [100,0,500])
        #self.addEfficiency('electron_cbidLoose_jet',     [100,0,500])
        #self.addEfficiency('electron_cbidMedium_jet',    [100,0,500])
        #self.addEfficiency('electron_cbidTight_jet',     [100,0,500])
        #self.addEfficiency('electron_wzLoose_jet',       [100,0,500])
        #self.addEfficiency('electron_wzMedium_jet',      [100,0,500])
        #self.addEfficiency('electron_wzTight_jet',       [100,0,500])
        #self.addEfficiency('electron_heepV60_jet',       [100,0,500])
        #self.addEfficiency('electron_mvaNonTrigWP80_jet',[100,0,500])
        #self.addEfficiency('electron_mvaNonTrigWP90_jet',[100,0,500])
        #self.addEfficiency('electron_mvaTrigPre_jet',    [100,0,500])
        #self.addEfficiency('electron_mvaTrigWP80_jet',   [100,0,500])
        #self.addEfficiency('electron_mvaTrigWP90_jet',   [100,0,500])

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

        # matched to gen decay from hadron TODO: need new ntuples
        #self.addEfficiency('muon_loose_jet',             [100,0,500])
        #self.addEfficiency('muon_medium_jet',            [100,0,500])
        #self.addEfficiency('muon_tight_jet',             [100,0,500])
        #self.addEfficiency('muon_highPt_jet',            [100,0,500])
        #self.addEfficiency('muon_loose_tightiso_jet',    [100,0,500])
        #self.addEfficiency('muon_medium_tightiso_jet',   [100,0,500])
        #self.addEfficiency('muon_tight_tightiso_jet',    [100,0,500])
        #self.addEfficiency('muon_highPt_tightiso_jet',   [100,0,500])
        #self.addEfficiency('muon_wzLoose_jet',           [100,0,500])
        #self.addEfficiency('muon_wzMedium_jet',          [100,0,500])


    def fill(self,rtrow):
        # first electrons
        for i in xrange(rtrow.electrons_count):
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
            else:
                if sigmaIEtaIEta>0.033: passMVATrigPre = False
                if hcalOverEcal>0.09:   passMVATrigPre = False
                if ecalRelIso>0.45:     passMVATrigPre = False
                if hcalRelIso>0.28:     passMVATrigPre = False
                if trackRelIso>0.18:    passMVATrigPre = False
            # match to gen particle
            if (self.getObjectVariable(rtrow,('electrons',i),'genMatch')>0.5
                and self.getObjectVariable(rtrow,('electrons',i),'genStatus')==1
                and self.getObjectVariable(rtrow,('electrons',i),'genIsPrompt')>0.5):
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
            if ((self.getObjectVariable(rtrow,('electrons',i),'genMatch')<0.5)          # not gen matched
                or (self.getObjectVariable(rtrow,('electrons',i),'genMatch')>0.5        # or gen matched
                and self.getObjectVariable(rtrow,('electrons',i),'genStatus')==1        # status 1
                and self.getObjectVariable(rtrow,('electrons',i),'genIsPrompt')<0.5     # non-prompt
                and self.getObjectVariable(rtrow,('electrons',i),'genIsFromTau')<0.5)): # non-tau
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
            #if (self.getObjectVariable(rtrow,('electrons',i),'genMatch')>0.5
            #    and self.getObjectVariable(rtrow,('electrons',i),'genStatus')==1
            #    and self.getObjectVariable(rtrow,('electrons',i),'genIsFromHadron')>0.5):
            #    # fill efficiencies
            #    self.fillEfficiency('electron_cbidVeto_jet',pt,passCutBasedVeto)
            #    self.fillEfficiency('electron_cbidLoose_jet',pt,passCutBasedLoose)
            #    self.fillEfficiency('electron_cbidMedium_jet',pt,passCutBasedMedium)
            #    self.fillEfficiency('electron_cbidTight_jet',pt,passCutBasedTight)
            #    self.fillEfficiency('electron_wzLoose_jet',pt,passWWLoose)
            #    self.fillEfficiency('electron_wzMedium_jet',pt,passCutBasedMedium and passWWLoose)
            #    self.fillEfficiency('electron_wzTight_jet',pt,passCutBasedTight and passWWLoose)
            #    self.fillEfficiency('electron_heepV60_jet',pt,passHEEPV60)
            #    self.fillEfficiency('electron_mvaNonTrigWP80_jet',pt,passMVANonTrigWP80)
            #    self.fillEfficiency('electron_mvaNonTrigWP90_jet',pt,passMVANonTrigWP90)
            #    self.fillEfficiency('electron_mvaTrigPre_jet',pt,passMVATrigPre)
            #    self.fillEfficiency('electron_mvaTrigWP80_jet',pt,passMVATrigWP80 and passMVATrigPre)
            #    self.fillEfficiency('electron_mvaTrigWP90_jet',pt,passMVATrigWP90 and passMVATrigPre)
        # next muons
        for i in xrange(rtrow.muons_count):
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
            # match to gen particle
            if (self.getObjectVariable(rtrow,('muons',i),'genMatch')>0.5
                and self.getObjectVariable(rtrow,('muons',i),'genStatus')==1
                and self.getObjectVariable(rtrow,('muons',i),'genIsPrompt')>0.5):
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
            if ((self.getObjectVariable(rtrow,('muons',i),'genMatch')<0.5)          # not gen matched
                or (self.getObjectVariable(rtrow,('muons',i),'genMatch')>0.5        # or gen matched
                and self.getObjectVariable(rtrow,('muons',i),'genStatus')==1        # status 1
                and self.getObjectVariable(rtrow,('muons',i),'genIsPrompt')<0.5     # non-prompt
                and self.getObjectVariable(rtrow,('muons',i),'genIsFromTau')<0.5)): # non-tau
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
            #if (self.getObjectVariable(rtrow,('muons',i),'genMatch')>0.5
            #    and self.getObjectVariable(rtrow,('muons',i),'genStatus')==1
            #    and self.getObjectVariable(rtrow,('muons',i),'genIsFromHadron')>0.5):
            #    # fill efficiencies
            #    self.fillEfficiency('muon_loose_jet',pt,passLoose)
            #    self.fillEfficiency('muon_medium_jet',pt,passMedium)
            #    self.fillEfficiency('muon_tight_jet',pt,passTight)
            #    self.fillEfficiency('muon_highPt_jet',pt,passHighPt)
            #    self.fillEfficiency('muon_loose_tightiso_jet',pt,passLoose and iso<0.15)
            #    self.fillEfficiency('muon_medium_tightiso_jet',pt,passMedium and iso<0.15)
            #    self.fillEfficiency('muon_tight_tightiso_jet',pt,passTight and iso<0.15)
            #    self.fillEfficiency('muon_highPt_tightiso_jet',pt,passHighPt and iso<0.15)
            #    self.fillEfficiency('muon_wzLoose_jet',pt,passMedium and iso<0.4 and trackRelIso<0.4)
            #    self.fillEfficiency('muon_wzMedium_jet',pt,passMedium and iso<0.15 and trackRelIso<0.4 and dz<0.1 and (dxy<0.01 if pt<20 else dxy<0.02))


