import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path

from cryptography import __version__ as cryptography_version
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ============================================================
# Configuration
# ============================================================

KEY_SIZE = 32
NONCE_SIZE = 12
TAG_SIZE = 16

PLAINTEXT = b"123456789012"   # Exactly 12 bytes

WARMUP_RECORDS = 1_000
BENCHMARK_RECORDS = 10_000
REPEAT_RUNS = 5


# ============================================================
# Results
# ============================================================

def save_results(results):
    output_path = Path("results/aes_gcm_benchmark.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")


# ============================================================
# AES-GCM helpers
# ============================================================

def encrypt_record(aesgcm: AESGCM, plaintext: bytes, nonce: bytes) -> bytes:
    return aesgcm.encrypt(nonce, plaintext, None)


def decrypt_record(aesgcm: AESGCM, encrypted: bytes, nonce: bytes) -> bytes:
    return aesgcm.decrypt(nonce, encrypted, None)


# ============================================================
# Encryption benchmark
# ============================================================

def benchmark_encryption(aesgcm: AESGCM, nonces):
    """
    Measures AES-GCM encryption only.

    Nonces are generated before timing starts, so nonce generation
    is excluded from encryption latency.
    """
    latencies = []

    for _ in range(REPEAT_RUNS):
        start = time.perf_counter_ns()

        for nonce in nonces:
            encrypt_record(aesgcm, PLAINTEXT, nonce)

        elapsed_ns = time.perf_counter_ns() - start

        latency_ms = elapsed_ns / BENCHMARK_RECORDS / 1_000_000
        latencies.append(latency_ms)

    return latencies


# ============================================================
# Decryption benchmark
# ============================================================

def benchmark_decryption(aesgcm: AESGCM, encrypted_records):
    """
    Measures AES-GCM decryption only.
    """
    latencies = []

    for _ in range(REPEAT_RUNS):
        start = time.perf_counter_ns()

        for nonce, encrypted in encrypted_records:
            decrypt_record(aesgcm, encrypted, nonce)

        elapsed_ns = time.perf_counter_ns() - start

        latency_ms = elapsed_ns / BENCHMARK_RECORDS / 1_000_000
        latencies.append(latency_ms)

    return latencies


# ============================================================
# End-to-end throughput benchmark
# ============================================================

def benchmark_throughput(aesgcm: AESGCM):
    """
    Measures end-to-end encryption throughput including nonce
    generation and AES-GCM encryption.
    """
    start = time.perf_counter_ns()

    for _ in range(BENCHMARK_RECORDS):
        nonce = os.urandom(NONCE_SIZE)
        encrypt_record(aesgcm, PLAINTEXT, nonce)

    elapsed_ns = time.perf_counter_ns() - start
    elapsed_sec = elapsed_ns / 1_000_000_000

    return BENCHMARK_RECORDS / elapsed_sec


# ============================================================
# Integrity / Tamper Detection
# ============================================================

