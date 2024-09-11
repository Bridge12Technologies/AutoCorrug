
def create_geometry_plotfile(run_directory,step_directory):
    import string, os

    # os.chdir(run_directory)
    pltfile =step_directory+'\\plotGeometry.plt'
    title = step_directory
    titlefont = 'font "Helvetica,18"'
    plotidentifierfont = 'font "Helvetica,9" noenhanced'

    with open(pltfile,'w') as file:
        file.write('set term windows \n')
        file.write('load "..\\\\gnuplot-linestyles.plt" \n')
        file.write('set label' + '"' + step_directory + '"' + 'left at screen 0.05, screen 0.9425'
                   + plotidentifierfont + '\n')
        file.write('set datafile missing "nan" \n')
        file.write('set key noenhanced \n')
        file.write('clear \n')
        file.write('set auto \n')
        file.write('unset mouse \n')
        file.write('set auto \n')
        file.write('set grid \n')
        file.write('set title "' + title + '"' + titlefont + '\n')
        file.write('set xlabel "Distance (mm)" \n')
        file.write('set ylabel "Radius (mm)" \n')

        file.write('plot "geometry.out" using 1:2 with l ls 1 lw 0.5')
        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return


def create_gnuplot_file_2parameters_1variable(run_directory,datafile1,plot_variable1,plot_variable1_units,
                                              parameter1,parameter1_units,parameter1_range,legend1,parameter2,parameter2_units,parameter2_range,
                                              plotxrange ='[:]',plotyrange='[:]',plot_title=' ',labels='False'):
    import string, os

    os.chdir(run_directory)
    pltfile = parameter1 + '-' + parameter2 + '-' + plot_variable1 + '-' +  '.plt'
    title = plot_variable1 
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
        file.write('\n')
        file.write('pause -1 "hit any key to continue"')

    return

