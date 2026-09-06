import json
import numpy as np
import matplotlib.pyplot as plt


files = [
    ("S0", "results/S0_summary.json", 0.0),
    ("S1", "results/S1_loss5.json", 0.05),
    ("S2", "results/S2_loss10.json", 0.10),
    ("S3", "results/S3_loss20.json", 0.20),
    ("S4", "results/S4_loss30.json", 0.30)
]


loss = []
pdr = []
rtt = []


for name, filename, loss_value in files:

    with open(filename, "r") as f:
        data = json.load(f)


    loss.append(loss_value * 100)


    # PDR
    pdr.append(data["PDR"])


    # RTT calculation
    if "RTT" in data:
        mean_rtt = np.mean(data["RTT"]) * 1000
    else:
        mean_rtt = data["mean_RTT"] * 1000


    rtt.append(mean_rtt)



print("========================")
print("FINAL VALIDATION RESULTS")
print("========================")


for i in range(len(loss)):

    print(
        files[i][0],
        "Loss =", loss[i],
        "%",
        "PDR =", pdr[i],
        "%",
        "Mean RTT =",
        round(rtt[i],4),
        "ms"
    )


# -----------------------
# Plot PDR
# -----------------------

plt.figure(figsize=(7,5))

plt.plot(
    loss,
    pdr,
    marker="o"
)

plt.xlabel("Packet Loss Rate (%)")
plt.ylabel("Packet Delivery Ratio (%)")
plt.title("Packet Delivery Performance")
plt.grid(True)

plt.savefig(
    "PDR_vs_Loss.png",
    dpi=300,
    bbox_inches="tight"
)



# -----------------------
# Plot RTT
# -----------------------

plt.figure(figsize=(7,5))

plt.plot(
    loss,
    rtt,
    marker="o"
)

plt.xlabel("Packet Loss Rate (%)")
plt.ylabel("Mean RTT (ms)")
plt.title("Latency Performance")
plt.grid(True)

plt.savefig(
    "RTT_vs_Loss.png",
    dpi=300,
    bbox_inches="tight"
)


print("\nGenerated:")
print("PDR_vs_Loss.png")
print("RTT_vs_Loss.png")
