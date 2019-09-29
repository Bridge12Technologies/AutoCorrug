
def create_type1_plot_files(run_directory, datafile, plot_variable1, plot_variable1_units, parameter1, parameter1_units,
                            plotxrange = '[:]', plotyrange = '[:]', labels='False',plot_title = ' '):
    import string, os

    pltfile = datafile + '.plt'
    titlefont = 'font "Helvetica,18"'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'
    ls_start = 1

    with open(pltfile,'w') as file:
        file.write('set term windows \n')
        if os.path.exists('gnuplot-linestyles.plt'):
            file.write('load "gnuplot-linestyles.plt" \n')
        file.write('set label' + '"' + run_directory + '"' + 'left at screen 0.05, screen 0.9425'
                   + plotidentifierfont + '\n')
        file.write('set key noenhanced \n')
        file.write('set datafile missing "nan" \n')
        file.write('clear \n')
        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set grid \n')
        file.write('set title "' + plot_title + '"' + titlefont + '\n')
        file.write('set xlabel "' + parameter1 + ' (' + parameter1_units+ ')"'+ '\n')
        file.write('set ylabel "' + plot_variable1 + ' (' + plot_variable1_units + ')"'+ '\n')
        file.write('set datafile separator ","' + '\n')
        file.write('set xrange ' + plotxrange + '\n')
        file.write('set yrange ' + plotyrange + '\n')
        file.write('plot "' + datafile + '"  u 1:2 with lp ls ' + str(ls_start) +  "t  ''")
        if labels == 'True':
            file.write(' , "' + datafile + '"  u 1:2:3 with labels center offset 0, 1 notitle ')
            # can also use 0, 1 boxed notittle
        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return


def create_type2_plot_files(run_directory, datafile, plot_variable1, plot_variable1_units, parameter1,
                            parameter1_units, parameter1_range, parameter2, parameter2_units, parameter2_range,
                            legend,plotxrange ='[:]',plotyrange = '[:]', labels='False', plot_title = ' '):
    import string, os

    pltfile = datafile + '.plt'
    titlefont = 'font "Helvetica,18"'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'
    ls_start = 1
    with open(pltfile,'w') as file:
        file.write('set term windows \n')
        if os.path.exists('gnuplot-linestyles.plt'):
            file.write('load "gnuplot-linestyles.plt" \n')
        file.write('set label' + '"' + run_directory + '"' + 'left at screen 0.05, screen 0.9425'
                   + plotidentifierfont + '\n')
        file.write('set datafile missing "nan" \n')
        file.write('set key noenhanced \n')
        file.write('clear \n')
        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set grid \n')
        file.write('set title "' + plot_title + '" ' + titlefont + '\n')
        file.write('set xlabel "' + parameter1 + ' (' + parameter1_units+ ')"'+ '\n')
        file.write('set ylabel "' + plot_variable1 + ' (' + plot_variable1_units + ')"'+ '\n')
        file.write('set datafile separator ","' + '\n')
        file.write('set xrange ' + plotxrange + '\n')
        file.write('set yrange ' + plotyrange + '\n')

        file.write('plot "' + datafile + '"  u 1:2 with lp ls ' + str(ls_start) + " t  '" + legend[0] +"'")
        if labels == 'True':
            file.write(' , "' + datafile + '"  u 1:' + str(2) + ':' + str(2+len(parameter2_range)) +
                       ' with labels center offset 0, 1 notitle ')   # can also use 0, 1 boxed notittle
        for i in range (1,len(parameter2_range)):
            file.write(' , "' + datafile + '"  u 1:' + str(i+2)+' with lp ls ' + str(ls_start+i) + " t '" +
                       str(legend[i]) +"'")
            if labels == 'True':
                file.write(' , "' + datafile + '"  u 1:' +str(i+2)+':' + str(i+2+len(parameter2_range)) +
                           ' with labels center offset 0, 1 notitle')

        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return

