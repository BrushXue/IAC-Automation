"""
This script is used to generate the IAC recommendation for Recover Exhaust Gas Heat.
"""

import json5, sys, os
from docx import Document
from easydict import EasyDict
from python_docx_replace import docx_replace
sys.path.append(os.path.join('..', '..')) 
from Shared.IAC import *
import numpy as np
import AFR

# Load utility cost
jsonDict = json5.load(open(os.path.join('..', '..', 'Utility.json5')))
# Load database
jsonDict.update(json5.load(open('database.json5')))
# Convert to easydict
iac = EasyDict(jsonDict)

# Interpolation

# Calculations
iac.OH = int(iac.HR * iac.DY * iac.WK)
iac.NGS = round(iac.SIZE * iac.OH * (iac.LF/100) * (iac.SAV/100))
iac.ACS = round(iac.NGS * iac.NGC)
iac.CAH = round(AFR.AFR(iac.CAT, iac.FGT, iac.O2))
iac.IC = round(iac.LABOR * iac.PARTS)

# Implementation
iac.PB = payback(iac.ACS, iac.IC)

## Format strings
# set electricity cost to 3 digits accuracy
iac = dollar(['EC'],iac,3)
# set the natural gas and demand to 2 digits accuracy
iac = dollar(['NGC', 'DC'],iac,2)
# set the rest to integer
varList = ['LR', 'NGCS', 'EUC', 'DUC', 'ACS', 'IC']
iac = dollar(varList,iac,0)
# Format all numbers to string with thousand separator
iac = grouping_num(iac)

# Import docx template
doc = Document('template.docx')

# Replacing keys
docx_replace(doc, **iac)

savefile(doc, iac.AR)

# Caveats
caveat("Please modify highlighted region if necessary.")