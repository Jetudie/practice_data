import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = "meter_try4_json"
Time = []
with open(DATA_FILE, "r") as read_data:
    data = json.load(read_data)
data_length = len(data)
print("length:", data_length)
print("data type", type(data))

for n in range(data_length):
    if 'ip' in data[n]['_source']['layers']:
        ip_src = data[n]['_source']['layers']['ip']['ip.src']
        if ip_src == "192.168.1.27":
            if 'rtps' in data[n]['_source']['layers']:
                if 'rtps.sm.id_tree' in data[n]['_source']['layers']['rtps']:
                    if 'serializedData' in data[n]['_source']['layers']['rtps']['rtps.sm.id_tree']:
                        if 'rtps.issueData' in data[n]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']:
                            issueData = data[n]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']['rtps.issueData']
                            if "00:00:40:41" in issueData :
                                t1 = float(data[n]['_source']['layers']['frame']['frame.time_epoch'])
                                # print("t1 = ", t1)
                                for i in range(data_length-n):
                                    n2 = n+i
                                    if 'ip' in data[n2]['_source']['layers']:
                                        ip_src2 = data[n2]['_source']['layers']['ip']['ip.src']
                                    if ip_src2 == "192.168.1.13":
                                        if 'rtps' in data[n2]['_source']['layers']:
                                            if 'rtps.sm.id_tree' in data[n2]['_source']['layers']['rtps']:
                                                if 'serializedData' in data[n2]['_source']['layers']['rtps']['rtps.sm.id_tree']:
                                                    if 'rtps.issueData' in data[n2]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']:
                                                        issueData2 = data[n2]['_source']['layers']['rtps']['rtps.sm.id_tree']['serializedData']['rtps.issueData']
                                                        if "00:4f:46:46:00" in issueData2 :
                                                            t2 = float(data[n2]['_source']['layers']['frame']['frame.time_epoch'])
                                                            # print("t2 = ", t2)
                                                            t = t2 - t1
                                                            Time.append(t)
                                                            break

print(Time)
with open('Time.json', 'w') as outfile:
    json.dump(Time, outfile)
#sns.kdeplot(Time)
#plt.hist(Time)
Time = pd.Series(Time, name = "Elapsed Time")
sns.distplot(Time)
plt.savefig('Time.png')
plt.show()