def create_subplot_files(run_directory, datafiles, plot_variable1, plot_variable1_units, parameter1,
                            parameter1_units, parameter1_range, parameter2, parameter2_units, parameter2_range,
                            parameter3, parameter3_units, parameter3_range, legend, subplot_title, plot_title = '',
                            subplot_columns = 2, plotxrange ='[:]',plotyrange = '[:]', labels='False'):

    import string, os

    subplot_rows = int(len(parameter3_range))/subplot_columns +1

    datafile_prefix = parameter3 + '-' + parameter2 + '-' + parameter1 + '-' + plot_variable1
    datafile_prefix.replace(" ", "-")

    pltfile = datafile_prefix + '.plt'
    keyfont = 'font "Helvetica,12"'
    titlefont = 'font "Helvetica,12" noenhanced'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'
    labelfont = 'font "Helvetica,14" noenhanced'
    ticsfont = 'font "Helvetica,14"'
    pointsize = 1.0
    keyspacing = 0.5
    keysamplen = 1

    MP_LEFT = 0.1
    MP_RIGHT = 0.95
    MP_BOTTOM = 0.1
    MP_TOP = 0.9
    MP_GAP = 0.15
    xlabel_offset = 'offset 0,0'
    ylabel_offset = 'offset 4,0'
    title_offset = 'offset 0,0.0'

    ls_start = 1
    with open(pltfile,'w') as file:
        # file.write('set term windows \n')  # - can't change the terminal in multiplot mode
        if os.path.exists('gnuplot-multiplot-linestyles.plt'):
            file.write('load "gnuplot-multiplot-linestyles.plt" \n')
        file.write('set label' + '"' + run_directory + '"' + ' left at screen 0.05, screen 0.98'
                   + plotidentifierfont + '\n')
        file.write('clear \n')
        file.write('set datafile missing "nan" \n')
        file.write('MP_LEFT = ' + str(MP_LEFT) + '\n')
        file.write('MP_RIGHT = ' + str(MP_RIGHT) + '\n')
        file.write('MP_BOTTOM = ' + str(MP_BOTTOM) + '\n')
        file.write('MP_TOP = ' + str(MP_TOP) + '\n')
        file.write('MP_GAP = ' + str(MP_GAP) + '\n')
        file.write('set multiplot layout ' + str(int(subplot_rows)) + ',' + str(subplot_columns) + ' rowsfirst ' +
                   'margins MP_LEFT, MP_RIGHT, MP_BOTTOM, MP_TOP spacing MP_GAP''\n')
        file.write('set key noenhanced \n')
        file.write('set pointsize  ' + str(pointsize) + '\n')
        file.write('set key ' + keyfont + '\n')
        file.write('set key spacing ' + str(keyspacing) + '\n')
        file.write('set key samplen ' + str(keysamplen) + '\n')
        file.write('set tics ' + ticsfont + '\n')

        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set grid \n')

        file.write('set xlabel "' + parameter1 + ' (' + parameter1_units+ ')" '+  labelfont + ' ' +
                   xlabel_offset + '\n')
        file.write('set ylabel "' + plot_variable1 + ' (' + plot_variable1_units + ')" ' + labelfont + ' ' +
                   ylabel_offset + '\n')
        file.write('set datafile separator ","' + '\n')
        file.write('set xrange ' + plotxrange + '\n')
        file.write('set yrange ' + plotyrange + '\n')

        for subplot_count in range (0, len(datafiles)):
            if datafiles[subplot_count] is not None:
                file.write('set title "' + parameter3 + ' = ' + str(parameter3_range[subplot_count]) +
                            ' '+ parameter3_units + '" ' + titlefont + ' ' + title_offset + '\n')
                file.write('plot "' + datafiles[subplot_count] + '"  u 1:2 with lp ls ' + str(ls_start) +
                        " t  '" + legend[0] + "'")
                if labels == 'True':
                    file.write(' , "' + datafiles[subplot_count] + '"  u 1:' + str(2) + ':' +
                            str(2+len(parameter2_range)) + ' with labels ' + labelfont +
                            ' center offset 0, 0.5 notitle ')
                                # can also use 0, 1 boxed notittle
                for i in range (1,len(parameter2_range)):
                    file.write(' , "' + datafiles[subplot_count] + '"  u 1:' + str(i+2)+' with lp ls ' +
                            str(ls_start+i) + " t '" + str(legend[i]) + "'")
                    if labels == 'True':
                        file.write(' , "' + datafiles[subplot_count] + '"  u 1:' +str(i+2)+':' +
                                str(i+2+len(parameter2_range)) + ' with labels ' + labelfont +
                                ' center offset 0, 0.5 notitle')
                file.write('\n')
        file.write('\n')
        file.write('unset multiplot' + '\n')
        file.write('pause -1 "hit any key to continue"')

    return

