from itertools import product, combinations_with_replacement

cats = ['I','II','III','IV','V','VI']
catLabelMap = {
    'I'  : 'Cat I',
    'II' : 'Cat II',
    'III': 'Cat III',
    'IV' : 'Cat IV',
    'V'  : 'Cat V',
    'VI' : 'Cat VI',
}
catLabels = [catLabelMap[cat] for cat in cats]
# based on number of taus in each higgs
catContentMap = {
    'Hpp4l': {
        'I'  : [0,0],
        'II' : [0,1],
        'III': [0,2],
        'IV' : [1,1],
        'V'  : [1,2],
        'VI' : [2,2],
    },
    'Hpp3l': {
        'I'  : [0,0],
        'II' : [0,1],
        'III': [1,0],
        'IV' : [1,1],
        'V'  : [2,0],
        'VI' : [2,1],
    },
}
# based on flavor of light lepton relative to first
# 0,1,2 = e/m,m/e,t
# each cat = [n,n,n,n], [n,n,n]
subCats = {
    'Hpp4l' : {
        'I' : {
            'a': [0,0,0,0], # all same flavor
            'b': [0,0,0,1], # one different flavor
            'c': [0,0,1,1], # hpp and hmm same flavor (cleanest)
            'd': [0,1,0,1], # hpp and hmm flavor violating
        },
        'II' : {
            'a': [0,0,0,2], # single tau, rest same
            'b': [0,0,1,2], # one higgs same flavor, other to opposite flavor/tau
            'c': [0,1,0,2], # one flavor violating, other to light + tau
        },
        'III' : {
            'a': [0,0,2,2], # one same, other taus
            'b': [0,1,2,2], # one flavor violating, other taus
        },
        'IV' : {
            'a': [0,2,0,2], # each to same light plus tau
            'b': [0,2,1,2], # each to different light plus tau
        },
        'V' : {
            'a': [0,2,2,2], # to three taus + light
        },
        'VI' : {
            'a': [2,2,2,2], # to 4 taus
        },
   },
   'Hpp3l' : {
       'I' : {
           'a': [0,0,0], # all same flavor
           'b': [0,0,1], # one different flavor in h-
           'c': [0,1,0], # one different flavor in h++
       },
       'II' : {
           'a': [0,0,2], # h++ same h- tau
           'b': [0,1,2], # h++ different h- tau
       },
       'III' : {
           'a': [0,2,0], # h++ one tau, same h-
           'b': [0,2,1], # h++ one tau, different h-
       },
       'IV' : {
           'a': [0,2,2], # h++ one tau, h- tau
       },
       'V' : {
           'a': [2,2,0], # h++ two tau, h- light
       },
       'VI' : {
           'a': [2,2,2], # all tau
       },
   },
}
subCatLabelMap = {
    'Hpp4l' : {
        'I' : {
            'a': 'llll',
            'b': 'llll\'',
            'c': 'lll\'l\'',
            'd': 'll\'ll\'',
        },
        'II' : {
            'a': 'lll#tau',
            'b': 'lll\'#tau',
            'c': 'll\'l#tau',
        },
        'III' : {
            'a': 'll#tau#tau',
            'b': 'll\'#tau#tau',
        },
        'IV' : {
            'a': 'l#tau l#tau',
            'b': 'l#tau l\'#tau',
        },
        'V' : {
            'a': 'l#tau#tau#tau',
        },
        'VI' : {
            'a': '#tau#tau#tau#tau',
        },
    },
    'Hpp3l' : {
        'I' : {
            'a': 'lll',
            'b': 'lll\'',
            'c': 'll\'l',
        },
        'II' : {
            'a': 'll#tau',
            'b': 'll\'#tau',
        },
        'III' : {
            'a': 'l#tau l',
            'b': 'l#tau l\'',
        },
        'IV' : {
            'a': 'l#tau#tau',
        },
        'V' : {
            'a': '#tau#tau l',
        },
        'VI' : {
            'a': '#tau#tau#tau',
        },
    },
}
subCatChannels = {}
for analysis in ['Hpp3l','Hpp4l']:
    subCatChannels[analysis] = {}
    for cat in cats:
        subCatChannels[analysis][cat] = {}
        for subCat in subCats[analysis][cat]:
            strings = []
            for i,l in enumerate(subCats[analysis][cat][subCat]):
                if i==0 and l==0:                          # start with a light lepton
                    strings = ['e','m']
                elif i==0 and l==2:                        # start with a tau
                    strings = ['t']
                elif i>0:                                  # add a character
                    if l==2:                               # add a tau
                        for s in range(len(strings)):
                            strings[s] += 't'
                    else:                                  # add a light lepton
                        for s in range(len(strings)):
                            if l==subCats[analysis][cat][subCat][0]: # add the same light lepton
                                strings[s] += strings[s][0]
                            else:                          # add a different light lepton
                                strings[s] += 'e' if strings[s][0]=='m' else 'm'
            result = []
            if analysis in ['Hpp4l']:
                for string in strings:
                    hpphmm = ''.join(sorted(string[:2]) + sorted(string[2:]))
                    if hpphmm not in result: result += [hpphmm]
                    hmmhpp = ''.join(sorted(string[2:]) + sorted(string[:2]))
                    if hmmhpp not in result: result += [hmmhpp]
            elif analysis in ['Hpp3l']:
                for string in strings:
                    hpphm = ''.join(sorted(string[:2]) + sorted(string[2:]))
                    if hpphm not in result: result += [hpphm]
            subCatChannels[analysis][cat][subCat] = result

