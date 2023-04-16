"""
Slade Brooks
brooksl@mail.uc.edu
Dan Cuppoletti
04.14.23

Far Field Determination Code

This class takes input of multiple .tdms
microphone data files and processes them
to determine the range of frequencies that
can be considered to be in the acoustic far
field. It also features plotting functions for
NB spectra and OASPL.
"""

import numpy as np
import nptdms as nptd
import scipy as sp
import matplotlib.pyplot as plt
import glob


class micData():
    """
    This class takes input of multiple .tdms
    microphone data files and processes them
    to determine the range of frequencies that
    can be considered to be in the acoustic far
    field. It also features plotting functions for
    NB spectra and OASPL.

    Attributes
    ----------
    fs : int
        Microphone sampling frequency.
    samptime : int
        Data sampling time.
    N : int
        Number of data points.
    data : dict
        Dictionary containing each .tdms file's data.
    nmics : int
        Number of microphones in each data set.
    corData : dict
        Dictionary containing the corrected data for each file.
    pData : dict
        Dictionary containing the filtered and corrected data for each file.

    Methods
    -------
    dataProcess(corfac, critfreqs=np.array([100, 100000]), border=5)
        Apply correction factor and butterworth filter to data.
    oaspl(filenum)
        Compute the OASPL for each mic of a given file.
    narrowband(filenum, binwidth=5)
        Compute the narrowband spectra of each mic of a given file.
    """
    def __init__(self, path, fs, samptime, single=False):
        """
        Reads in the list of data files into numpy arrays
        in a dictionary. Also sets up variables with data
        collection info for later use.

        Parameters
        ----------
        path : string
            Path to folder with .tdms files.
        fs : int
            Sampling frequency (Hz).
        samptime : int
            Sampling time (s).
        single : bool, default = False
            Flag for passing a single file instead of folder.
        """
        # set up collection info
        self.fs = fs     # sampling frequency
        self.samptime = samptime        # sampling time
        self.N = fs*samptime      # number of data points

        # make dictionary for data
        self.data = {}

        # make list of files from folder
        if single == False:
            files = glob.glob(path + "*.tdms")
        elif single == True:
            files = [path]

        # go through each file
        for i in range(len(files)):
            # read in file
            tdmsfile = nptd.TdmsFile.read(files[i])

            # go thru group in file
            for group in tdmsfile.groups():
                # make data array
                tempdata = np.empty([len(group.channels()), self.N])

                # go thru each channel in group
                k = 0
                for channel in group.channels():
                    # store data in array
                    tempdata[k, :] = channel
                    k += 1
            # add data to dictionary
            self.data["data{0}".format(i)] = tempdata

        # get number of mics
        self.nmics = len(self.data["data0"])

    def dataProcess(self, corfac, critfreqs=np.array([100, 100000]), border=5):
        """
        Processes the data by correcting with given
        correction factor and then doing a butterworth
        bandpass filter.

        Parameters
        ----------
        corfac : np.ndarray
            Array of correction factor for each mic.
        critfreqs : np.ndarray, default = np.array([100, 100000])
            Array of crtifreqs.
        border : int, default = 5
            Butterworth filter order.
        """
        # apply correction factor to each file
        self.corData = self.data.copy()
        for key in self.data:
            for i in range(len(self.data[key])):
                self.corData[key][i, :] = self.data[key][i, :]*corfac[i]

        # apply butterworth filter
        self.pData = self.corData.copy()
        # setup bworth
        fh = self.fs/2
        [b, a] = sp.signal.butter(border, critfreqs/fh, "bandpass")
        for key in self.data:
            for i in range(len(self.data[key])):
                self.pData[key][i, :] = sp.signal.filtfilt(b, a, self.corData[key][i, :])

    def oaspl(self, filenum):
        """
        Computes the OASPL of each mic for a
        specified data file.

        Parameters
        ----------
        filenum : int
            Data file index to report.

        Returns
        -------
        oaspls : np.ndarray
            Array with OASPL for each mic in data file.
        """
        oaspls = np.empty(len(self.pData["data{0}".format(filenum)]))
        for i in range(len(self.pData["data{0}".format(filenum)])):
            # calculate oaspl
            rms = np.sqrt(np.mean(np.square(self.pData["data{0}".format(filenum)][i,:])))
            oaspls[i] = np.array(20*np.log10(rms/20e-6))

        return oaspls
    
    def narrowband(self, filenum, binwidth=5):
        """
        Computes the narrowband spectra of each mic
        for a specified data file.

        Parameters
        ----------
        filenum : int
            Data file index to report.
        binwidth : int, default = 5
            Desired frequency bin width.

        Returns
        -------
        spls : np.ndarray
            Array of spl for each frequency bin.
        freqs : np.ndarray
            Array of plotting frequencies.
        """
        # set up bins
        bw = binwidth
        bins = self.fs//bw
        n = self.N//bins
        T = self.samptime/n

        # for ease, pull single data file first
        datafile = self.pData["data{0}".format(filenum)]
        spls = np.empty([self.nmics, bins//2])

        # loop through mics
        for i in range(self.nmics):
            # split data to ensembles
            pDataens = np.array_split(datafile[i], n)

            # compute fft
            fft = np.array([np.abs(np.fft.fft(pDataens[k])) for k in range(n)])

            # take rms
            rms = np.sqrt(np.sum((2*fft/bins)**2, axis=0)/n)

            # convert to SPL and store
            spls[i, :] = 20*np.log10(rms[:bins//2]/20e-6)

        # get plotting frequencies
        freqs = np.fft.fftfreq(bins, T/(bins-1))[:bins//2]

        return spls, freqs


if __name__ == "__main__":
    # testing
    path = "C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab" \
            "\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50" \
            "\\mic6inplane\\data0.tdms"
    micData = micData(path, 204800, 5, True)

    corFac = np.array([0.9964, 0.9945, 0.99894, 0.99841, 1.00117, 0.99957, 0.99798, 0.9902])

    micData.dataProcess(corFac)
    # print(micData.oaspl(0))
    spls, freqs = micData.narrowband(0, 5)
    plt.semilogx(freqs, spls[6], label="Mic 6")
    plt.semilogx(freqs, spls[0], label="Mic 0")
    plt.legend()
    plt.xlim([100, 100000])
    plt.grid()
    plt.show()