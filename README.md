# WASAD-IS-IOT

IoMT telemetry and secure transmission proof-of-concept based on the WESAD dataset.

The project focuses on:

- WESAD signal loading and preprocessing
- IoMT telemetry generation
- Compact binary payload encoding
- Payload-size optimization
- AES-256-GCM encryption
- Telemetry integrity and security testing
- Zero Trust access-control prototype
- Performance evaluation

The current implementation is a research prototype. It does not yet represent a complete production IoMT or Zero Trust system.

## 1. Requirements

- Python 3.10+
- Git
- WESAD dataset

## 2. Setup

Clone the repository:

```bash
git clone https://github.com/NattaphurinV/WASAD-IS-IOT.git
cd WASAD-IS-IOT

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

python -m pip install -r requirements.txt

Verify dependencies:

python -m pip check
3. Dataset

This project uses the WESAD dataset.

The raw WESAD dataset is not included in this repository because of its large size and dataset distribution restrictions.

Place the dataset locally under:

data/raw/WESAD/

For example:

data/raw/WESAD/S2/S2.pkl

The data/raw/ directory is excluded from Git.

4. Current IoMT Pipeline

The current prototype uses WESAD S2 to validate the telemetry pipeline.

Current flow:

WESAD S2
   |
   v
Wrist EDA + Skin Temperature
   |
   v
1 Hz telemetry records
   |
   v
12-byte binary payload
   |
   v
AES-256-GCM
   |
   v
Encrypted packet

Current telemetry generation:

python -m scripts.generate_iot_telemetry

Validate the binary payload:

python -m scripts.test_iot_payload
5. Binary Payload

The current prototype uses a fixed 12-byte binary payload.

Format:

>IBhfB

Fields:

Field	Size
Timestamp	4 bytes
Heart rate	1 byte
Skin temperature	2 bytes
EDA	4 bytes
Status flag	1 byte
Total	12 bytes

The current heart-rate value is deterministic mock telemetry used for pipeline testing. It is not calculated as medical-grade heart rate from WESAD BVP.

6. AES-256-GCM

The current cryptographic prototype uses:

AES-256
GCM authenticated encryption
256-bit key
12-byte nonce
16-byte authentication tag

Run the benchmark:

python -m scripts.benchmark_aes_gcm

The benchmark evaluates encryption/decryption latency, throughput, packet overhead, and ciphertext tamper detection.

7. Security Architecture

The intended architecture is:

IoMT Device
    |
    | Device ID + Nonce + Ciphertext + Tag
    v
Gateway
    |
    v
Policy Decision Point (PDP)
    |
    v
Policy Enforcement Point (PEP)
    |
    +---- Authorized ----> Decrypt + Decode
    |
    +---- Unauthorized --> Reject

The Zero Trust components are under active development.

8. Security Tests

Planned security tests include:

Packet tampering
Unauthorized device
Replay attack
Invalid authentication tag
Valid packet acceptance
Invalid packet rejection

The current implementation includes AES-GCM ciphertext tamper detection. Replay protection and device authorization are not yet implemented.

9. Experimental Scope

The project evaluates:

Payload
Payload size
Serialization/deserialization latency
Encoding overhead
Cryptography
AES-256-GCM encryption latency
AES-256-GCM decryption latency
Cryptographic packet overhead
Integrity protection
IoMT Security
Device authentication/authorization
Tamper detection
Replay protection
Zero Trust policy enforcement
End-to-End Performance

The final experiment will measure:

Telemetry generation
        |
        v
Serialization
        |
        v
Encryption
        |
        v
Packet transmission representation
        |
        v
Authorization
        |
        v
Decryption
        |
        v
Deserialization
10. Repository Structure
wesad-is/
├── data/
│   ├── raw/                 # Local WESAD dataset, not tracked
│   ├── processed/           # Generated data, not tracked
│   └── features/            # Generated features, not tracked
├── docs/
│   ├── experiment_notes.md
│   ├── IOT_PAYLOAD.md
│   └── ...
├── scripts/
│   ├── generate_iot_telemetry.py
│   ├── test_iot_payload.py
│   ├── test_signals.py
│   └── benchmark_aes_gcm.py
├── src/
│   ├── preprocessing/
│   └── iot_payload.py
├── archive/
│   └── ml_pipeline/
├── requirements.txt
└── README.md
11. Current Status
Component	Status
WESAD loader	Implemented
EDA/TEMP preprocessing	Implemented
IoMT telemetry generation	Implemented
12-byte binary payload	Implemented
AES-256-GCM	Implemented
AES benchmark	Implemented
Payload optimization comparison	In progress
Device identity	Planned
Gateway	Planned
PDP/PEP	Planned
Zero Trust enforcement	Planned
Replay protection	Planned
Unauthorized-device test	Planned
End-to-end benchmark	Planned
12. Important Data Policy

Do not commit the WESAD dataset or generated large data files.

Before committing:

git status

Verify that raw and generated data are not staged:

git status --short

The repository .gitignore excludes:

data/raw/
data/processed/
data/features/
results/
outputs/

Small reproducible documentation and source-code artifacts may be committed normally.
