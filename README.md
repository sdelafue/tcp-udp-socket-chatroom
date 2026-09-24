# tcp-udp-socket-chatroom
## TCP and UDP Applications plus Comparison Report

This project implements two network applications using both TCP and UDP:

1. Chat and Messaging System
2. File Transfer System

The project compares TCP and UDP in terms of reliability, ordering, throughput, latency, retransmissions, and implementation complexity.

---

## Requirements

- Python 3.13.3
- Install matplotlib for graph generation:

```bash
py -m pip install matplotlib
```

---

## Step-by-Step Guide

### Step 1 — Install the dependency

```bash
py -m pip install matplotlib
```

Expected output:

```
Successfully installed matplotlib-3.x.x
```

---

### Step 2 — Generate test files

Run this once before running any file transfer scripts. It creates the binary test files the server will send.

```bash
py experiment_runner.py
```

Expected output:

```
Created files/test_100KB.bin with size 102400 bytes
Created files/test_1MB.bin with size 1048576 bytes
Created files/test_5MB.bin with size 5242880 bytes
```

A `files/` directory will be created containing the three test files.

---

### Step 3 — Run TCP Chat (Application 1, TCP)

Open **3 separate terminals** in the project folder.

**Terminal 1 — Start the server:**

```bash
py tcp_chat_server.py
```

Expected output:

```
[SERVER] Listening on 127.0.0.1:5000
[SERVER] Alice joined
[SERVER] Bob joined
[SERVER] Alice -> Bob: Hello!
```

**Terminal 2 — Start client 1:**

```bash
py tcp_chat_client.py
```

Expected prompts and interaction:

```
Enter your username: Alice
[Alice] >> Hello!
[Bob]: Hi Alice!
```

**Terminal 3 — Start client 2:**

```bash
py tcp_chat_client.py
```

Expected prompts and interaction:

```
Enter your username: Bob
[Alice]: Hello!
[Bob] >> Hi Alice!
```

Each client can send messages that are broadcast to all other connected clients. Type `quit` to disconnect.

---

### Step 4 — Run UDP Chat (Application 1, UDP)

Open **3 separate terminals** in the project folder.

**Terminal 1 — Start the UDP server:**

```bash
py udp_chat_server.py
```

Expected output:

```
[UDP SERVER] Listening on 127.0.0.1:5001
[UDP SERVER] Registered: Alice
[UDP SERVER] Registered: Bob
[UDP SERVER] Alice -> Bob: Hey!
```

**Terminal 2 — Start UDP client 1:**

```bash
py udp_chat_client.py
```

Expected interaction:

```
Enter your username: Alice
[REGISTERED] Alice
[Alice] >> Hey!
[ACK] seq=1
[Bob]: Hey back!
```

**Terminal 3 — Start UDP client 2:**

```bash
py udp_chat_client.py
```

Expected interaction:

```
Enter your username: Bob
[REGISTERED] Bob
[Alice]: Hey!
[Bob] >> Hey back!
[ACK] seq=1
```

UDP chat uses sequence numbers, ACK messages, and automatic retransmission if an ACK is not received within the timeout.

---

### Step 5 — Run TCP File Transfer (Application 2, TCP)

Open **2 separate terminals** in the project folder.

**Terminal 1 — Start the TCP file server:**

```bash
py tcp_file_server.py
```

Expected output:

```
[TCP FILE SERVER] Listening on 127.0.0.1:6000
[TCP FILE SERVER] Sending test_100KB.bin in chunks of 4096 bytes
[TCP FILE SERVER] Transfer complete
```

**Terminal 2 — Start the TCP file client:**

```bash
py tcp_file_client.py
```

When prompted:

```
Enter filename: test_100KB.bin
Enter chunk size (bytes): 4096
```

Expected output:

```
Receiving test_100KB.bin...
Progress: 100%
Transfer time: 0.13 seconds
Throughput: 77614.80 KB/s
SHA-256 checksum match: YES
File saved to received_files/tcp_test_100KB.bin
```

Repeat for other file and chunk size combinations:

| Filename | Chunk size |
|---|---|
| test_100KB.bin | 1024 |
| test_100KB.bin | 4096 |
| test_100KB.bin | 16384 |
| test_1MB.bin | 4096 |
| test_5MB.bin | 4096 |

---

### Step 6 — Run UDP File Transfer (Application 2, UDP)

Open **2 separate terminals** in the project folder.

**Terminal 1 — Start the UDP file server:**

```bash
py udp_file_server.py
```

Expected output:

```
[UDP FILE SERVER] Listening on 127.0.0.1:6001
[UDP FILE SERVER] Sending test_100KB.bin, 25 packets of 4096 bytes
[UDP FILE SERVER] All packets ACKed. Transfer complete.
```

**Terminal 2 — Start the UDP file client:**

```bash
py udp_file_client.py
```

When prompted:

```
Enter filename: test_100KB.bin
Enter chunk size (bytes): 4096
```

Expected output:

```
Receiving test_100KB.bin via UDP...
Packets received: 25/25
Retransmissions: 0
Transfer time: 0.15 seconds
Throughput: 66470.74 KB/s
SHA-256 checksum match: YES
File saved to received_files/udp_test_100KB.bin
```

Repeat for `test_1MB.bin` and `test_5MB.bin` as with TCP.

---

### Step 7 — Generate graphs

Run the graph generator from the project root:

```bash
py results/experiment_runner3.py
```

Expected output:

```
Saved results/file_throughput.png
Saved results/chat_latency.png
```

This produces the two required graphs using the pre-collected data in `results/metrics.csv`.

---

## Results

All experimental data is stored in:

```
results/metrics.csv
```

Generated graphs:

```
results/chat_latency.png       — Message size vs average latency (TCP and UDP)
results/file_throughput.png    — File size vs throughput (TCP and UDP)
```

---

## Submission Checklist

| Item | File |
|---|---|
| TCP Chat | tcp_chat_server.py, tcp_chat_client.py |
| UDP Chat | udp_chat_server.py, udp_chat_client.py |
| TCP File Transfer | tcp_file_server.py, tcp_file_client.py |
| UDP File Transfer | udp_file_server.py, udp_file_client.py |
| Experiment runner | experiment_runner.py |
| Metrics data | results/metrics.csv |
| Chat latency graph | results/chat_latency.png |
| File throughput graph | results/file_throughput.png |
| Documentation | README.md |
| Report | report.docx |

---

## Files Included

```
tcp_chat_server.py
tcp_chat_client.py
udp_chat_server.py
udp_chat_client.py
tcp_file_server.py
tcp_file_client.py
udp_file_server.py
udp_file_client.py
experiment_runner.py
results/experiment_runner3.py
results/metrics.csv
results/file_throughput.png
results/chat_latency.png
README.md
report.docx
```

---

## Project Summary

### TCP Advantages

- Reliable delivery
- Ordered packets
- Built-in flow control
- Built-in congestion control
- Easier to implement

### UDP Advantages

- Lower overhead
- Faster in some real-time cases
- Full protocol control by developer
- Useful for gaming, streaming, VoIP

### UDP Additional Work Required

To make UDP reliable, this project implemented:

- Sequence numbers
- ACK packets
- Timeout detection
- Retransmission logic
- Packet reordering
- Checksum verification

### Final Conclusion

TCP is easier and more reliable for general communication and file transfer.
UDP requires more programming effort but gives greater flexibility and lower protocol overhead.
