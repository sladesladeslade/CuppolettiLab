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
    """
    def __init__(self, path, fs, samptime):
        """
        Reads in the list of data files into numpy arrays
        in a dictionary. Also sets up variables with data
        collection info for later use.

        :param_path: path to folder with .tdms files
        :param_fs: sampling frequency (Hz)
        :param_samptime: sampling time (s)
        :returns: dictionary with data array for each file
        """
        # set up collection info
        self.fs = fs     # sampling frequency
        self.samptime = samptime        # sampling time
        self.N = fs*samptime      # number of data points

        # make dictionary for data
        self.data = {}

        # make list of files from folder
        files = glob.glob(path + "*.tdms")

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

        :param_corfac: np array of correction factor for each mic
        :param_critfreqs: np array of crtifreqs
        :param_border: butterworth order
        :returns: dictionary with processed data
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

        return self.pData

    def oaspl(self, filenum):
        """
        Computes the OASPL of each mic for each
        data file.

        :param_filenum: data file index to report
        :returns: OASPL for each mic in data file
        """


if __name__ == "__main__":
    # testing
    path = "C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab" \
            "\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50" \
            "\\mic6inplane\\"
    micData = micData(path, 204800, 5)

    corFac = np.array([0.9964, 0.9945, 0.99894, 0.99841, 1.00117, 0.99957, 0.99798, 0.9902])
    print(micData.data["data0"])
    print(micData.dataProcess(corFac)["data0"])