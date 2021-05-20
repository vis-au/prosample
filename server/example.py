from server.pipeline import *

# Dataset, Linearization and Subdivision is chosen once
data = MOUNTAIN_PEAKS
lin = LinearizationZOrder()
subd = SubdivisionStandard(0.1)
sampler = Sampler(data, lin, subd)

# Selection is chosen dynamically
sel = SelectionMinimum(3)
chunk = sampler.sample(sel)
print(chunk)

sel = SelectionMaximum(3)
chunk = sampler.sample(sel)
print(chunk)
chunk = sampler.sample(sel)
print(chunk)
chunk = sampler.sample(sel)
print(chunk)

sel = SelectionRandom(42)
chunk = sampler.sample(sel)
print(chunk)