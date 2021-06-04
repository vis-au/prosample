from pipeline import *

# Requires file mountainPeaksData.csv to be in the input_files folder
# Linearizes file by 3 attributes (columns 2,3 and 4, since the first one is the ID)
linearization = LinearizationZOrderKD(MOUNTAIN_PEAKS, 3)
linearization.linearize()


