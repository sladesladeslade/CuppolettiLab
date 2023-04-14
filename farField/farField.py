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


class micData():
    """
    This class takes input of multiple .tdms
    microphone data files and processes them
    to determine the range of frequencies that
    can be considered to be in the acoustic far
    field. It also features plotting functions for
    NB spectra and OASPL.
    """
    def __init__(self, files, fs, samptime):
        """
        Reads in the list of data files into numpy arrays.
        Also sets up variables with data collection info.

        :param_files: list of .tdms files (1 group)
        :param_fs: sampling frequency (Hz)
        :param_samptime: sampling time (s)
        """
        # set up collection info
        self.fs = 204800     # sampling frequency
        self.samptime = 5        # sampling time
        self.N = fs*samptime      # number of data points
        self.pref = 20e-6    # ref p for calcs

        # make dictionary for data
        data = {}

        # do this for each data file in loop
        data["data{0}".format(i)] = data[i, k]


if __name__ == "__main__":
    # testing
    micData = micData("C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab"
                        "\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50"
                        "\\mic6inplane\\data0.tdms", 204800, 5)