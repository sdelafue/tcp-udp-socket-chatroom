import matplotlib.pyplot as plt

# File throughput graph
sizes = ["100KB", "1MB", "5MB"]
tcp_file = [77614.80, 138547.33, 138817.80]
udp_file = [66470.74, 85097.73, 72956.56]




plt.figure(figsize=(10, 6))
plt.plot(sizes, tcp_file, marker="o", label="TCP")
plt.plot(sizes, udp_file, marker="o", label="UDP")
plt.title("File Size vs Throughput")
plt.xlabel("File Size")
plt.ylabel("Throughput (KB/s)")
plt.legend()
plt.grid(True)
plt.savefig("results/file_throughput.png")
print("Saved results/file_throughput.png")




message_sizes = ["32B", "256B", "1024B"]

tcp_latency = [1.2, 1.6, 2.4]
udp_latency = [1.5, 2.0, 3.1]

plt.figure(figsize=(10, 6))
plt.plot(message_sizes, tcp_latency, marker="o", label="TCP")
plt.plot(message_sizes, udp_latency, marker="o", label="UDP")
plt.title("Message Size vs Average Latency")
plt.xlabel("Message Size")
plt.ylabel("Average Latency (ms)")
plt.legend()
plt.grid(True)
plt.savefig("results/chat_latency.png")
print("Saved results/chat_latency.png")