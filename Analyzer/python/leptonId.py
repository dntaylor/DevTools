# common leptons ids

#########################
### SMP-16-002 WZ ids ###
#########################
def passWZLoose(self,rtrow,cand):
    pt = self.getObjectVariable(rtrow,cand,'pt')
    eta = self.getObjectVariable(rtrow,cand,'eta')
    if cand[0]=="electrons":
        if pt<=10: return False
        if abs(eta)>=2.5: return False
        if self.getObjectVariable(rtrow,cand,'wwLoose')<0.5: return False
    elif cand[0]=="muons":
        if pt<=10: return False
        if abs(eta)>=2.4: return False
        isMediumMuon = self.getObjectVariable(rtrow,cand,'isMediumMuon')
        if isMediumMuon<0.5: return False
        trackIso = self.getObjectVariable(rtrow,cand,'trackIso')
        if trackIso/pt>=0.4: return False
        pfRelIsoDB = self.getObjectVariable(rtrow,cand,'relPFIsoDeltaBetaR04')
        if pfRelIsoDB>=0.4: return False
    else:
        return False
    return True

def passWZMedium(self,rtrow,cand):
    if not passWZLoose(self,rtrow,cand): return False
    if cand[0]=="electrons":
        if self.getObjectVariable(rtrow,cand,'cutBasedMedium')<0.5: return False
    elif cand[0]=="muons":
        dz = self.getObjectVariable(rtrow,cand,'dz')
        if abs(dz)>=0.1: return False
        pt = self.getObjectVariable(rtrow,cand,'pt')
        dxy = self.getObjectVariable(rtrow,cand,'dB2D')
        if abs(dxy)>=0.01 and pt<20: return False
        if abs(dxy)>=0.02 and pt>=20: return False
        pfRelIsoDB = self.getObjectVariable(rtrow,cand,'relPFIsoDeltaBetaR04')
        if pfRelIsoDB>=0.15: return False
    else:
        return False
    return True

def passWZTight(self,rtrow,cand):
    if not passWZLoose(self,rtrow,cand): return False
    if cand[0]=="electrons":
        if self.getObjectVariable(rtrow,cand,'cutBasedTight')<0.5: return False
    elif cand[0]=="muons":
        return passWZMedium(self,rtrow,cand)
    else:
        return False
    return True

###############
### H++ ids ###
###############
def passHppLoose(self,rtrow,cand):
    if cand[0]=='electrons':
        #pt = self.getObjectVariable(rtrow,cand,'pt')
        #sceta = self.getObjectVariable(rtrow,cand,'superClusterEta')
        #sigmaIEtaIEta = self.getObjectVariable(rtrow,cand,'sigmaIetaIeta')
        #hcalOverEcal = self.getObjectVariable(rtrow,cand,'hcalOverEcal')
        #ecalRelIso = self.getObjectVariable(rtrow,cand,'dr03EcalRecHitSumEt')/pt
        #hcalRelIso = self.getObjectVariable(rtrow,cand,'dr03HcalTowerSumEt')/pt
        #trackRelIso = self.getObjectVariable(rtrow,cand,'dr03TkSumPt')/pt
        #dEtaSC = self.getObjectVariable(rtrow,cand,'deltaEtaSuperClusterTrackAtVtx')
        #dPhiSC = self.getObjectVariable(rtrow,cand,'deltaPhiSuperClusterTrackAtVtx')
        #passMVATrigPre = True
        #if sceta<1.479:
        #    if sigmaIEtaIEta>0.012: passMVATrigPre = False
        #    if hcalOverEcal>0.09:   passMVATrigPre = False
        #    if ecalRelIso>0.37:     passMVATrigPre = False
        #    if hcalRelIso>0.25:     passMVATrigPre = False
        #    if trackRelIso>0.18:    passMVATrigPre = False
        #    if abs(dEtaSC)>0.0095:  passMVATrigPre = False
        #    if abs(dPhiSC)>0.065:   passMVATrigPre = False
        #else:
        #    if sigmaIEtaIEta>0.033: passMVATrigPre = False
        #    if hcalOverEcal>0.09:   passMVATrigPre = False
        #    if ecalRelIso>0.45:     passMVATrigPre = False
        #    if hcalRelIso>0.28:     passMVATrigPre = False
        #    if trackRelIso>0.18:    passMVATrigPre = False
        #return passMVATrigPre
        return passWZLoose(self,rtrow,cand)
    elif cand[0]=='muons':
        return passWZLoose(self,rtrow,cand)
    elif cand[0]=='taus':
        decayModeFinding = self.getObjectVariable(rtrow,cand,'decayModeFinding')
        againstMuonTight3 = self.getObjectVariable(rtrow,cand,'againstMuonTight3')
        againstElectronTightMVA6 = self.getObjectVariable(rtrow,cand,'againstElectronTightMVA6')
        byVTightIsolationMVArun2v1DBoldDMwLT = self.getObjectVariable(rtrow,cand,'byVTightIsolationMVArun2v1DBoldDMwLT')
        return (decayModeFinding>0.5
                and againstMuonTight3>0.5
                and againstElectronTightMVA6>0.5
                and byVTightIsolationMVArun2v1DBoldDMwLT>0.5)
    else:
        return False

def passHppMedium(self,rtrow,cand):
    if not passHppLoose(self,rtrow,cand): return False
    if cand[0]=='electrons':
        #return self.getObjectVariable(rtrow,cand,'mvaTrigWP80') > 0.5
        return passWZMedium(self,rtrow,cand)
    elif cand[0]=='muons':
        return passWZMedium(self,rtrow,cand)
    elif cand[0]=='taus':
        return True # only 1 ID for now
    else:
        return False

def passHppTight(self,rtrow,cand):
    if not passHppLoose(self,rtrow,cand): return False
    if cand[0]=='electrons':
        #return self.getObjectVariable(rtrow,cand,'mvaTrigWP80') > 0.5
        return passWZTight(self,rtrow,cand)
    elif cand[0]=='muons':
        return passWZMedium(self,rtrow,cand)
    elif cand[0]=='taus':
        return True # only 1 ID for now
    else:
        return False
