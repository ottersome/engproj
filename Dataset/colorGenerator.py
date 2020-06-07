from numpy.random import rand
import pandas as pd
colors = []
for i in range(40):
    #Format : <id,r,g,b>
    colors.append([i,rand(),rand(),rand()])
df = pd.DataFrame(colors)
df.to_csv('colorMapping.csv',index=False,header=False)

