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


if __name__ == "__main__":
    # testing
    path = "C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab" \
            "\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50" \
            "\\mic6inplane\\"
    micData = micData(path, 204800, 5)