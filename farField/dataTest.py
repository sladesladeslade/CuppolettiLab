# Slade Brooks
# brooksl@mail.uc.edu
# 03.14.23

import numpy as np
import nptdms as nptd
import scipy as sp
import matplotlib.pyplot as plt

# read in tdms
tdms_file = nptd.TdmsFile.read("C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab"
                               "\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50"
                               "\\mic6inplane\\data0.tdms")

# set up collection info
fs = 204800     # sampling frequency
samptime = 5        # sampling time
N = fs*samptime      # number of data points
pref = 20e-6    # ref p for calcs

# make data array from file
for group in tdms_file.groups():
    # make data array for each group
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

# get number of mics
nmics = len(data)

# correct data w/ correction factors
corFac = np.array([0.9964, 0.9945, 0.99894, 0.99841, 1.00117, 0.99957, 0.99798, 0.9902])
corData = data.copy()
for i in range(nmics):
    corData[i, :] = data.copy()[i, :]*corFac[i]

# butterworth filter on pressure vals
Wl = 100        
Wh = 100000
critfreqs = np.array([Wl, Wh])      # critical freqs
fh = fs/2       # nyquist freq
border = 5      # bworth order

# setup bworth
[b, a] = sp.signal.butter(border, critfreqs/fh, "bandpass")

# do bworth on data
pData = sp.signal.filtfilt(b, a, corData)

# set up bins
bins = fs//50        # 50 Hz width
n = N//bins
T = samptime/(bins*n)

# for each bin do calcs
fft = np.empty([bins, n//2])
rms = np.empty(bins)
spl = np.empty(bins)
freqs = np.empty_like(fft)
for i in range(0, N, n):
    buck = i//n
    # take the fft
    fft[buck,:] = 2/n*np.abs(np.fft.fft(pData[6, i:i+n])[:n//2])

    freqs[buck,:] = np.fft.fftfreq(n, T)[:n//2]

    # take the rms
    rms[buck] = np.sqrt(np.mean(np.square(fft[buck,:])))

    # calculate SPL
    spl[buck] = 20*np.log10(rms[buck]/pref)

# plot NBSPL
plt.semilogx(freqs, fft)
plt.xlim([10**2, 2*10**4])
plt.ylim(20)
plt.grid()
plt.show()

# do OASPL calc w/ rms
for mic in range(nmics):
    # take rms of filtered data
    rms = np.sqrt(np.mean(np.square(pData[mic,:])))
    # get OASPL
    oaspl = 20*np.log10(rms/pref)
    # print OASPLs
    print("OASPL {0}: {1:.2f}".format(mic, oaspl))