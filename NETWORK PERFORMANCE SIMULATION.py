import numpy as np
import matplotlib.pyplot as plt

# Dữ liệu lấy CHÍNH XÁC từ kết quả bạn vừa chạy ra
protocols = ["Kyber-only", "Hybrid TLS 1.3", "KEMTLS", "Kyber+Dilithium", "HPQ-AKE (Ours)"]
t_comp = np.array([1.31, 9.62, 2.46, 6.55, 3.33]) # ms (Lấy từ bảng của bạn)
msg_sizes = np.array([2272, 8500, 6544, 7517, 2784]) # Bytes

# Các kịch bản mạng
scenarios = {
    "LAN/5G (100Mbps, 10ms RTT)": {"bw": 100, "rtt": 10},
    "4G/Wi-Fi (10Mbps, 50ms RTT)": {"bw": 10, "rtt": 50},
    "IoT/Satellite (1Mbps, 200ms RTT)": {"bw": 1, "rtt": 200}
}

results = {}
for name, par in scenarios.items():
    bw_bytes_ms = (par["bw"] * 10**6 / 8) / 1000
    # Tổng thời gian = Tính toán + Truyền tải (Message/BW) + Độ trễ vòng (2*RTT)
    results[name] = t_comp + (msg_sizes / bw_bytes_ms) + (par["rtt"] * 2)

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(12, 7))
x = np.arange(len(protocols))
width = 0.25
colors = ['#cbd5e1', '#94a3b8', '#64748b', '#f87171', '#3b82f6']

for i, (name, total_latencies) in enumerate(results.items()):
    ax.bar(x + i*width, total_latencies, width, label=name)

ax.set_title("Total Handshake Latency across Network Scenarios", fontsize=14)
ax.set_ylabel("Total Latency (ms)")
ax.set_xticks(x + width)
ax.set_xticklabels(protocols)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("final_network_sim.png", dpi=300)
plt.show()