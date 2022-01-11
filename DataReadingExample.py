#!/usr/bin/python
# An example of reading data from a file
import numpy as np
from GRANDRootTrees import *
# import ROOT

# tadccounts = GRANDADCCountsTree("stored_data.root")
#
# tadccounts.GetEvent(2)
# print(tadccounts.evt_id, tadccounts.det_time[0], tadccounts.trace_x[0])


tefield = GRANDEfieldTree("stored_data.root")
tadccounts = GRANDADCCountsTree("stored_data.root")
tvoltage = GRANDVoltageTree("stored_data.root")
#tefield = GRANDADCCountsTree("stored_data.root")

tefield.GetEvent(2)
print(tefield.evt_id, tefield.det_time[0], tefield.trace_x[0][0])#, tadccounts)
#print("post")

# Here are experiments to avoid the crash - not working yet!

for tree in tefield.tree.GetListOfFriends():
	tefield.tree.RemoveFriend(tree.GetTree())

for tree in tadccounts.tree.GetListOfFriends():
	tadccounts.tree.RemoveFriend(tree.GetTree())
	
for tree in tvoltage.tree.GetListOfFriends():
	tvoltage.tree.RemoveFriend(tree.GetTree())

tadccounts.tree.Delete()
tvoltage.tree.Delete()
tefield.tree.Delete()
#tefield.file.Close()
print("aaa")

#tefield.RemoveFriend(tadccounts.tree)
#print(tadccounts.tree.GetListOfFriends())
#exit()
for tree in tefield.tree.GetListOfFriends():
	print(tree)
#tefield.RemoveFriend(tvoltage.tree)
#tvoltage.RemoveFriend(tadccounts.tree)
