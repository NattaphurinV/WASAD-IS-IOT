# AES-GCM Security Benchmark

## Objective

The benchmark evaluates the performance and communication overhead of
AES-GCM protection for a small IoMT telemetry payload.

The benchmark measures:

1. Encryption latency
2. Decryption latency
3. End-to-end throughput
4. Encrypted packet size
5. Cryptographic overhead
6. Authentication/integrity detection

## Cryptographic Configuration

| Parameter | Value |
|---|---:|
| Algorithm | AES-256-GCM |
| Key size | 256 bits |
| Plaintext size | 12 bytes |
| Nonce size | 12 bytes |
| Authentication tag | 16 bytes |

AES-GCM produces ciphertext with the same length as the plaintext. The
authentication tag is appended by the AES-GCM implementation.

## Benchmark Configuration

| Parameter | Value |
|---|---:|
| Warm-up records | 1,000 |
| Records per run | 10,000 |
| Benchmark runs | 5 |

## Encryption Latency

Encryption latency measures the AES-GCM encryption operation only.

The 12-byte nonces are generated before the timed section. Therefore,
nonce-generation time is excluded from the encryption-latency measurement.

This distinction is important because nonce generation and cryptographic
encryption are separate operations.

## Decryption Latency

Decryption latency measures the AES-GCM decryption and authentication
operation using pre-generated encrypted records.

## Throughput

Throughput represents end-to-end encryption processing and includes:

    nonce generation
    +
    AES-GCM encryption

It is reported in records per second.

Therefore, throughput should not be interpreted as the inverse of the
AES-GCM-only encryption latency.

## Packet Size

For a 12-byte plaintext:

    Plaintext       = 12 bytes
    Nonce           = 12 bytes
    Ciphertext      = 12 bytes
    Authentication  = 16 bytes
    ---------------------------
    Total           = 40 bytes

Cryptographic overhead is:

    40 - 12 = 28 bytes

## Integrity Test

The benchmark modifies one bit of the encrypted ciphertext and attempts
decryption.

A successful integrity check requires AES-GCM to reject the modified packet.

Expected result:

    Tamper detection = PASS

This demonstrates authentication/integrity detection for the tested packet.

## Interpretation

The benchmark results are specific to the hardware, operating system,
Python runtime, cryptography library version, and benchmark configuration
used during the experiment.

They should therefore be reported together with the experimental
environment rather than treated as universal AES-GCM performance values.
