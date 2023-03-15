# Slade Brooks
# brooksl@mail.uc.edu
# 03.14.23

import numpy as np
import nptdms as nptd
import scipy as sp

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

# correct data w/ correction factor
corFac = np.array([0.9964, 0.9945, 0.99894, 0.99841, 1.00117, 0.99957, 0.99798, 0.9902])
corData = data.copy()
for i in range(len(data)):
    corData[i, :] = data.copy()[i, :]*corFac[i]

# butterworth filter on pressure vals
# critical freqs
Wl = 100
Wh = 100000
critfreqs = np.array([Wl, Wh])

# nyquist freq
fh = fs/2

# bworth order
border = 5

# setup bworth
[b, a] = sp.signal.butter(border, critfreqs/fh, "bandpass")

# do bworth on data
sp.signal.filtfilt(b, a, corData)

# FFT - for single mic across frequency bins
    # set up frequency bins
    # do Xn(fn) for each bin
    # do NB (SPL) for each bin w/ Xn(fn)

# do OASPL - for single mic across entire frequency range
    # take rms of filtered data
    # do OASPL calc w/ rms