def create_plot_files_2V_2A_P2Sing_1Datafile(run_directory, sim_directory, datafile, plot_variable1, plot_variable1_units,
                            plot_variable2, plot_variable2_units, xlabel, xlabel_units, ylabel, ylabel_units,
                            y2label, y2label_units, plot_title = ' '):
    import string, os

    pltfile = run_directory + '/' + datafile + '.plt'
    titlefont = 'font "Helvetica,18"'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'
    ls_start = 1
    with open(pltfile,'w') as file:
        file.write('set term windows \n')
        if os.path.exists('gnuplot-linestyles.plt'):
            file.write('load "gnuplot-linestyles.plt \n')
        file.write('set label' + '"' + run_directory + '/' + sim_directory + '"' + 'left at screen 0.05, screen 0.9425'
                   + plotidentifierfont + '\n')
        file.write('set datafile missing "nan" \n')
        file.write('set key noenhanced \n')
        file.write('clear \n')
        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set auto \n')
        file.write('set grid \n')
        file.write('set title "' + plot_title + '" ' + titlefont + '\n')
        file.write('set xlabel "' + xlabel + ' (' + xlabel_units + ')" \n')
        file.write('set ylabel "' + ylabel + ' (' + ylabel_units + ')" \n')
        file.write('set y2label "'+ y2label + ' (' + y2label_units + ')" \n')
        file.write('set ytics nomirror \n')
        file.write('set y2tics nomirror \n')
        file.write('set yrange [] \n')
        plottext = 'plot "'+ datafile + '" u 1:2  with l ls ' + str(ls_start) + ' t  "' + plot_variable1 +'" , '
        plottext = plottext + '"' + datafile +'" u 1:3  axes x1y2 with l ls ' + str(ls_start+1) + ' t  "' + \
                   plot_variable2 +'"'
        file.write(plottext)
        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return


def create_plot_files_2V_2A_P2Sing_2Datafile(run_directory, sim_directory, datafile1, datafile2, plot_variable1,
                                             plot_variable1_units, plot_variable2, plot_variable2_units,xlabel,
                                             xlabel_units, ylabel, ylabel_units, y2label, y2label_units,
                                             plot_title = ' '):
    import string, os

    pltfile = run_directory + '/' + 'cav_B0_profile.plt'
    titlefont = 'font "Helvetica,18"'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'
    ls_start = 1

    with open(pltfile,'w') as file:
        file.write('set term windows \n')
        if os.path.exists('gnuplot-linestyles.plt'):
            file.write('load "gnuplot-linestyles.plt" \n')
        file.write('set label' + '"' + run_directory + '/' + sim_directory + '"' + 'left at screen 0.05, screen 0.9425'
                   + plotidentifierfont + '\n')
        file.write('set datafile missing "nan" \n')
        file.write('clear \n')
        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set auto \n')
        file.write('set grid \n')
        file.write('set title "' + plot_title + '"' + titlefont + '\n')
        file.write('set xlabel "' + xlabel + ' (' + xlabel_units + ')" \n')
        file.write('set ylabel "' + ylabel + ' (' + ylabel_units + ')" \n')
        file.write('set y2label "'+ y2label + ' (' + y2label_units + ')" \n')
        file.write('set ytics nomirror \n')
        file.write('set y2tics nomirror \n')
        plottext = 'plot "'+ datafile1 + '" u 1:2  with l ls ' + str(ls_start) + ' t  "' + plot_variable1 +'" , '
        plottext = plottext + '"' + datafile2 +'" u 1:2  axes x1y2 with l ls ' + str(ls_start+1) + ' t  "' +  \
                   plot_variable2 +'"'
        file.write(plottext)
        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return