def getCategories(analysis):
    '''Get categories'''
    return cats

def getCategoryLabels(analysis):
    '''Get category labels'''
    return catLabels

def getSubCategories(analysis):
    '''Get subcategories'''
    return subCatChannels[analysis] if analysis in subCatChannels else {}

def getSubCategoryLabels(analysis):
    '''Get subcategory labels'''
    if analysis not in subCatLabelMap: return []
    subCatLabelList = []
    for cat in cats:
        for subCat in sorted(subCatLabelMap[analysis][cat]):
            subCatLabelList += [subCatLabelMap[analysis][cat][subCat]]
    return subCatLabelList

def getChannels(analysis):
    '''Get channel strings for analysis'''
    chans = {}
    hppChannels = [''.join(x) for x in product('emt',repeat=2)]
    hmChannels  = [''.join(x) for x in product('emt',repeat=1)]
    if analysis=='Hpp4l':
        for hpp in hppChannels:
            for hmm in hppChannels:
                chanString = ''.join(sorted(hpp))+''.join(sorted(hmm))
                if chanString not in chans:
                    chans[chanString] = []
                chans[chanString] += [hpp+hmm]
    elif analysis=='Hpp3l':
        for hpp in hppChannels:
            for hm in hmChannels:
                chanString = ''.join(sorted(hpp))+''.join(sorted(hm))
                if chanString not in chans:
                    chans[chanString] = []
                chans[chanString] += [hpp+hm]
    return chans

def getChannelLabels(analysis):
    '''Get channel labels'''
    labelMap = {
        'e': 'e',
        'm': '#mu',
        't': '#tau',
    }
    chanLabels = [''.join([labelMap[c] for c in chan]) for chan in sorted(getChannels(analysis).keys())]
    return chanLabels

def getGenChannels(analysis):
    genChannelsPP = []
    genChannelsAP = []
    genHiggsChannels = [''.join(x) for x in combinations_with_replacement('emt',2)]
    genHiggsChannels2 = [''.join(x) for x in combinations_with_replacement('emt',1)]
    for hpp in genHiggsChannels:
        for hmm in genHiggsChannels:
            genChannelsPP += [hpp+hmm]
        for hm in genHiggsChannels2:
            genChannelsAP += [hpp+hm]
    return {'PP':genChannelsPP,'AP':genChannelsAP}
