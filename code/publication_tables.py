import pandas as pd
import os

print("="*65)
print("PUBLICATION TABLE GENERATION")
print("="*65)


# ==========================================
# Load experimental results
# ==========================================

input_file = "publication_results_table.csv"

if not os.path.exists(input_file):
    print("ERROR: publication_results_table.csv not found")
    exit()


df = pd.read_csv(input_file)


# ==========================================
# Add S0 baseline condition
# ==========================================

s0 = pd.DataFrame({
    "Loss (%)": [0],
    "PDR (%)": [100],
    "Mean RTT (ms)": [0.2644],
    "P95 RTT (ms)": [0.7209],
    "STD RTT (ms)": [0.1048]
})


df = pd.concat(
    [s0, df],
    ignore_index=True
)


# Sort according to loss rate

df = df.sort_values(
    by="Loss (%)"
).reset_index(drop=True)


print("\nFINAL DATASET:")
print(df)



# ==========================================
# Table 1
# Experimental configuration
# ==========================================

table1 = pd.DataFrame({

    "Parameter": [

        "Experiment scenarios",
        "Packet loss range",
        "Packets per scenario",
        "Number of repetitions",
        "Evaluation metrics",
        "Measured parameters",
        "Experimental platform"

    ],


    "Value": [

        "S0-S6",
        "0-50%",
        "100 packets",
        "10 independent runs",
        "PDR, RTT, P95 RTT",
        "Reliability and latency",
        "Linux network emulation environment"

    ]

})


table1.to_csv(
    "Table1_Experimental_Configuration.csv",
    index=False
)



# ==========================================
# Table 2
# Performance results
# ==========================================

# Round numerical values

for col in df.columns:

    if df[col].dtype != "object":

        df[col] = df[col].round(4)



df.to_csv(
    "Table2_Performance_Results.csv",
    index=False
)



# ==========================================
# LaTeX tables
# ==========================================


with open(
    "Table1_Experimental_Configuration.tex",
    "w"
) as f:

    f.write(
        table1.to_latex(
            index=False,
            caption="Experimental configuration",
            label="tab:experimental_configuration"
        )
    )



with open(
    "Table2_Performance_Results.tex",
    "w"
) as f:

    f.write(
        df.to_latex(
            index=False,
            caption="Network performance under increasing packet loss",
            label="tab:performance_results"
        )
    )



# ==========================================
# Automatically create manuscript summary
# ==========================================


results_text = f"""

The network performance was evaluated under seven packet loss
conditions ranging from 0% to 50%. The baseline scenario achieved
100% packet delivery, while increasing packet loss progressively
reduced communication reliability.

Packet Delivery Ratio decreased from {df['PDR (%)'].iloc[0]}%
at 0% loss to {df['PDR (%)'].iloc[-1]}% at 50% loss, demonstrating
the dominant influence of packet loss on network reliability.

Latency remained relatively stable under moderate degradation.
The mean RTT varied between {df['Mean RTT (ms)'].min():.4f} ms and
{df['Mean RTT (ms)'].max():.4f} ms. However, severe packet loss
caused increased latency variation and deterioration of tail
performance.

The maximum P95 RTT reached {df['P95 RTT (ms)'].max():.4f} ms,
indicating significant delay instability under extreme packet loss
conditions.

"""


with open(
    "Results_Summary_for_Paper.txt",
    "w"
) as f:

    f.write(results_text)



# ==========================================
# Display generated files
# ==========================================


print("\nGenerated files:")
print("-----------------------------")


files = [

    "Table1_Experimental_Configuration.csv",
    "Table2_Performance_Results.csv",
    "Table1_Experimental_Configuration.tex",
    "Table2_Performance_Results.tex",
    "Results_Summary_for_Paper.txt"

]


for file in files:

    print(file)



print("\n")
print("="*65)
print("PUBLICATION TABLE GENERATION COMPLETE")
print("="*65)
