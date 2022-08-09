import numpy as np
from tqdm import trange
from time import sleep
def BaselineCorrect(raw, Peak_references, weighting_matrix, baseline_method, onset_value, offset_value,
                                ref_start, ref_end, extra_data):
    print('baseline_mothod is',baseline_method)
    """BaselineCorrect.m is a function used by Bergen EEG & fMRI Toolbox plugin
       for EEGLAB in order to adjust the corected and / or non corrected data
       to a given baseline.
       Copyright(C) 2009 The Bergen fMRI Group
       Bergen fMRI Group, Department 
       of Biological and Medical Psychology, University
       of Bergen, Norway Written by Emanuel Neto, 2009 netoemanuel @ gmail.com
       Last Modified on 3 - Nov - 2009 12: 04:11"""
    intro = trange(0,desc='Baseline Correction Initializing', leave=True)
    t = trange(100, desc='Applying Changes', leave=True)
    data=raw.get_data()*1e6
    n_channels = len(raw.ch_names)
    TR = Peak_references[0,2] - Peak_references[0,1]
    precision = 0.000001
    # Baseline Methods: variable "baseline_method"
    #0 - No method
    # 1 - Based on WHOLE ARTIFACT to zero
    # 2 - Average of precedent silent gap
    #ref_start will be used has the begining of the precedent silent gap
    #ref_end will be used has the end of the precedent silent gap
    #3 - Average of time interval
    # extra_data if = 1 then the data not afected by the gradient artifacts
    # removal process is also ajusted for the specifyed baseline.

    #h = waitbar(0, 'Baseline correction of Artifacts');
    #hw = findobj(h, 'Type', 'Patch');
    #set(hw, 'EdgeColor', [1 1 0], 'FaceColor', [1 1 0]);
    #precision = 0.000001;
    lim1 = Peak_references.shape[1]
    lim2 = weighting_matrix.shape[1]
    residual = lim1 - lim2 + 1
    #residual = lim2 - lim1 + 1;
#baseline=my_switcher(baseline_method)
    if baseline_method==1:
        baseline = 0
        for ch in range(1, n_channels+1):
            for i in range(residual,lim1+1):
                starter = int(np.fix(Peak_references[0, i - 1] + onset_value))
                ender = int(np.fix(Peak_references[0, i - 1] + offset_value))
                artif_average = np.mean(data[ch-1, starter:ender+1])
                adjust = baseline - artif_average
                if ch==18:
                    print('adjust is'+str(adjust))
                    print('artif_average is' + str(artif_average))

                if np.abs(adjust) > precision:
                    for j in range(starter,ender+1):
                        data[ch-1, j] = data[ch-1, j] + adjust

        st = Peak_references[0,residual-1] + onset_value
        en = Peak_references[0,lim1-1] + offset_value

    if baseline_method == 2:   # 2 - Average of precedent silent gap case
        for ch in range(1, n_channels+1):
            for i in range(residual, lim1 + 1):
                try:
                    baseline_start =int(np.fix(Peak_references[0, i - 1]  + ref_start))
                    baseline_end = int(np.fix(Peak_references[0, i - 1]  + ref_end))
                    baseline = np.mean(data[ch-1, baseline_start:baseline_end+1])
                except:
                    baseline = 0

                starter = int(np.fix(Peak_references[0, i - 1] + onset_value))
                ender = int(np.fix(Peak_references[0, i - 1] + offset_value))
                artif_average = np.mean(data[ch-1, starter:ender+1])
                adjust = baseline - artif_average
                if np.abs(adjust) > precision:
                    for j in range(starter,ender+1):
                        data[ch-1, j] = data[ch-1, j] + adjust

        st = Peak_references[0, residual - 1] + onset_value
        en = Peak_references[0, lim1 - 1] + offset_value

    if baseline_method==3:
        for ch in range(1, n_channels+1):
            for i in range(residual, lim1 + 1):
                try:
                    baseline_start = int(np.fix(Peak_references[0, i - 1] + ref_end))
                    baseline_end = int(np.fix(Peak_references[0, i - 1] + ref_start -1))
                    baseline = np.mean(data[ch - 1, baseline_start:baseline_end + 1])
                except:
                    baseline = 0

                starter = int(np.fix(Peak_references[0, i - 1]  + ref_start))
                ender = int(np.fix(Peak_references[0, i - 1] + ref_end))
                artif_average = np.mean(data[ch-1, starter:ender+1])
                adjust = baseline - artif_average
                if abs(adjust) > precision:
                    for j in range(starter,ender+1):
                        data[ch-1, j] = data[ch-1, j] + adjust

        st = Peak_references[0, residual - 1]  + ref_start
        en = Peak_references[0, lim1 - 1]  + ref_end

    print('baseline_mothod is', baseline_method)
# Shift also non corrected data
    if extra_data == 1:
        print('baseline_mothod is', baseline_method)
        boundary1 = int(np.fix(Peak_references[0,residual-1] + onset_value - 1)) # start  of fMRI gradients
        boundary2 = int(np.fix(Peak_references[0,lim1-1] + offset_value + 1))# % end of fMRI gradients
        for ch in range(1, n_channels+1):
            if baseline_method == 1:
                print('baseline_method is 1')
                baseline = 0
            else:
                baseline1 = np.mean(data[ch-1, st:st + TR+1])
                baseline2 = np.mean(data[ch-1, en:en + TR+1])

            #if baseline_method!=1:
             #   lim3 = len(data[ch-1,:])
             #   adjust = baseline1 - np.mean(data[ch-1, 1:boundary1+1])
              #  if np.abs(adjust) > precision:
               #     for i in range(1,boundary1+1):
                #        data[ch-1, i-1] = data[ch-1, i-1] + adjust

                #adjust = baseline2 - np.mean(data[ch-1, boundary2:])
                #if np.abs(adjust) > precision:
                #    for i in range(boundary2,lim3+1): #Channel could happen to turn disconected during recording
                 #       data[ch-1, i-1] = data[ch-1, i-1] + adjust

    return data

