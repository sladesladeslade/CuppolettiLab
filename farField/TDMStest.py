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

# take FFT of data
fft = np.empty([len(pData), N//2])
for i in range(len(pData)):
    fft[i,:] = 2/N*np.abs(np.fft.fft(pData[0,:])[:N//2])

# set up bins
bw = 50        # binwidth
bins = fs//bw

# split data into frequency bins

# take rms of each bin

# convert to SPL

# plotting freqs
freqs = np.arange(0, fs, bw)

# plot NBSPL
plt.semilogx(freqs, fft[0,:])
plt.xlim([10**2, 10**5])
plt.show()

# take rms of filtered data
rms = np.sqrt(np.mean(np.square(pData[0,:])))

# do OASPL calc w/ rms
oaspl = 20*np.log10(rms/pref)
print("OASPL: {0:.2f}".format(oaspl))