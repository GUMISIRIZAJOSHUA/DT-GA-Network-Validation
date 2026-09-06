import json
import glob
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================
# Load S0 multi-run files
# ============================

files = sorted(glob.glob("results/S0_run*.json"))

if len(files) == 0:
    print("No S0 files found")
    exit()


all_rtt = []
run_mean = []
run_names = []


for f in files:

    with open(f, "r") as file:
        data = json.load(file)

    rtts = []

    # Correct format:
    # data["packets"][i]["rtt"]

    if "packets" in data:

        for packet in data["packets"]:

            if "rtt" in packet:
                rtts.append(packet["rtt"])


    if len(rtts) > 0:

        rtts = np.array(rtts)

        all_rtt.extend(rtts)

        run_mean.append(np.mean(rtts)*1000)
        run_names.append(os.path.basename(f))

        print(
            os.path.basename(f),
            "packets:",
            len(rtts),
            "mean RTT(ms):",
            np.mean(rtts)*1000
        )


all_rtt=np.array(all_rtt)



# ============================
# Statistics
# ============================

print("\n======================")
print("S0 FINAL STATISTICS")
print("======================")

print("Total packets:",len(all_rtt))

print("Mean RTT(ms):",
      np.mean(all_rtt)*1000)

print("STD RTT(ms):",
      np.std(all_rtt)*1000)

print("P50 RTT(ms):",
      np.percentile(all_rtt,50)*1000)

print("P95 RTT(ms):",
      np.percentile(all_rtt,95)*1000)

print("P99 RTT(ms):",
      np.percentile(all_rtt,99)*1000)

print("Minimum RTT(ms):",
      np.min(all_rtt)*1000)

print("Maximum RTT(ms):",
      np.max(all_rtt)*1000)



# ============================
# Figure 1 RTT distribution
# ============================

plt.figure(figsize=(8,5))

plt.hist(all_rtt*1000,bins=30)

plt.xlabel("RTT (ms)")
plt.ylabel("Packet count")

plt.title("S0 RTT Distribution")

plt.grid(True)

plt.savefig(
    "S0_RTT_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# ============================
# Figure 2 RTT sequence
# ============================

plt.figure(figsize=(8,5))

plt.plot(
    range(len(all_rtt)),
    all_rtt*1000,
    marker="o",
    markersize=3
)

plt.xlabel("Packet index")
plt.ylabel("RTT (ms)")

plt.title("S0 Packet RTT Variation")

plt.grid(True)

plt.savefig(
    "S0_RTT_sequence.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# ============================
# Figure 3 Run comparison
# ============================

plt.figure(figsize=(10,5))

plt.bar(
    range(1,len(run_mean)+1),
    run_mean
)

plt.xlabel("Validation run")
plt.ylabel("Mean RTT (ms)")

plt.title("S0 Mean RTT Across 10 Runs")

plt.grid(True)

plt.savefig(
    "S0_run_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



print("\n======================")
print("Figures generated:")
print("S0_RTT_distribution.png")
print("S0_RTT_sequence.png")
print("S0_run_comparison.png")
print("======================")
