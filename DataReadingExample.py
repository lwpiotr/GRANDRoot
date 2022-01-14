#!/usr/bin/python
# An example of reading data from a file
import numpy as np
from GRANDRootTrees import *
# import ROOT

tadccounts = GRANDADCCountsTree("stored_data.root")

tadccounts.GetEvent(2)
print("ADCCounts readout: tadccounts.evt_id, tadccounts.det_time[0], tadccounts.trace_x[0]")
print(tadccounts.evt_id, tadccounts.det_time[0], tadccounts.trace_x[0])


tefield = GRANDEfieldTree("stored_data.root")
#tvoltage = GRANDVoltageTree("stored_data.root")

tefield.GetEvent(2)
print("\nEfield readout: tefield.evt_id, tefield.det_time[0], tefield.trace_x[0][0], tadccounts.evt_id")
print("The evt_id of tadccounts changed to 4 when tefield event with evt_id 4 was requested")
print(tefield.evt_id, tefield.det_time[0], tefield.trace_x[0][0], tadccounts.evt_id)

