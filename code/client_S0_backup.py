import socket
import json
import time
import os
import statistics

HOST = "127.0.0.1"
PORT = 5000

NUM_RUNS = 10
PACKETS_PER_RUN = 10

os.makedirs("results", exist_ok=True)

all_rtt = []

for run in range(1, NUM_RUNS + 1):

    print("\n======================")
    print(f"Starting S0 run {run}")
    print("======================")

    run_data = {
        "run": run,
        "packets": [],
        "successful_ack": 0,
        "failed_packets": 0
    }

    for pkt in range(1, PACKETS_PER_RUN + 1):

        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        start = time.time()

        try:
            client.connect((HOST, PORT))

            message = {
                "seq": pkt,
                "run": run,
                "timestamp": start,
                "signal": [0.12, 0.25, 0.38, 0.51, 0.67],
                "power": -5
            }

            client.send(json.dumps(message).encode())

            data = client.recv(4096)

            end = time.time()

            rtt = end - start

            response = json.loads(data.decode())

            print(
                f"Run {run} Packet {pkt}: "
                f"ACK received, RTT={rtt:.6f}s"
            )

            run_data["successful_ack"] += 1

            run_data["packets"].append(
                {
                    "packet": pkt,
                    "rtt": rtt,
                    "response": response
                }
            )

            all_rtt.append(rtt)

        except Exception as e:

            print(
                f"Run {run} Packet {pkt}: FAILED {e}"
            )

            run_data["failed_packets"] += 1

        finally:
            client.close()


    filename = f"results/S0_run{run}.json"

    with open(filename, "w") as f:
        json.dump(run_data, f, indent=4)

    print(f"Saved {filename}")


# summary file

summary = {
    "total_runs": NUM_RUNS,
    "total_packets": NUM_RUNS * PACKETS_PER_RUN,
    "successful_ack": len(all_rtt),
    "PDR": len(all_rtt) / (NUM_RUNS * PACKETS_PER_RUN) * 100,
    "mean_RTT": statistics.mean(all_rtt),
    "RTT_STD": statistics.stdev(all_rtt) if len(all_rtt) > 1 else 0,
    "min_RTT": min(all_rtt),
    "max_RTT": max(all_rtt)
}


with open("results/S0_summary.json", "w") as f:
    json.dump(summary, f, indent=4)


print("\n======================")
print("S0 MULTI-RUN SUMMARY")
print("======================")
print(json.dumps(summary, indent=4))
