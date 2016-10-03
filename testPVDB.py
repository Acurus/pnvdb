from pvdb import PvdbRead
import pandas as pd

r = PvdbRead()
r.segmentation = 'false'
data = r.get_road_objects(899,inkluder=('metadata','egenskaper'))

print(data['objekter'][0].keys())
#df = pd.DataFrame(data)
#print(df.tail())
