#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies, Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Postprocessor for analyzing CORRUG simulation results

import sys, argparse, os
sys.path.insert(0, '..\\src')
import CorrugUtils, CorrugPostprocessUtils
import os, json

def main(args):
    if args.timestamp == 'latest':
        all_subdirs = [d for d in os.listdir(args.p) if os.path.isdir(args.p + '/' + d)]
        latest_timestamp = max(all_subdirs)
        results_dir = args.p + '/' + latest_timestamp
    else:
        results_dir = args.p + '/' + args.timestamp    

    var_range = json.load(open(results_dir + '/NominalParameters.dict'))
    var_list = json.load(open(results_dir + '/ScanVariables.list'))

    var_list_flat = CorrugUtils.flatten(var_list)  # flatten the multilevel scan parameter list
    var_list = list(set(var_list_flat))   # remove duplicates

    if args.retabulate == True or os.path.exists(results_dir + '/' + 'parameters.sort') == False:
        listdic =CorrugPostprocessUtils.tabulate_parameter_variations(results_dir) # read all the simulation directories and gather parameter variations
        warning_oldtab = False
    else:
        print('WARNING - Loading sorted scanned parameters tables from disk. Tables may not be up to date. Run with PostProcessor with option  -r True')
        warning_oldtab = True
        with open (results_dir + '/' + 'parameters.sort', 'r') as infile:
            listdic = json.load(infile)

    TE11HE11ProfileList = ['Linear', 'Sine Squared', 'Raised Cosine']
    TE11HE11ConvLenList = [15, 40, 50, 80]
    CWGStraightSectionLength = [10, 20, 40, 60, 80, 100]
    FrequencyList = [90,92,93,94,96,98,100]                      
                                                                                                     
    CorrugPostprocessUtils.postprocess_3parameters_1variable(results_dir, listdic, var_range, var_list, 'HE11 Power', 'Fraction', 'Frequency', 'GHz', FrequencyList,  
                                    'TE11-HE11 Conv Profile', ' ', TE11HE11ProfileList, 'CWG Straight Section Length', 'mm', CWGStraightSectionLength,  
                                    plotxrange='[:]',plotyrange='[:]', labels = 'False', subplot_columns = 2)  

    CorrugPostprocessUtils.postprocess_3parameters_1variable(results_dir, listdic, var_range, var_list, 'HE11 Power', 'Fraction', 'Frequency', 'GHz', FrequencyList,  
                                    'TE11-HE11 Conv Length', ' ', TE11HE11ConvLenList, 'CWG Straight Section Length', 'mm', CWGStraightSectionLength,  
                                    plotxrange='[:]',plotyrange='[:]', labels = 'True', subplot_columns = 3)  
   
    if warning_oldtab == True:
        print('WARNING - Used old sorted scanned parameters tables from disk. Tables may not be up to date. Run with PostProcessor with option  -r True')

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("p", help="Path of results folder", default = '.')
    parser.add_argument("-t", "--timestamp", help="Time Stamp, default='latest'", default='latest')
    parser.add_argument("-r", "--retabulate", type = bool, help="Retabulate scan parameters list, default=False", default=False)
    args = parser.parse_args()
    main(args)
