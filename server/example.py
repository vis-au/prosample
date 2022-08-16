from pipeline import *

# Dataset, Linearization and Subdivision is chosen once
data = MOUNTAIN_PEAKS
lin = LinearizationReaderZOrder()
subd = SubdivisionCardinality(0.1)

# Selection is chosen dynamically
sel = SelectionMinimum(3)
sampler = Sampler(data, lin, subd, sel)
chunk = sampler.sample(sel)
print(chunk)

sel = SelectionMaximum(3)
sampler.update_selection(sel)
chunk = sampler.sample(sel)
print(chunk)
chunk = sampler.sample(sel)
print(chunk)
chunk = sampler.sample(sel)
print(chunk)

sel = SelectionRandom(42)
sampler.update_selection(sel)
chunk = sampler.sample(sel)
print(chunk)