def create_plot_files_2V_2A_P2Range_2Datafile(run_directory,datafile1,plot_variable1,plot_variable1_units,datafile2,plot_variable2,plot_variable2_units,
                                              parameter1,parameter1_units,parameter1_range,legend1,parameter2,parameter2_units,parameter2_range,legend2,
                                              plotxrange ='[:]',plotyrange='[:]',ploty2range='[:]',plot_title=' ',labels='False'):
    import string, os

    os.chdir(run_directory)
    pltfile = parameter1 + '-' + parameter2 + '-' + plot_variable1 + '-' + plot_variable2 + '.plt'
    title = plot_variable1 + ' and ' + plot_variable2
    titlefont = 'font "Helvetica,18"'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'
    ls_start = 1

    with open(pltfile,'w') as file:
        file.write('set term windows \n')
        if os.path.exists('gnuplot-linestyles.plt'):
            file.write('load "gnuplot-linestyles.plt" \n')
        file.write('set label' + '"' + run_directory + '"' + 'left at screen 0.05, screen 0.9425'
                   + plotidentifierfont + '\n')
        file.write('set datafile missing "nan" \n')
        file.write('set key noenhanced \n')
        file.write('clear \n')
        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set auto \n')
        file.write('set grid \n')
        file.write('set title "' + title + '"' + titlefont + '\n')
        file.write('set xlabel "' + parameter1 + ' (' + parameter1_units + ')" \n')
        file.write('set ylabel "' + plot_variable1 + ' (' + plot_variable1_units + ')" \n')
        file.write('set y2label "'+ plot_variable2 + ' (' + plot_variable2_units + ')" \n')
        file.write('set ytics nomirror \n')
        file.write('set y2tics nomirror \n')

        file.write('plot "' + datafile1 + '"  u 1:2 with lp ls ' + str(ls_start) + " t  '" + legend1[0] + "'")
        if labels == 'True':
            file.write(' , "' + datafile1 + '"  u 1:' + str(2) + ':' + str(2 + len(parameter2_range)) +
                       ' with labels center offset 0, 1 notitle ')  # can also use 0, 1 boxed notittle
        for i in range(1, len(parameter2_range)):
            file.write(' , "' + datafile1 + '"  u 1:' + str(i + 2) + ' with lp ls ' + str(ls_start + i) + " t '" + str(
                legend1[i]) + "'")
            if labels == 'True':
                file.write(' , "' + datafile1 + '"  u 1:' + str(i + 2) + ':' + str(i + 2 + len(parameter2_range)) +
                           ' with labels center offset 0, 1 notitle')

        ls_start = ls_start + len(parameter2_range)
        file.write(' , "' + datafile2 + '"  u 1:2 axes x1y2 with lp ls ' + str(ls_start) + " t  '" + legend2[0] + "'")
        if labels == 'True':
            file.write(' , "' + datafile2 + '"  u 1:2:' + str(3 + len(parameter2_range)) +
                       ' axes x1y2 with labels center offset 0, 1 notitle ')  # can also use 0, 1 boxed notittle

        for j in range(1, len(parameter2_range)):
            file.write(' , "' + datafile2 + '"  u 1:' + str(j + 2) + ' axes x1y2 with lp ls ' + str(ls_start + j) + " t '" + str(
                legend2[j]) + "'")
            if labels == 'True':
                file.write(' , "' + datafile2 + '"  u 1:' + str(j + 2) + ':' + str(j + 2 + len(parameter2_range)) +
                           ' axes x1y2 with labels center offset 0, 1 notitle')

        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return


