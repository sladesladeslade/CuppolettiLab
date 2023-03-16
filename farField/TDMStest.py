# Slade Brooks
# brooksl@mail.uc.edu
# 03.14.23

import numpy as np
import nptdms as nptd
import scipy as sp
import matplotlib.pyplot as plt

tdms_file = nptd.TdmsFile.read("C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50\\mic6inplane\\data12.tdms")
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
# set up frequency bins
binwidth = 50
nb = int(fs/binwidth)    # num of bins

# testing data and filters
# t = np.linspace(0, 5, len(N))
# plt.plot(t, data[0,:], label="raw")
# plt.plot(t, corData[0,:], label="corrected")
# plt.plot(t, pData[0,:], label="filtered")
# plt.legend()
# plt.show()

# take FFT of signal
pFFT = pData.copy()
for i in range(len(pData)):
    pFFT[i, :] = sp.fft.fft(pData.copy()[i, :])

# FFT plotting test
# freqs = np.linspace(0, fs, N)
# plt.semilogx(freqs, pFFT[0,:])
# plt.xlim([Wl, Wh])
# plt.show()

# do Xn(fn) for each bin
Xtemp = np.empty([np.shape(pData)[1]])
Xn = np.empty([len(pFFT), nb])
for i in range(len(pFFT)):
    for k in range(nb):
        start = k*binwidth
        end = start + binwidth + k*binwidth
        pts = np.arange(start, end, 1)
        for p in range(binwidth):
            Xtemp[p] = 2*(np.abs(pFFT[i, pts[p]]))**2
        Xn[i, k] = np.mean(Xtemp)

# do NB (SPL) for each bin w/ Xn(fn)
nbSPL = np.empty([len(Xn), nb])
for i in range(len(Xn)):
    nbSPL[i, :] = 10*np.log10(Xn[i, :]/(pref**2))

plotfreq = np.arange(0, fs, binwidth)
plt.semilogx(plotfreq, nbSPL[0,:])
plt.xlim([Wl, Wh])
plt.xlabel("$f \ (Hz)$")
plt.ylabel("$SPL \ (dB)$")
plt.ylim(30, 150)
plt.grid()
plt.show()

# do OASPL - for single mic across entire frequency range
# take rms of filtered data
rms = np.sqrt(np.mean(pData[0,:]**2))
# do OASPL calc w/ rms
oaspl = 20*np.log10(rms/pref)
print(oaspl)