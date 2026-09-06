import json
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress


# ============================================
# Publication Quality Figures
# ============================================

print("==============================")
print("PUBLICATION FIGURE GENERATION")
print("==============================")


# -----------------------------
# Load experimental results
# -----------------------------

files = sorted(
    glob.glob("results/S*_loss*.json")
)

loss = []
pdr = []
mean_rtt = []
p95_rtt = []
std_rtt = []


for f in files:

    with open(f,'r') as file:
        data=json.load(file)


    loss.append(
        data["loss_rate"]*100
    )

    pdr.append(
        data["PDR"]
    )


    rtt=np.array(
        data["RTT"]
    )


    mean_rtt.append(
        np.mean(rtt)*1000
    )


    p95_rtt.append(
        np.percentile(rtt,95)*1000
    )


    std_rtt.append(
        np.std(rtt)*1000
    )



loss=np.array(loss)
pdr=np.array(pdr)
mean_rtt=np.array(mean_rtt)
p95_rtt=np.array(p95_rtt)
std_rtt=np.array(std_rtt)



# ============================================
# Figure 1: PDR vs Loss with Regression
# ============================================


reg = linregress(
    loss,
    pdr
)


plt.figure(figsize=(8,5))


plt.scatter(
    loss,
    pdr,
    s=90
)


plt.plot(
    loss,
    reg.intercept + reg.slope*loss,
    linewidth=2
)


plt.xlabel(
    "Packet Loss Rate (%)",
    fontsize=13
)

plt.ylabel(
    "Packet Delivery Ratio (%)",
    fontsize=13
)


plt.title(
    "Packet Delivery Reliability Under Loss",
    fontsize=15
)


plt.text(
    0.05,
    0.15,
    f"$R^2$ = {reg.rvalue**2:.3f}\np = {reg.pvalue:.4e}",
    transform=plt.gca().transAxes,
    fontsize=12
)


plt.grid(True)

plt.tight_layout()


plt.savefig(
    "PUB_PDR_vs_LOSS.png",
    dpi=600
)

plt.close()



# ============================================
# Figure 2: RTT vs Loss
# ============================================


reg2=linregress(
    loss,
    mean_rtt
)


plt.figure(figsize=(8,5))


plt.errorbar(
    loss,
    mean_rtt,
    yerr=std_rtt,
    marker='o',
    markersize=8,
    capsize=5,
    linewidth=2
)


plt.plot(
    loss,
    reg2.intercept+reg2.slope*loss,
    linestyle="--",
    linewidth=2
)



plt.xlabel(
    "Packet Loss Rate (%)",
    fontsize=13
)


plt.ylabel(
    "Mean RTT (ms)",
    fontsize=13
)


plt.title(
    "Latency Behaviour Under Packet Loss",
    fontsize=15
)



plt.text(
    0.05,
    0.85,
    f"$R^2$ = {reg2.rvalue**2:.3f}\np = {reg2.pvalue:.4f}",
    transform=plt.gca().transAxes,
    fontsize=12
)



plt.grid(True)

plt.tight_layout()


plt.savefig(
    "PUB_RTT_vs_LOSS.png",
    dpi=600
)

plt.close()



# ============================================
# Figure 3: P95 Tail Latency
# ============================================


plt.figure(figsize=(8,5))


plt.plot(
    loss,
    p95_rtt,
    marker="s",
    markersize=9,
    linewidth=2
)



plt.xlabel(
    "Packet Loss Rate (%)",
    fontsize=13
)


plt.ylabel(
    "P95 RTT (ms)",
    fontsize=13
)


plt.title(
    "Tail Latency Behaviour",
    fontsize=15
)


plt.grid(True)


plt.tight_layout()


plt.savefig(
    "PUB_P95_RTT.png",
    dpi=600
)


plt.close()



# ============================================
# Figure 4: Combined Summary
# ============================================


fig,ax1=plt.subplots(
    figsize=(8,5)
)


ax1.plot(
    loss,
    pdr,
    marker='o',
    linewidth=2
)


ax1.set_xlabel(
    "Packet Loss Rate (%)"
)


ax1.set_ylabel(
    "PDR (%)"
)



ax2=ax1.twinx()


ax2.plot(
    loss,
    mean_rtt,
    marker='s',
    linewidth=2
)


ax2.set_ylabel(
    "Mean RTT (ms)"
)



plt.title(
    "Overall Network Performance Degradation"
)


plt.grid(True)


plt.tight_layout()


plt.savefig(
    "PUB_COMBINED_PERFORMANCE.png",
    dpi=600
)


plt.close()



# ============================================
# Save summary table
# ============================================


table=pd.DataFrame({

    "Loss (%)":loss,
    "PDR (%)":pdr,
    "Mean RTT (ms)":mean_rtt,
    "P95 RTT (ms)":p95_rtt,
    "STD RTT (ms)":std_rtt

})


table.to_csv(
    "publication_results_table.csv",
    index=False
)



print("==============================")
print("FIGURES GENERATED")
print("==============================")


print("""
PUB_PDR_vs_LOSS.png
PUB_RTT_vs_LOSS.png
PUB_P95_RTT.png
PUB_COMBINED_PERFORMANCE.png
publication_results_table.csv
""")
