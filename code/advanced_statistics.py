import json
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd


print("==============================")
print("ADVANCED STATISTICAL ANALYSIS")
print("==============================")


# -----------------------------
# Load data
# -----------------------------

files = sorted(glob.glob("results/S*_loss*.json"))

loss_values = []
PDR_values = []
RTT_values = []
P95_values = []


for f in files:

    with open(f,'r') as file:
        data=json.load(file)


    loss=data["loss_rate"]*100

    loss_values.append(loss)

    PDR_values.append(
        data["PDR"]
    )

    rtt=np.array(data["RTT"])

    RTT_values.append(
        np.mean(rtt)*1000
    )

    P95_values.append(
        np.percentile(rtt,95)*1000
    )


# dataframe

df=pd.DataFrame({

    "Loss (%)":loss_values,
    "PDR (%)":PDR_values,
    "Mean RTT (ms)":RTT_values,
    "P95 RTT (ms)":P95_values

})


print("\nDATA SUMMARY")
print(df)


df.to_csv(
    "advanced_statistics_summary.csv",
    index=False
)



# -----------------------------
# ANOVA
# -----------------------------


def run_anova(values,name):

    groups=[]

    for i in range(len(values)):
        groups.append([values[i]])


    result=f_oneway(*groups)


    print("\n",name)
    print("----------------")
    print("F-value =",result.statistic)
    print("p-value =",result.pvalue)



run_anova(
    PDR_values,
    "PDR ANOVA"
)


run_anova(
    RTT_values,
    "RTT ANOVA"
)


run_anova(
    P95_values,
    "P95 RTT ANOVA"
)



# -----------------------------
# Tukey test
# -----------------------------

print("\nTukey Test: PDR")

tukey=pairwise_tukeyhsd(
    endog=PDR_values,
    groups=loss_values,
    alpha=0.05
)

print(tukey)



with open(
    "tukey_results.txt",
    "w"
) as f:

    f.write(str(tukey))



# -----------------------------
# Figures
# -----------------------------


plt.figure(figsize=(8,5))

plt.boxplot(
    [PDR_values],
    labels=["PDR"]
)

plt.ylabel(
    "Packet Delivery Ratio (%)"
)

plt.title(
    "PDR Statistical Distribution"
)

plt.grid(True)

plt.savefig(
    "PDR_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



plt.figure(figsize=(8,5))

plt.boxplot(
    [RTT_values],
    labels=["RTT"]
)

plt.ylabel(
    "RTT (ms)"
)

plt.title(
    "Latency Statistical Distribution"
)

plt.grid(True)

plt.savefig(
    "RTT_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



print("\n==============================")
print("ADVANCED ANALYSIS COMPLETE")
print("==============================")

print("""
Generated:

advanced_statistics_summary.csv
tukey_results.txt
PDR_boxplot.png
RTT_boxplot.png
""")
