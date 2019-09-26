#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies Inc.
#   37 Loring Drive, Framingham, MA
#   Date Created: 2 September 2017
#   Last Modified: 2 September 2017
#   Executes the program

#   Ver 1.0 20170902 - 

def aggregate_results(dirname_top,postprocess_list):
    import corrug_utils,plot_utils,os
    import linecache

    # Ignore the scripts folder during postprocessing. There is nothing to postprocess in the scripts folder
    param_list = [x for x in os.listdir(dirname_top) if x != "scripts"]
    
    for param_name in param_list:
        os.chdir(dirname_top)

        #Read unit of current param from the 'param_val_unit' file in variation step1
        filename=dirname_top+'\\'+param_name+'\\'+'step1'+'\\'+'param_val_unit'
        param_unit=linecache.getline(filename, 2).rstrip()
        
        plot_utils.create_parameter_plot_files(dirname_top,param_name,param_unit)

        results_summary_file_name = dirname_top+'\\vary_'+param_name+'_modal_power.out'     
        results_summary_file = open(results_summary_file_name,'a')
        results_summary_file.write('#'+param_name+'('+param_unit+')'+', TE11_power(a.u.), TE11_phase(deg), HE11_power(a.u.), HE11_phase(deg), HE12_power(a.u.), HE12_phase(deg), Return Loss (dB) ')
        results_summary_file.write('\n')
        dirname_low = dirname_top+'\\'+param_name

        # ensure that directories go as step1, step2, ... step9, step10, ..
        reordered_step=[]
        for element in os.listdir(dirname_low):
            reordered_step.append(int(element[4:]))
        reordered_step.sort(reverse=True)

        step_list=[]
        for element in reordered_step:
            step_list.append('step'+str(element))
            
        for step in step_list:
            dirname_step = dirname_low+'\\'+step
            param_val,run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss = corrug_utils.extract_simulation_results(dirname_step)
            if run_fail == False:
                results_summary_file.write(str(param_val))
                results_summary_file.write(', ')
                results_summary_file.write(str(TE11_amp**2))
                results_summary_file.write(', ')
                results_summary_file.write(str(TE11_phase))
                results_summary_file.write(', ')
                results_summary_file.write(str(HE11_amp**2))
                results_summary_file.write(', ')
                results_summary_file.write(str(HE11_phase))
                results_summary_file.write(', ')
                results_summary_file.write(str(HE12_amp**2))
                results_summary_file.write(', ')
                results_summary_file.write(str(HE12_phase))
                results_summary_file.write(', ')
                results_summary_file.write(str(Return_Loss))
                results_summary_file.write('\n')
            else:
                results_summary_file.write('#')
                results_summary_file.write(str(param_val))
                results_summary_file.write(' Run Failed ')
                results_summary_file.write('\n')
        results_summary_file.close()
    return
