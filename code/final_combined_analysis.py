import os
import json
import csv
import numpy as np
import matplotlib.pyplot as plt


RESULT_DIR = "results"

FILES = [
    ("S0", "S0_summary.json", 0),
    ("S1", "S1_loss5.json", 5),
    ("S2", "S2_loss10.json", 10),
    ("S3", "S3_loss20.json", 20),
    ("S4", "S4_loss30.json", 30),
    ("S5", "S5_loss40.json", 40),
    ("S6", "S6_loss50.json", 50),
]


loss_values = []
pdr_values = []
rtt_values = []
std_values = []
p95_values = []
received_values = []
lost_values = []


print("==============================")
print("FINAL COMBINED ANALYSIS")
print("==============================")


for name, filename, loss in FILES:

    filepath = os.path.join(RESULT_DIR, filename)

    with open(filepath, "r") as f:
        data = json.load(f)


    total = data.get("total_packets", 0)

    # Compatible with S0 and S1-S6 formats
    received = data.get(
        "received_packets",
        data.get("successful_ack", 0)
    )

    lost = data.get(
        "lost_packets",
        total - received
    )

    pdr = data.get(
        "PDR",
        (received / total) * 100
    )


    rtt_list = data.get(
        "RTT",
        []
    )

    if len(rtt_list) > 0:

        rtt_array = np.array(rtt_list)

        mean_rtt = np.mean(rtt_array) * 1000
        std_rtt = np.std(rtt_array) * 1000
        p95_rtt = np.percentile(
            rtt_array,
            95
        ) * 1000

    else:

        mean_rtt = data.get(
            "mean_RTT",
            0
        ) * 1000

        std_rtt = 0
        p95_rtt = 0


    loss_values.append(loss)
    pdr_values.append(pdr)
    rtt_values.append(mean_rtt)
    std_values.append(std_rtt)
    p95_values.append(p95_rtt)

    received_values.append(received)
    lost_values.append(lost)


    print(
        f"{name}: "
        f"Loss={loss}% "
        f"PDR={pdr:.2f}% "
        f"RTT={mean_rtt:.4f} ms"
    )



# ===============================
# CSV TABLE
# ===============================

with open(
    "final_validation_table.csv",
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "Scenario",
        "Loss (%)",
        "Received",
        "Lost",
        "PDR (%)",
        "Mean RTT (ms)",
        "STD RTT (ms)",
        "P95 RTT (ms)"
    ])


    for i,(name,_,_) in enumerate(FILES):

        writer.writerow([
            name,
            loss_values[i],
            received_values[i],
            lost_values[i],
            pdr_values[i],
            rtt_values[i],
            std_values[i],
            p95_values[i]
        ])


print("\nSaved:")
print("final_validation_table.csv")



# ===============================
# FIGURE 1 PDR vs LOSS
# ===============================

plt.figure(figsize=(7,5))

plt.plot(
    loss_values,
    pdr_values,
    marker="o"
)

plt.xlabel(
    "Packet Loss (%)"
)

plt.ylabel(
    "Packet Delivery Ratio (%)"
)

plt.title(
    "Packet Delivery Ratio vs Loss Rate"
)

plt.grid(True)

plt.savefig(
    "FINAL_PDR_vs_LOSS.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# ===============================
# FIGURE 2 RTT vs LOSS
# ===============================

plt.figure(figsize=(7,5))

plt.errorbar(
    loss_values,
    rtt_values,
    yerr=std_values,
    marker="o",
    capsize=4
)

plt.xlabel(
    "Packet Loss (%)"
)

plt.ylabel(
    "Mean RTT (ms)"
)

plt.title(
    "Latency Variation vs Loss Rate"
)

plt.grid(True)

plt.savefig(
    "FINAL_RTT_vs_LOSS.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# ===============================
# FIGURE 3 P95 RTT
# ===============================

plt.figure(figsize=(7,5))

plt.plot(
    loss_values,
    p95_values,
    marker="s"
)

plt.xlabel(
    "Packet Loss (%)"
)

plt.ylabel(
    "P95 RTT (ms)"
)

plt.title(
    "Tail Latency Behaviour"
)

plt.grid(True)

plt.savefig(
    "FINAL_P95_RTT.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# ===============================
# STATISTICS
# ===============================

try:

    from scipy.stats import linregress


    pdr_result = linregress(
        loss_values,
        pdr_values
    )

    rtt_result = linregress(
        loss_values,
        rtt_values
    )


    with open(
        "final_statistics.txt",
        "w"
    ) as f:

        f.write("PDR vs Loss\n")
        f.write("================\n")
        f.write(
            f"Slope: {pdr_result.slope}\n"
        )
        f.write(
            f"R2: {pdr_result.rvalue**2}\n"
        )
        f.write(
            f"p-value: {pdr_result.pvalue}\n\n"
        )


        f.write("RTT vs Loss\n")
        f.write("================\n")
        f.write(
            f"Slope: {rtt_result.slope}\n"
        )
        f.write(
            f"R2: {rtt_result.rvalue**2}\n"
        )
        f.write(
            f"p-value: {rtt_result.pvalue}\n"
        )


    print("Saved:")
    print("final_statistics.txt")


except Exception as e:

    print(
        "Statistics not generated:",
        e
    )



print("\n==============================")
print("FINAL ANALYSIS COMPLETE")
print("==============================")

print("\nGenerated:")
print("FINAL_PDR_vs_LOSS.png")
print("FINAL_RTT_vs_LOSS.png")
print("FINAL_P95_RTT.png")
print("final_validation_table.csv")
print("final_statistics.txt")
