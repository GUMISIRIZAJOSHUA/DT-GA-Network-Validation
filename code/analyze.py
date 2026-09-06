import json
import os
import numpy as np

RESULT_DIR = "results"

runs = []

# Load S0_run1 to S0_run10
for i in range(1, 11):

    filename = f"{RESULT_DIR}/S0_run{i}.json"

    if os.path.exists(filename):

        with open(filename, "r") as f:
            data = json.load(f)

        rtts = []

        for p in data["packets"]:
            rtts.append(p["rtt"])

        rtts = np.array(rtts)

        run_result = {
            "run": i,
            "packets": len(rtts),
            "successful_ack": data["successful_ack"],
            "PDR": data["successful_ack"] /
                   len(rtts) * 100,

            "mean_RTT": float(np.mean(rtts)),
            "std_RTT": float(np.std(rtts)),
            "min_RTT": float(np.min(rtts)),
            "max_RTT": float(np.max(rtts)),
            "P50_RTT": float(np.percentile(rtts, 50)),
            "P95_RTT": float(np.percentile(rtts, 95)),
            "P99_RTT": float(np.percentile(rtts, 99))
        }

        runs.append(run_result)


# Combine all RTT values

all_rtt = []

for i in range(1, 11):

    filename = f"{RESULT_DIR}/S0_run{i}.json"

    with open(filename, "r") as f:
        data = json.load(f)

    for p in data["packets"]:
        all_rtt.append(p["rtt"])


all_rtt = np.array(all_rtt)


# Overall statistics

summary = {

    "total_runs": len(runs),

    "total_packets":
        len(all_rtt),

    "successful_ack":
        int(sum(r["successful_ack"] for r in runs)),

    "PDR":
        float(
            sum(r["successful_ack"] for r in runs)
            /
            len(all_rtt)
            * 100
        ),

    "mean_RTT":
        float(np.mean(all_rtt)),

    "STD_RTT":
        float(np.std(all_rtt)),

    "P50_RTT":
        float(np.percentile(all_rtt,50)),

    "P95_RTT":
        float(np.percentile(all_rtt,95)),

    "P99_RTT":
        float(np.percentile(all_rtt,99)),

    "minimum_RTT":
        float(np.min(all_rtt)),

    "maximum_RTT":
        float(np.max(all_rtt))
}


# Save detailed report

report = {

    "summary": summary,

    "individual_runs": runs
}


with open(
    f"{RESULT_DIR}/S0_statistical_report.json",
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=4
    )


# Print results

print("==============================")
print("S0 STATISTICAL VALIDATION")
print("==============================")

print(
    json.dumps(
        summary,
        indent=4
    )
)


print("\nRun-by-run RTT:")
print("----------------")

for r in runs:

    print(
        f"Run {r['run']}: "
        f"Mean RTT={r['mean_RTT']:.6f}s "
        f"P95={r['P95_RTT']:.6f}s "
        f"PDR={r['PDR']:.1f}%"
    )
