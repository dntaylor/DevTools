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
        dxy = self.getObjectVariable(rtrow,cand,'dxy')
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


