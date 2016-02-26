import ROOT

# Some colors
colors = {
    'Gray'       : {'color' : ROOT.TColor.GetColor('#B8B8B8'), 'accent' : ROOT.TColor.GetColor('#C8C8C8')},
    'Purple'     : {'color' : ROOT.TColor.GetColor('#AD33FF'), 'accent' : ROOT.TColor.GetColor('#7924B2')},
    'Yellow'     : {'color' : ROOT.TColor.GetColor('#FFFF00'), 'accent' : ROOT.TColor.GetColor('#FFCC26')},
    'Gold'       : {'color' : ROOT.TColor.GetColor('#CCCC00'), 'accent' : ROOT.TColor.GetColor('#D1D119')},
    'DarkYellow' : {'color' : ROOT.TColor.GetColor('#FFCC00'), 'accent' : ROOT.TColor.GetColor('#E6B800')},
    'Orange'     : {'color' : ROOT.TColor.GetColor('#DC7612'), 'accent' : ROOT.TColor.GetColor('#BD3200')},
    'Blue'       : {'color' : ROOT.TColor.GetColor('#107FC9'), 'accent' : ROOT.TColor.GetColor('#0E4EAD')},
    'Navy'       : {'color' : ROOT.TColor.GetColor('#003399'), 'accent' : ROOT.TColor.GetColor('#00297A')},
    'Steel'      : {'color' : ROOT.TColor.GetColor('#9999FF'), 'accent' : ROOT.TColor.GetColor('#B8B8FF')},
    'DarkRed'    : {'color' : ROOT.TColor.GetColor('#A30000'), 'accent' : ROOT.TColor.GetColor('#8F0000')},
    'Red'        : {'color' : ROOT.TColor.GetColor('#F01800'), 'accent' : ROOT.TColor.GetColor('#780000')},
    'Green'      : {'color' : ROOT.TColor.GetColor('#36802D'), 'accent' : ROOT.TColor.GetColor('#234D20')},
    'BlueGreen'  : {'color' : ROOT.TColor.GetColor('#00CC99'), 'accent' : ROOT.TColor.GetColor('#00A37A')},
    'LightGreen' : {'color' : ROOT.TColor.GetColor('#66FF99'), 'accent' : ROOT.TColor.GetColor('#52CC7A')},
    'Lime'       : {'color' : ROOT.TColor.GetColor('#9ED54C'), 'accent' : ROOT.TColor.GetColor('#59A80F')},
    'Aqua'       : {'color' : ROOT.TColor.GetColor('#66FFFF'), 'accent' : ROOT.TColor.GetColor('#52CCCC')},
}

colorMap = {
    'datadriven': 'Gray',
    'ZZ'        : 'Blue',
    'ZG'        : 'Red',
    'WZ'        : 'Purple',
    'WW'        : 'Aqua',
    'VVV'       : 'Navy',
    'WWW'       : 'Navy',
    'WWZ'       : 'Navy',
    'WZZ'       : 'Navy',
    'ZZZ'       : 'Navy',
    'TTV'       : 'BlueGreen', 
    'TTZ'       : 'BlueGreen', 
    'TTW'       : 'BlueGreen', 
    'Z'         : 'Yellow',
    'TT'        : 'Green',
    'HppHmm'    : 'Orange',
    'HppHm'     : 'Orange',
}

labelMap = {
    'datadriven': 'Non-Prompt',
    'ZZ'        : 'ZZ',
    'ZG'        : 'Z#gamma',
    'WZ'        : 'WZ',
    'WW'        : 'WW',
    'VVV'       : 'VVV',
    'WWW'       : 'WWW',
    'WWZ'       : 'WWZ',
    'WZZ'       : 'WZZ',
    'ZZZ'       : 'ZZZ',
    'TTV'       : 't#bar{t}V',
    'TTZ'       : 't#bar{t}Z',
    'TTW'       : 't#bar{t}W',
    'Z'         : 'Z',
    'TT'        : 't#bar{t}',
    'HppHmm'    : '#Phi^{++}#Phi^{--}',
    'HppHm'     : '#Phi^{#pm#pm}#Phi^{#mp}',
}

for sig in ['HppHmm','HppHm']:
    for mass in [200,250,300,350,400,450,500,600,700,800,900]:
        key = '{0}{1}GeV'.format(sig,mass)
        colorMap[key] = colorMap[sig]
        labelMap[key] = labelMap[sig] + ' ({0} GeV)'.format(mass)
    for mass in [1,1.1,1.2,1.3,1.4,1.5]:
        key = '{0}{1:3.1f}TeV'.format(sig,mass)
        colorMap[key] = colorMap[sig]
        labelMap[key] = labelMap[sig] + ' ({0:3.1f} TeV)'.format(mass)



def getStyle(sample):
    style = {}
    if sample=='data':
        style['legendstyle'] = 'pe'
        style['drawstyle'] = 'pe'
        style['name'] = 'Observed'
    else:
        style['legendstyle'] = 'f'
        style['drawstyle'] = 'hist'
        style['fillstyle'] = 1001
        style['linecolor'] = colors[colorMap[sample]]['accent']
        style['fillcolor'] = colors[colorMap[sample]]['color']
        style['name'] = labelMap[sample]
    return style
