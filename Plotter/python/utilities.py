# common utilities for plotting

def isData(sample):
    '''Test if sample is data'''
    dataSamples = ['DoubleMuon','DoubleEG','MuonEG','SingleMuon','SingleElectron','Tau']
    return sample in dataSamples

def getLumi():
    '''Get the integrated luminosity to scale monte carlo'''
    #return 2263 # december jamboree golden json
    return 2318 # moriond golden json

