import csv

from src.iot_payload import (
    PAYLOAD_SIZE,
    decode_payload,
    encode_payload,
)


CSV_PATH = "data/processed/iot/s2_dummy_1000.csv"


def main():
    with open(CSV_PATH, newline="") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 1000

    payloads = []

    for row in rows:
        payload = encode_payload(
            timestamp=int(row["timestamp"]),
            heart_rate=int(row["heart_rate"]),
            skin_temp=float(row["skin_temp"]),
            eda_value=float(row["eda_value"]),
            status_flag=int(row["status_flag"]),
        )

        assert len(payload) == PAYLOAD_SIZE
        payloads.append(payload)

    assert all(len(p) == 12 for p in payloads)

    decoded = decode_payload(payloads[0])

    print("Payload format: >IBhfB")
    print("Payload size:", PAYLOAD_SIZE, "bytes")
    print("Records:", len(payloads))
    print("Total plaintext size:", sum(len(p) for p in payloads), "bytes")

    print("\nFirst payload:")
    print(payloads[0].hex())

    print("\nDecoded first payload:")
    print(decoded)

    print("\n12-byte payload validation passed.")


if __name__ == "__main__":
    main()
