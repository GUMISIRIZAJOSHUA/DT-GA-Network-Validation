import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import csv


# Experimental data

loss = np.array([0,5,10,20,30])

pdr = np.array([
    100,
    94,
    91,
    76,
    72
])


rtt = np.array([
    0.2644,
    0.2424,
    0.2256,
    0.2271,
    0.2475
])


# ============================
# PDR regression
# ============================

pdr_reg = linregress(loss,pdr)


print("==============================")
print("STATISTICAL ANALYSIS")
print("==============================")


print("\nPDR vs Loss")
print("----------------")
print("Slope:",
      pdr_reg.slope)

print("R2:",
      pdr_reg.rvalue**2)

print("p-value:",
      pdr_reg.pvalue)



# ============================
# RTT regression
# ============================


rtt_reg = linregress(loss,rtt)


print("\nRTT vs Loss")
print("----------------")

print("Slope:",
      rtt_reg.slope)

print("R2:",
      rtt_reg.rvalue**2)

print("p-value:",
      rtt_reg.pvalue)



# ============================
# Save table
# ============================


with open(
    "statistical_summary.csv",
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "Loss (%)",
        "PDR (%)",
        "RTT (ms)"
    ])


    for i in range(len(loss)):
        writer.writerow([
            loss[i],
            pdr[i],
            rtt[i]
        ])



# ============================
# Figure 1
# ============================


plt.figure(figsize=(7,5))


plt.scatter(
    loss,
    pdr
)


plt.plot(
    loss,
    pdr_reg.intercept +
    pdr_reg.slope*loss
)


plt.xlabel(
    "Packet Loss Rate (%)"
)

plt.ylabel(
    "Packet Delivery Ratio (%)"
)

plt.title(
    "PDR Degradation Under Packet Loss"
)

plt.grid(True)


plt.savefig(
    "PDR_regression.png",
    dpi=300,
    bbox_inches="tight"
)



# ============================
# Figure 2
# ============================


plt.figure(figsize=(7,5))


plt.scatter(
    loss,
    rtt
)


plt.plot(
    loss,
    rtt_reg.intercept +
    rtt_reg.slope*loss
)


plt.xlabel(
    "Packet Loss Rate (%)"
)


plt.ylabel(
    "Mean RTT (ms)"
)


plt.title(
    "Latency Stability Under Packet Loss"
)


plt.grid(True)


plt.savefig(
    "RTT_regression.png",
    dpi=300,
    bbox_inches="tight"
)



print("\nGenerated files:")
print("statistical_summary.csv")
print("PDR_regression.png")
print("RTT_regression.png")
