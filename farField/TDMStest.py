# Slade Brooks
# brooksl@mail.uc.edu
# 03.14.23

import numpy as np
import nptdms as nptd

tdms_file = nptd.TdmsFile.read("C:\\Users\\spbro\\OneDrive - University of Cincinnati\\Cuppoletti Lab\\NearFieldAcousticDuctedRotor\\slade mic data\\20220725\\ducted\\tm0.50\\mic6inplane\\data0.tdms")
for group in tdms_file.groups():
    group_name = group.name
    for channel in group.channels():
        channel_name = channel.name
        # Access dictionary of properties:
        properties = channel.properties
        # Access numpy array of data for channel:
        data = channel[:]