def test_integrity(aesgcm: AESGCM, encrypted: bytes, nonce: bytes):
    """
    Flip one bit in ciphertext and verify that AES-GCM
    rejects the modified packet.
    """
    tampered = bytearray(encrypted)
    tampered[0] ^= 0x01

    try:
        decrypt_record(aesgcm, bytes(tampered), nonce)
        return False
    except Exception:
        return True


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 60)
    print("AES-GCM IoMT Security Benchmark")
    print("=" * 60)

    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)

    print("Algorithm          : AES-256-GCM")
    print(f"Plaintext size     : {len(PLAINTEXT)} bytes")
    print(f"Nonce size         : {NONCE_SIZE} bytes")
    print(f"Auth tag size      : {TAG_SIZE} bytes")
    print(f"Warm-up records    : {WARMUP_RECORDS:,}")
    print(f"Benchmark records  : {BENCHMARK_RECORDS:,}")
    print(f"Benchmark runs     : {REPEAT_RUNS}")

    # --------------------------------------------------------
    # Warm-up
    # --------------------------------------------------------

    for _ in range(WARMUP_RECORDS):
        nonce = os.urandom(NONCE_SIZE)
        encrypted = encrypt_record(aesgcm, PLAINTEXT, nonce)
        decrypt_record(aesgcm, encrypted, nonce)

    # --------------------------------------------------------
    # Pre-generate nonces BEFORE encryption benchmark
    # --------------------------------------------------------

    benchmark_nonces = [
        os.urandom(NONCE_SIZE)
        for _ in range(BENCHMARK_RECORDS)
    ]

    # --------------------------------------------------------
    # Generate encrypted records for decryption benchmark
    # --------------------------------------------------------

    encrypted_records = [
        (
            nonce,
            encrypt_record(aesgcm, PLAINTEXT, nonce)
        )
        for nonce in benchmark_nonces
    ]

    # --------------------------------------------------------
    # Encryption benchmark
    # --------------------------------------------------------

    encryption_latencies = benchmark_encryption(
        aesgcm,
        benchmark_nonces,
    )

    # --------------------------------------------------------
    # Decryption benchmark
    # --------------------------------------------------------

    decryption_latencies = benchmark_decryption(
        aesgcm,
        encrypted_records,
    )

    # --------------------------------------------------------
    # End-to-end throughput
    # --------------------------------------------------------

    throughput_values = [
        benchmark_throughput(aesgcm)
        for _ in range(REPEAT_RUNS)
    ]

    # --------------------------------------------------------
    # Packet size
    # --------------------------------------------------------

    nonce, encrypted = encrypted_records[0]

    ciphertext_size = len(encrypted) - TAG_SIZE
    encrypted_packet_size = NONCE_SIZE + len(encrypted)

    cryptographic_overhead = (
        encrypted_packet_size - len(PLAINTEXT)
    )

    # --------------------------------------------------------
    # Integrity test
    # --------------------------------------------------------

    integrity_passed = test_integrity(
        aesgcm,
        encrypted,
        nonce,
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    enc_mean = statistics.mean(encryption_latencies)
    enc_median = statistics.median(encryption_latencies)

    dec_mean = statistics.mean(decryption_latencies)
    dec_median = statistics.median(decryption_latencies)

    throughput_mean = statistics.mean(throughput_values)
    throughput_median = statistics.median(throughput_values)

    # --------------------------------------------------------
    # Terminal output
    # --------------------------------------------------------

    print()
    print("-" * 60)
    print("Performance")
    print("-" * 60)

    print(
        f"Encryption latency : {enc_mean:.6f} ms/record "
        f"(median {enc_median:.6f} ms)"
    )

    print(
        f"Decryption latency : {dec_mean:.6f} ms/record "
        f"(median {dec_median:.6f} ms)"
    )

    print(
        f"Throughput         : {throughput_mean:,.2f} records/s "
        f"(median {throughput_median:,.2f})"
    )

    print()
    print("-" * 60)
    print("Packet Size")
    print("-" * 60)

    print(f"Plaintext          : {len(PLAINTEXT)} bytes")
    print(f"Ciphertext         : {ciphertext_size} bytes")
    print(f"Nonce              : {NONCE_SIZE} bytes")
    print(f"Authentication tag  : {TAG_SIZE} bytes")
    print(f"Encrypted packet   : {encrypted_packet_size} bytes")
    print(f"Crypto overhead    : {cryptographic_overhead} bytes")

    print()
    print("-" * 60)
    print("Integrity")
    print("-" * 60)

    print(
        f"Tamper detection   : "
        f"{'PASS' if integrity_passed else 'FAIL'}"
    )

    print()
    print("=" * 60)

    # --------------------------------------------------------
    # JSON result
    # --------------------------------------------------------

    results = {
        "experiment": {
            "name": "AES-GCM IoMT Security Benchmark",
            "algorithm": "AES-256-GCM",
            "key_size_bits": KEY_SIZE * 8,
            "plaintext_size_bytes": len(PLAINTEXT),
            "nonce_size_bytes": NONCE_SIZE,
            "authentication_tag_size_bytes": TAG_SIZE,
            "warmup_records": WARMUP_RECORDS,
            "benchmark_records": BENCHMARK_RECORDS,
            "benchmark_runs": REPEAT_RUNS,
        },

        "performance": {
            "encryption_latency_mean_ms_per_record": enc_mean,
            "encryption_latency_median_ms_per_record": enc_median,
            "decryption_latency_mean_ms_per_record": dec_mean,
            "decryption_latency_median_ms_per_record": dec_median,
            "throughput_mean_records_per_second": throughput_mean,
            "throughput_median_records_per_second": throughput_median,
        },

        "packet_size": {
            "plaintext_bytes": len(PLAINTEXT),
            "ciphertext_bytes": ciphertext_size,
            "nonce_bytes": NONCE_SIZE,
            "authentication_tag_bytes": TAG_SIZE,
            "encrypted_packet_bytes": encrypted_packet_size,
            "cryptographic_overhead_bytes": cryptographic_overhead,
        },

        "integrity": {
            "tamper_detection": integrity_passed,
            "test": "single_bit_flip_in_ciphertext",
        },

        "environment": {
            "python_version": sys.version.split()[0],
            "cryptography_version": cryptography_version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
    }

    save_results(results)


if __name__ == "__main__":
    main()
