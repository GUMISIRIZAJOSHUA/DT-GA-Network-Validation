import socket
import json
import time
import random
import os

HOST = "127.0.0.1"
PORT = 5000

# S6 experiment condition
LOSS_RATE = 0.50       # 50% packet loss
RUNS = 10
PACKETS_PER_RUN = 10

RESULT_FILE = "results/S6_loss50.json"


os.makedirs("results", exist_ok=True)

results = {
    "loss_rate": LOSS_RATE,
    "total_packets": RUNS * PACKETS_PER_RUN,
    "received_packets": 0,
    "lost_packets": 0,
    "PDR": 0,
    "RTT": []
}


for run in range(1, RUNS + 1):

    for packet in range(1, PACKETS_PER_RUN + 1):

        message = {
            "run": run,
            "packet": packet,
            "time": time.time()
        }

        try:

            # simulate packet loss
            if random.random() < LOSS_RATE:
                print(f"Run {run} Packet {packet}: LOST")
                results["lost_packets"] += 1
                continue


            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)

            start = time.time()

            client.connect((HOST, PORT))

            data = json.dumps(message).encode()

            client.send(data)

            response = client.recv(4096)

            end = time.time()

            rtt = end - start

            results["RTT"].append(rtt)
            results["received_packets"] += 1

            print(
                f"Run {run} Packet {packet}: "
                f"ACK received RTT={rtt:.6f}s"
            )

            client.close()


        except Exception:

            print(f"Run {run} Packet {packet}: LOST")
            results["lost_packets"] += 1


results["PDR"] = (
    results["received_packets"] /
    results["total_packets"]
) * 100


if results["RTT"]:
    results["mean_RTT"] = sum(results["RTT"]) / len(results["RTT"])
else:
    results["mean_RTT"] = None


with open(RESULT_FILE, "w") as f:
    json.dump(results, f, indent=4)


print("\n====================")
print("S6 TEST COMPLETE")
print("====================")

print(results)

print("\nSaved:")
print(RESULT_FILE)
