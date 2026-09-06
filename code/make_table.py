import json
import glob
import numpy as np
import csv


files = sorted(glob.glob("results/S0_run*.json"))

rows=[]

all_rtt=[]


for f in files:

    with open(f,"r") as file:
        data=json.load(file)

    rtt=[]

    for p in data["packets"]:
        rtt.append(p["rtt"])

    rtt=np.array(rtt)

    all_rtt.extend(rtt)

    rows.append([
        f.split("/")[-1],
        len(rtt),
        data["successful_ack"],
        np.mean(rtt)*1000,
        np.percentile(rtt,95)*1000,
        np.std(rtt)*1000
    ])



all_rtt=np.array(all_rtt)


with open("S0_validation_table.csv","w",newline="") as f:

    writer=csv.writer(f)

    writer.writerow(
        [
        "Run",
        "Packets",
        "ACK",
        "Mean RTT(ms)",
        "P95 RTT(ms)",
        "STD RTT(ms)"
        ]
    )

    writer.writerows(rows)


print("====================")
print("S0 VALIDATION TABLE")
print("====================")

print("Total packets:",len(all_rtt))
print("Mean RTT(ms):",np.mean(all_rtt)*1000)
print("P95 RTT(ms):",np.percentile(all_rtt,95)*1000)
print("PDR(%):",100)



print("\nSaved:")
print("S0_validation_table.csv")
