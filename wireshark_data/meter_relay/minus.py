import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

DIRECTORY = "./test4"
FILE_NAME_A = "Time_meter_try4"
FILE_NAME_B = "Time_relay_try4"
DATA_FILE_A = DIRECTORY + "/" + FILE_NAME_A + ".json"
DATA_FILE_B = DIRECTORY + "/" + FILE_NAME_B + ".json"
OUTPUT_FILE = DIRECTORY + '/'+ 'Time_compare.json'
OUTPUT_IMAGE = DIRECTORY + '/' + 'Time_compare.png'
TITLE_OF_IMAGE = "Elapsed Time"

Time = []
with open(DATA_FILE_A, "r") as read_data1:
    data1 = json.load(read_data1)
with open(DATA_FILE_B, "r") as read_data2:
    data2 = json.load(read_data2)
data1_length = len(data1)
data2_length = len(data2)
print("data1 length:", data1_length)
print("data2 length:", data2_length)
print("data type", type(data1))

Time = []
# if size match
if data1_length == data2_length:
    for n in range(data1_length):
        time = data1[n] - data2[n]
        Time.append(time)

    
#print(Time)
sum = 0
for t in Time:
    sum = sum + t
    # print(t)

print("Average Time: ", sum/len(Time))
print("Total data: ", len(Time))

with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(Time, outfile)
#sns.kdeplot(Time)
#plt.hist(Time)
Time = pd.Series(Time, name = TITLE_OF_IMAGE)
sns.distplot(Time)
plt.savefig(OUTPUT_IMAGE)
plt.show()