def create_gnuplot_file_2parameters_2variables(run_directory,datafile1,plot_variable1,plot_variable1_units,datafile2,plot_variable2,plot_variable2_units,
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

def create_gnuplot_file_3parameters_1variable(run_directory,datafiles1,plot_variable1,plot_variable1_units,legend1,
                                                parameter1,parameter1_units,parameter1_range,
                                                parameter2,parameter2_units,parameter2_range,
                                                parameter3,parameter3_units,parameter3_range,
                                                subplot_title,plot_title='',subplot_columns=2,plotxrange='[:]',plotyrange='[:]',labels='False'):

    import string, os

    subplot_rows = int(len(parameter3_range))/subplot_columns +1

    datafile_prefix = parameter3 + '-' + parameter2 + '-' + parameter1 + '-' + plot_variable1
    datafile_prefix.replace(" ", "-")

    pltfile = datafile_prefix + '.plt'
    keyfont = 'font "Helvetica,10"'
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
    ylabel_offset = 'offset 2,0'
    title_offset = 'offset 0,0.0'

    ls_start = 1
    with open(pltfile,'w') as file:
        file.write('set term windows \n')  # - can't change the terminal in multiplot mode
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

        for subplot_count in range (0, len(datafiles1)):
            if datafiles1[subplot_count] is not None:
                file.write('set title "' + parameter3 + ' = ' + str(parameter3_range[subplot_count]) +
                            ' '+ parameter3_units + '" ' + titlefont + ' ' + title_offset + '\n')
                file.write('plot "' + datafiles1[subplot_count] + '"  u 1:2 with lp ls ' + str(ls_start) +
                        " t  '" + legend1[0] + "'")
                if labels == 'True':
                    file.write(' , "' + datafiles1[subplot_count] + '"  u 1:' + str(2) + ':' +
                            str(2+len(parameter2_range)) + ' with labels ' + labelfont +
                            ' center offset 0, 0.5 notitle ')
                                # can also use 0, 1 boxed notittle
                for i in range (1,len(parameter2_range)):
                    file.write(' , "' + datafiles1[subplot_count] + '"  u 1:' + str(i+2)+' with lp ls ' +
                            str(ls_start+i) + " t '" + str(legend1[i]) + "'")
                    if labels == 'True':
                        file.write(' , "' + datafiles1[subplot_count] + '"  u 1:' +str(i+2)+':' +
                                str(i+2+len(parameter2_range)) + ' with labels ' + labelfont +
                                ' center offset 0, 0.5 notitle')
                file.write('\n')
        file.write('\n')
        file.write('unset multiplot' + '\n')
        file.write('pause -1 "hit any key to continue"')

    return


def create_gnuplot_file_3parameters_2variables(run_directory,datafiles1,plot_variable1,plot_variable1_units,legend1,datafiles2,plot_variable2,plot_variable2_units,legend2,
                                                parameter1,parameter1_units,parameter1_range,
                                                parameter2,parameter2_units,parameter2_range,
                                                parameter3,parameter3_units,parameter3_range,subplot_title,plot_title='',
                                                subplot_columns=2,plotxrange='[:]',plotyrange='[:]',ploty2range='[:]',labels='False'):

    import string, os

    subplot_rows = int(len(parameter3_range))/subplot_columns +1

    datafile_prefix = parameter3 + '-' + parameter2 + '-' + parameter1 + '-' + plot_variable1 + '-' + plot_variable2
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
    y2label_offset = 'offset -5,0'
    title_offset = 'offset 0,0.0'

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
        file.write('set y2label "' + plot_variable2 + ' (' + plot_variable1_units + ')" ' + labelfont + ' ' +
                   y2label_offset + '\n')
        file.write('set datafile separator ","' + '\n')
        file.write('set xrange ' + plotxrange + '\n')
        file.write('set yrange ' + plotyrange + '\n')
        file.write('set y2range ' + ploty2range + '\n')
        file.write('set ytics nomirror \n')
        file.write('set y2tics nomirror \n')



        for subplot_count in range (1, len(parameter3_range)):
            ls_start = 1
            file.write('set title "' + parameter3 + ' = ' + str(parameter3_range[subplot_count]) +
            ' '+ parameter3_units + '" ' + titlefont + ' ' + title_offset + '\n')
            file.write('plot "' + datafiles1[0] + '"  u 1:2 with lp ls ' + str(ls_start) + " t  '" + legend1[0] + "'")

            if labels == 'True':
                file.write(' , "' + datafiles1[0] + '"  u 1:' + str(2) + ':' + str(2 + len(parameter2_range)) +
                    ' with labels center offset 0, 1 notitle ')  # can also use 0, 1 boxed notittle
            if labels == 'True':
                file.write(' , "' + datafiles1[subplot_count] + '"  u 1:' + str(2) + ':' + str(2 + len(parameter2_range)) +
                        ' with labels center offset 0, 1 notitle ')  # can also use 0, 1 boxed notittle
            for i in range(1, len(parameter2_range)):
                file.write(' , "' + datafiles1[subplot_count] + '"  u 1:' + str(i + 2) + ' with lp ls ' + str(ls_start + i) + " t '" + str(
                    legend1[i]) + "'")
                if labels == 'True':
                    file.write(' , "' + datafiles1[subplot_count] + '"  u 1:' + str(i + 2) + ':' + str(i + 2 + len(parameter2_range)) +
                            ' with labels center offset 0, 1 notitle')
            ls_start = ls_start + len(parameter2_range)

            for i in range(0, len(parameter2_range)):
                file.write(' , "' + datafiles2[i] + '"  u 1:' + str(i + 2) + ' with lp ls ' + str(ls_start + i) + " t '" + str(
                    legend1[i]) + "'")
                if labels == 'True':
                    file.write(' , "' + datafiles2[i] + '"  u 1:' + str(i + 2) + ':' + str(i + 2 + len(parameter2_range)) +
                            ' with labels center offset 0, 1 notitle')

            file.write(' , "' + datafiles2[subplot_count-len(datafiles1)] + '"  u 1:2 axes x1y2 with lp ls ' + str(ls_start) + " t  '" + legend2[0] + "'")
            file.write('\n')
        file.write('\n')
        file.write('unset multiplot' + '\n')
        file.write('pause -1 "hit any key to continue"')

    return

