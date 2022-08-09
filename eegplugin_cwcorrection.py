def eegplugin_cwcorrection( fig, try_strings, catch_strings):

    vers = 'CW Regression Tool 0.01';

    toolsmenu = fig.findobj('tag', 'tools');
    cwregressionmenu=uimenu(toolsmenu,'label','CW Regression Tool','separator','on','tag','CW Regression Tools');
    commando1 = [ try_strings.no_check '[EEG LASTCOM] = pop_cwregression( EEG );' catch_strings.new_and_hist ];
    submenu_cwregression=uimenu(cwregressionmenu,'label','Remove BCG/Hg Artifacts','tag','cwregression menu','callback',commando1);