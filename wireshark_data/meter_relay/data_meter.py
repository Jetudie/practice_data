import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

DIRECTORY = "./test4"
FILE_NAME = "meter_try4" # name of json file
DATA_FILE = DIRECTORY + "/" + FILE_NAME + ".json"
SOURCE_IP = "192.168.1.27" # IP address of source
DESTINATION_IP = "192.168.1.13" # IP address of destination
SOURCE_PACKET = "00:00:40:41" # Packet of triggering signal
RECEIVED_PACKET = "00:4f:46:46:00" # Packet received of triggered signal
OUTPUT_FILE = DIRECTORY + "/" + 'Time_' + FILE_NAME + '.json'
OUTPUT_IMAGE = DIRECTORY + "/" + 'Time_' + FILE_NAME + '.png'
TITLE_OF_IMAGE = "Elapsed Time"

Time = []
with open(DATA_FILE, "r") as read_data:
    data = json.load(read_data)
data_length = len(data)
print("length:", data_length)
print("data type", type(data))

for n in range(data_length):
    if 'ip' in data[n]['_source']['layers']:
        ip_src = data[n]['_source']['layers']['ip']['ip.src']
        if ip_src == SOURCE_IP:
            if 'rtps' in data[n]['_source']['layers']:
                if 'rtps.sm.id_tree' in data[n]['_source']['layers']['rtps']:
                    if 'serializedData' in data[n]['_source']['layers']['rtps']['rtps.sm.id_tree']:
                        if 'rtps.issueData' in data[n]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']:
                            issueData = data[n]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']['rtps.issueData']
                            if SOURCE_PACKET in issueData :
                                t1 = float(data[n]['_source']['layers']['frame']['frame.time_epoch'])
                                # print("t1 = ", t1)
                                for i in range(data_length-n):
                                    n2 = n+i
                                    if 'ip' in data[n2]['_source']['layers']:
                                        ip_dst = data[n2]['_source']['layers']['ip']['ip.src']
                                    if ip_dst == DESTINATION_IP:
                                        if 'rtps' in data[n2]['_source']['layers']:
                                            if 'rtps.sm.id_tree' in data[n2]['_source']['layers']['rtps']:
                                                if 'serializedData' in data[n2]['_source']['layers']['rtps']['rtps.sm.id_tree']:
                                                    if 'rtps.issueData' in data[n2]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']:
                                                        issueData2 = data[n2]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']['rtps.issueData']
                                                        if RECEIVED_PACKET in issueData2 :
                                                            t2 = float(data[n2]['_source']['layers']['frame']['frame.time_epoch'])
                                                            # print("t2 = ", t2)
                                                            td = t2 - t1
                                                            Time.append(td)
                                                            break

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