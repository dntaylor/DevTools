import FWCore.ParameterSet.Config as cms

def getCapitalizedSingular(name):
    return name.rstrip('s').capitalize()

def objectSelector(process,obj,objSrc,selection):
    '''Filter an object collection based on a cut string'''
    
    module = cms.EDFilter(
        "PAT{0}Selector".format(getCapitalizedSingular(obj)),
        src = cms.InputTag(objSrc),
        cut = cms.string(selection),
    )
    modName = '{0}Selection'.format(obj)
    setattr(process,modName,module)

    pathName = '{0}SlectionPath'.format(obj)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)

    process.schedule.append(getattr(process,pathName))

    return modName

def objectCleaner(process,obj,objSrc,collections,cleaning):
    '''Clean an object collection'''

    cleanParams = cms.PSet()
    for cleanObj in cleaning:
        cleanSrc = collections[cleanObj]
        cut = cleaning[cleanObj]['cut']
        dr  = cleaning[cleanObj]['dr']

        particleParams = cms.PSet(
            src=cms.InputTag(cleanSrc),
            algorithm=cms.string("byDeltaR"),
            preselection=cms.string(cut),
            deltaR=cms.double(dr),
            checkRecoComponents=cms.bool(False),
            pairCut=cms.string(''),
            requireNoOverlaps=cms.bool(True),
        )

        setattr(cleanParams,cleanObj,particleParams)

    module = cms.EDProducer(
        "PAT{0}Cleaner".format(getCapitalizedSingular(obj)),
        src = cms.InputTag(objSrc),
        preselection = cms.string(''),
        checkOverlaps = cleanParams,
        finalCut = cms.string(''),
    )
    modName = '{0}Cleaning'.format(obj)
    setattr(process,modName,module)

    pathName = '{0}CleaningPath'.format(obj)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)

    process.schedule.append(getattr(process,pathName))

    return modName
