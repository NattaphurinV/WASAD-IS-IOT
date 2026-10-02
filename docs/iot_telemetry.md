# IoMT Telemetry

## Purpose

The IoMT telemetry layer converts processed physiological signals into
records that represent measurements transmitted by an IoMT device.

## Processing Flow

WESAD signal
    ↓
Preprocessing
    ↓
1 Hz physiological measurement
    ↓
IoMT telemetry record
    ↓
Fixed-size plaintext payload
    ↓
AES-GCM encryption

## Telemetry

The telemetry representation contains measurement information required by
the experiment, including timestamp, sensor/value information, units, and
the associated label where applicable.

The exact serialized payload used for cryptographic benchmarking is fixed at
12 bytes.

## Payload Size

The security benchmark uses:

    Plaintext = 12 bytes

The fixed payload size allows encryption performance and communication
overhead to be measured consistently.

## Scope

Telemetry generation and cryptographic benchmarking are separate stages.
The telemetry pipeline provides the input data, while the security benchmark
evaluates the protection applied to the resulting payload.
