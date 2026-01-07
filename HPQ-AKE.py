"""
Simulation-Based Performance Evaluation of HPQ-AKE
"""

import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# ======================================================
# 1. Simulation Parameters
# ======================================================
np.random.seed(42)

NUM_RUNS = 500

# Reference cryptographic timings (ms)
T_KYBER = 1.8
T_DILITHIUM = 6.4
T_RSA = 1.2
T_SYM = 0.15   # HMAC + HKDF + AEAD

# Communication overhead (bytes)
SIZE_KYBER_CT = 1088
SIZE_KYBER_PK = 1184
SIZE_DILITHIUM_SIG = 2700
SIZE_RSA_CT = 256
SIZE_SYM_TAG = 64

# ======================================================
# 2. Protocol Cost Models
# ======================================================
def kyber_only():
    latency = 2 * T_KYBER
    overhead = SIZE_KYBER_CT + SIZE_KYBER_PK
    return latency, overhead

def kyber_dilithium():
    latency = 2 * T_KYBER + T_DILITHIUM
    overhead = SIZE_KYBER_CT + SIZE_KYBER_PK + SIZE_DILITHIUM_SIG
    return latency, overhead

def hybrid_rsa_kyber():
    latency = 2 * T_KYBER + T_RSA
    overhead = SIZE_KYBER_CT + SIZE_KYBER_PK + SIZE_RSA_CT
    return latency, overhead

def hpq_ake():
    latency = 2 * T_KYBER + T_RSA + T_SYM
    overhead = (
        SIZE_KYBER_CT +
        SIZE_KYBER_PK +
        SIZE_RSA_CT +
        SIZE_SYM_TAG
    )
    return latency, overhead

# ======================================================
# 3. Monte Carlo Simulation
# ======================================================
schemes = {
    "Kyber-only": kyber_only,
    "Kyber + Dilithium": kyber_dilithium,
    "Hybrid RSA–Kyber": hybrid_rsa_kyber,
    "HPQ-AKE": hpq_ake
}

latency_results = {}
overhead_results = {}

for name, func in schemes.items():
    latencies = []
    overheads = []
    for _ in range(NUM_RUNS):
        l, o = func()
        latencies.append(l + np.random.normal(0, 0.05))
        overheads.append(o)
    latency_results[name] = np.mean(latencies)
    overhead_results[name] = np.mean(overheads)

# ======================================================
# 4. Figure 1: Handshake Latency Comparison
# ======================================================
plt.figure(figsize=(6,4))
plt.bar(latency_results.keys(), latency_results.values())
plt.ylabel("Handshake Latency (ms)")
plt.title("Handshake Latency Comparison")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("Fig6_latency_comparison.pdf")
plt.show()
plt.close()

# ======================================================
# 5. Figure 2: Communication Overhead Comparison
# ======================================================
plt.figure(figsize=(6,4))

protocols = list(overhead_results.keys())
overheads = list(overhead_results.values())

plt.barh(protocols, overheads)
plt.xlabel("Communication Overhead (bytes)")
plt.title("Communication Overhead per Handshake")
plt.grid(axis="x")

plt.tight_layout()
plt.savefig("Fig7_overhead_comparison.pdf")
plt.show()
plt.close()

# ======================================================
# 6. Print Summary
# ======================================================
print("=== Simulation Results Summary ===")
for name in schemes:
    print(f"{name:20s} | Latency = {latency_results[name]:.2f} ms | "
          f"Overhead = {overhead_results[name]:.0f} bytes")

# ======================================================
# 7. Download Figures (Optional but convenient)
# ======================================================
files.download("Fig6_latency_comparison.pdf")
files.download("Fig7_overhead_comparison.pdf")
