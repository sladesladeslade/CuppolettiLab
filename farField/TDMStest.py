# Slade Brooks
# brooksl@mail.uc.edu
# 03.14.23

import numpy as np
import nptdms as nptd

tdms_file = nptd.TdmsFile.read("C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50\\mic6inplane\\data0.tdms")
# for group in tdms_file.groups():
    # group_name = group.name
    # for channel in group.channels():
    #     channel_name = channel.name
    #     # Access dictionary of properties:
    #     properties = channel.properties
    #     # Access numpy array of data for channel:
    #     data = channel[:]

fs = 204800     # sampling frequency
samptime = 5        # sampling time
N = fs*samptime      # number of data points

for group in tdms_file.groups():

    # make data array
    data = np.empty([len(group.channels()), N])

    # loop thru to store data in array
    i = 0
    # go thru each channel in grouo
    for channel in group.channels():
        # go thru each data point
        for k in range(len(channel)):
            # store in horizontal array
            data[i, k] = channel[k]
        i += 1