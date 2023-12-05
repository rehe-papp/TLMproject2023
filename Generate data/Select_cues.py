import pandas as pd

indata = pd.read_csv("./Nelson-BRM-2004/Appendices .csv files/AppendixA1.csv")
indata = indata

cues = indata['Cues'].dropna().drop_duplicates()

#cues = cues_w_duplicates.drop_duplicates()
# algul 63396, pärast 4390 sõna
random_selection = cues.sample(n=100)
print(random_selection.values)

outdata = indata.where(indata['Cues'].isin(random_selection.values))
outdata.dropna(subset=['Cues'], inplace=True)
#print(outdata)
outdata.to_csv("cue_dataset.csv")
