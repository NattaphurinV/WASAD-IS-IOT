import csv
import json
import statistics
import time
from pathlib import Path

import cbor2

from src.iot_payload import decode_payload, encode_payload


CSV_PATH = Path("data/processed/iot/s2_dummy_1000.csv")
RESULT_PATH = Path("results/payload_format_benchmark.json")

WARMUP_RECORDS = 100
BENCHMARK_RECORDS = 1000
BENCHMARK_RUNS = 5


def load_records():
    with CSV_PATH.open(newline="") as f:
        rows = list(csv.DictReader(f))

    if len(rows) < BENCHMARK_RECORDS:
        raise ValueError(
            f"Expected at least {BENCHMARK_RECORDS} records, got {len(rows)}"
        )

    records = []

    for row in rows[:BENCHMARK_RECORDS]:
        records.append(
            {
                "timestamp": int(row["timestamp"]),
                "heart_rate": int(row["heart_rate"]),
                "skin_temp": float(row["skin_temp"]),
                "eda_value": float(row["eda_value"]),
                "status_flag": int(row["status_flag"]),
            }
        )

    return records


def encode_json(record):
    return json.dumps(
        record,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def decode_json(payload):
    return json.loads(payload.decode("utf-8"))


def encode_cbor(record):
    return cbor2.dumps(record)


def decode_cbor(payload):
    return cbor2.loads(payload)


def encode_binary(record):
    return encode_payload(
        timestamp=record["timestamp"],
        heart_rate=record["heart_rate"],
        skin_temp=record["skin_temp"],
        eda_value=record["eda_value"],
        status_flag=record["status_flag"],
    )


def decode_binary(payload):
    return decode_payload(payload)


FORMATS = {
    "json": (encode_json, decode_json),
    "cbor": (encode_cbor, decode_cbor),
    "binary": (encode_binary, decode_binary),
}


def measure_encode(records, encode_fn):
    start = time.perf_counter_ns()

    payloads = [encode_fn(record) for record in records]

    elapsed_ns = time.perf_counter_ns() - start

    return payloads, elapsed_ns / len(records) / 1_000_000


def measure_decode(payloads, decode_fn):
    start = time.perf_counter_ns()

    records = [decode_fn(payload) for payload in payloads]

    elapsed_ns = time.perf_counter_ns() - start

    return records, elapsed_ns / len(payloads) / 1_000_000


def normalize_for_comparison(record):
    return {
        "timestamp": int(record["timestamp"]),
        "heart_rate": int(record["heart_rate"]),
        "skin_temp": round(float(record["skin_temp"]), 2),
        "eda_value": float(record["eda_value"]),
        "status_flag": int(record["status_flag"]),
    }


def validate_round_trip(records, decoded_records):
    for original, decoded in zip(records, decoded_records):
        original = normalize_for_comparison(original)
        decoded = normalize_for_comparison(decoded)

        assert original["timestamp"] == decoded["timestamp"]
        assert original["heart_rate"] == decoded["heart_rate"]
        assert abs(original["skin_temp"] - decoded["skin_temp"]) < 0.01
        assert abs(original["eda_value"] - decoded["eda_value"]) < 1e-6
        assert original["status_flag"] == decoded["status_flag"]


def benchmark_format(name, records):
    encode_fn, decode_fn = FORMATS[name]

    # Warm-up
    warmup = records[:WARMUP_RECORDS]
    for record in warmup:
        payload = encode_fn(record)
        decode_fn(payload)

    encode_times = []
    decode_times = []
    payloads = None

    for _ in range(BENCHMARK_RUNS):
        payloads, encode_ms = measure_encode(records, encode_fn)
        _, decode_ms = measure_decode(payloads, decode_fn)

        encode_times.append(encode_ms)
        decode_times.append(decode_ms)

    decoded_records, _ = measure_decode(payloads, decode_fn)
    validate_round_trip(records, decoded_records)

    sizes = [len(payload) for payload in payloads]

    return {
        "record_count": len(records),
        "payload_size_bytes": {
            "first_record": sizes[0],
            "mean": statistics.mean(sizes),
            "min": min(sizes),
            "max": max(sizes),
            "total": sum(sizes),
        },
        "latency_ms_per_record": {
            "encode_mean": statistics.mean(encode_times),
            "encode_median": statistics.median(encode_times),
            "decode_mean": statistics.mean(decode_times),
            "decode_median": statistics.median(decode_times),
        },
        "round_trip": True,
    }


def main():
    records = load_records()

    print("=" * 64)
    print("IoMT Payload Format Benchmark")
    print("=" * 64)
    print(f"Records          : {len(records):,}")
    print(f"Benchmark runs   : {BENCHMARK_RUNS}")
    print(f"Warm-up records  : {WARMUP_RECORDS}")
    print()

    results = {}

    for name in FORMATS:
        result = benchmark_format(name, records)
        results[name] = result

        print(f"{name.upper()}")
        print("-" * 64)
        print(
            f"Payload size     : "
            f"{result['payload_size_bytes']['first_record']} bytes/record"
        )
        print(
            f"Total size       : "
            f"{result['payload_size_bytes']['total']:,} bytes"
        )
        print(
            f"Encode latency   : "
            f"{result['latency_ms_per_record']['encode_mean']:.6f} ms/record"
        )
        print(
            f"Decode latency   : "
            f"{result['latency_ms_per_record']['decode_mean']:.6f} ms/record"
        )
        print(f"Round-trip       : PASS")
        print()

    binary_size = results["binary"]["payload_size_bytes"]["mean"]

    for name, result in results.items():
        size = result["payload_size_bytes"]["mean"]
        result["vs_binary"] = {
            "size_ratio": size / binary_size,
            "size_overhead_bytes": size - binary_size,
            "size_reduction_vs_format_percent": (
                (1 - binary_size / size) * 100 if size else 0
            ),
        }

    output = {
        "experiment": {
            "name": "IoMT Payload Format Benchmark",
            "formats": ["json", "cbor", "binary"],
            "dataset": "WESAD S2",
            "records": len(records),
            "benchmark_runs": BENCHMARK_RUNS,
            "warmup_records": WARMUP_RECORDS,
        },
        "results": results,
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    print("=" * 64)
    print(f"Results saved to: {RESULT_PATH}")


if __name__ == "__main__":
    main()
