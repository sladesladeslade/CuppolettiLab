# Slade Brooks
# brooksl@mail.uc.edu
# 03.14.23

import numpy as np
import nptdms as nptd
import scipy as sp
import matplotlib.pyplot as plt

tdms_file = nptd.TdmsFile.read("C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab"
                               "\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50"
                               "\\mic6inplane\\data12.tdms")
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
pref = 20e-6    # ref p for calcs

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
pData = sp.signal.filtfilt(b, a, corData)

# FFT - for single mic across frequency bins
# set up bins
bw = 50         # binwidth
bins = fs//bw
w = N//bins      # bin width in data points

# do FFT on each bin
fft1 = np.empty([bins, w//2])
for i in range(0, N, w):
    buck = i//w
    fft1[buck, :] = 2/w*np.abs(np.fft.fft(corData[0, i:(i+w)])[:w//2])

# take rms of the daterp
rms1 = np.empty(bins)
for i in range(bins):
    rms1[i] = np.sqrt(np.mean(np.square(fft1[i,:])))

# convert to SPL
spl1 = 20*np.log10(rms1/pref)

# plotting frews
freqs = np.arange(0, fs, bw)

# plot NBSPL
plt.semilogx(freqs, spl1)
plt.show()

# take rms of filtered data
rms = np.sqrt(np.mean(np.square(pData[0,:])))

# do OASPL calc w/ rms
oaspl = 20*np.log10(rms/pref)
print("OASPL: {0:.2f}".format(oaspl))