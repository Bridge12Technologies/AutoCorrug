#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies, Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Define run and geometry parameters for CORRUG

import sys
sys.path.insert(0, '..\\src')
import numpy as np
from numpy import linspace
from Sections import *


def simulation_parameters():
    # nodes = ['10.12.70.12', '10.12.70.64']
    nodes = ['10.12.50.5']
    # nodes on which the simulation is run
    # results_path = '//10.12.70.26/Shared Data/Projects/FFP-PANS-0099/HE11-Launcher/v1'
    results_path = 'D:/Bridge12/Projects/MyCorrugDesign/results'
    var_range = {}

    var_range['version_num'] = ['HE11Taper']    # version number
    var_range['Frequency'] = [193,190,191,192,193,194,195,196,384,385,386,387,388]
    var_range['Input Modes'] = ['HE11'] # TE11, HE11
    var_range['Number of Modes at Input Crosssection'] = [10,20]
    var_range['NTheta'] = [10]
    var_range['DTheta'] = [10]


    var_range['Input Section Profile'] = ['Linear'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['Input Section Length'] = [20]
    var_range['Input Dia'] = [5.0]
    var_range['Output Dia'] = [16.28]
    
    var_range['CWG Uptaper Profile'] = ['Linear', 'Sine Squared', 'Raised Cosine']
    var_range['CWG Uptaper Length'] = [110,150,200]

    var_range['Output Section Profile'] = ['Linear'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['Output Section Length'] = [25,50,75,100]

    var_range['Tooth Width'] = [0.13] #[0.26]
    var_range['Slot Width'] = [0.13] #[0.26]
    var_range['Corrug Depth'] = [0.195] #[0.39]
    
    var_list = [['Output Section Length', 'CWG Uptaper Profile', 'Frequency'], ['Output Section Length', 'CWG Uptaper Length', 'Frequency']]

    return nodes, results_path, var_list, var_range

def define_geometry(var_register,step_directory):

    geometry = []
    
    nummodes = var_register['Number of Modes at Input Crosssection'][0] 
    geometry.append(CorrugatedSection(name='Input Section',sd=var_register['Input Dia'][0],ed=var_register['Input Dia'][0],
    scd=var_register['Corrug Depth'][0],ecd=var_register['Corrug Depth'][0],
    csw=var_register['Slot Width'][0],ctw=var_register['Tooth Width'][0],  
    length=var_register['Input Section Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['Input Section Profile'][0],z=[],r=[],rn=[]))
    
    nummodes = int(var_register['Number of Modes at Input Crosssection'][0]*var_register['Input Dia'][0]/var_register['Input Dia'][0])
    geometry.append(CorrugatedSection(name='CWG Uptaper',sd=var_register['Input Dia'][0],ed=var_register['Output Dia'][0], 
    scd=var_register['Corrug Depth'][0],ecd=var_register['Corrug Depth'][0],
    csw=var_register['Slot Width'][0],ctw=var_register['Tooth Width'][0],  
    length=var_register['CWG Uptaper Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['CWG Uptaper Profile'][0],z=[],r=[],rn=[]))

    nummodes = int(var_register['Number of Modes at Input Crosssection'][0]*var_register['Output Dia'][0]/var_register['Input Dia'][0])
    geometry.append(CorrugatedSection(name='CWG Straight Section',sd=var_register['Output Dia'][0],ed=var_register['Output Dia'][0],
    scd=var_register['Corrug Depth'][0],ecd=var_register['Corrug Depth'][0],
    csw=var_register['Slot Width'][0],ctw=var_register['Tooth Width'][0],  
    length=var_register['Output Section Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['Output Section Profile'][0],z=[],r=[],rn=[]))

    return geometry