def create_mapfile(run_directory, mapfile, parameter1, parameter1_range, parameter1_units, 
parameter2, parameter2_range, parameter2_units, plot_variable1, plot_variable1_units, plot_variable2, plot_variable2_units, plotxrange ='[:]',
                                              plotyrange = '[:]', plot_title = ' ', labels='False'):
    import string, os

    os.chdir(run_directory)
    pltfile = parameter1 + '-' + parameter2 + '-' + plot_variable1 + '-' + plot_variable2 + '-map.plt'
    title = plot_variable2 + '-' + plot_variable1 + ' map for (' + parameter1 + ', ' + parameter2 + ')'
    titlefont = 'font "Helvetica,16"'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'
    ls_start = 1
    lenparameter2 = len(parameter2_range)
    with open(pltfile,'w') as file:
        file.write('set term windows \n')
        if os.path.exists('gnuplot-linestyles.plt'):
            file.write('load "gnuplot-linestyles.plt" \n')
        file.write('set label' + '"' + run_directory + '"' + 'left at screen 0.05, screen 0.9425'
                   + plotidentifierfont + '\n')
        file.write('set datafile missing "nan" \n')
        file.write('set key noenhanced \n')
        file.write('clear \n')
        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set auto \n')
        file.write('set grid \n')
        file.write('set title "' + title + '"' + titlefont + '\n')
        file.write('set xlabel "' + plot_variable2 + ' (' + plot_variable2_units + ')" \n')
        file.write('set ylabel "' + plot_variable1 + ' (' + plot_variable1_units + ')" \n')

        file.write('plot ')
        
        for i in range(0, lenparameter2):
            if labels == 'True':
                file.write(' "' + mapfile + '"  u ' + str(3*i+1) + ':' + str(3*i+2) + ' smooth uniq with lp ls ' + str(ls_start+i) + ' t "", "' 
                + mapfile + '"  u ' + str(3*i+1) + ':' + str(3*i+2) + ':' + str(3*i+3) + ' t "" with labels, ')
            else:
                file.write(' "' + mapfile + '"  u ' + str(3*i+1) + ':' + str(3*i+2) + ' smooth uniq with lp ls ' + str(ls_start+i) + 
                ' t "'+ str(parameter2) + ' = ' + str(parameter2_range[i]) + ' ' + parameter2_units + '", ')

        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return


def create_plotfile_spent_beam_dist_hist(run_directory, sim_directory):
    import os,string,shutil,math
    titlefont = 'font "Helvetica,18"'
    title = 'Spent Beam Distribution'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'

    with open(run_directory + '/' +'plot_spent_beam_dist_hist.plt','w') as pltfile:
        pltfile.write('set term windows \n')
        if os.path.exists('gnuplot-linestyles.plt'):
            pltfile.write('load "gnuplot-linestyles.plt" \n')
        pltfile.write('set label' + '"' + run_directory + '/' + sim_directory  + '"'
                      + 'left at screen 0.05, screen 0.9425' + plotidentifierfont + '\n')
        pltfile.write('set datafile missing "nan" \n')
        pltfile.write('clear \n')
        pltfile.write('set auto \n')
        pltfile.write('unset mouse \n')
        pltfile.write('set title "'+title+ '"'+titlefont+'\n')
        pltfile.write('set xlabel "Voltage (kV)" \n')
        pltfile.write('set ylabel "Num Particles (a.u.)" \n')
        pltfile.write('set boxwidth 0.8 relative \n')
        pltfile.write('set style fill solid 1.0 \n')
        plottext = 'plot "output_spent_beam_dist_hist.out" u 2:1 t "" w boxes \n'
        pltfile.write(plottext)
        pltfile.write('pause -1 "hit any key to continue"')

    return    #plot_spent_beam_dist_hist
