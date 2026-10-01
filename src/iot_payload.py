import struct


PAYLOAD_FORMAT = ">IBhfB"
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_FORMAT)

assert PAYLOAD_SIZE == 12


def encode_payload(
    timestamp: int,
    heart_rate: int,
    skin_temp: float,
    eda_value: float,
    status_flag: int,
) -> bytes:
    """
    Encode one IoMT telemetry record into exactly 12 bytes.

    Format:
        >IBhfB

        timestamp   : uint32
        heart_rate  : uint8
        skin_temp   : int16, Celsius * 100
        eda_value   : float32
        status_flag : uint8
    """

    skin_temp_scaled = round(skin_temp * 100)

    return struct.pack(
        PAYLOAD_FORMAT,
        timestamp,
        heart_rate,
        skin_temp_scaled,
        eda_value,
        status_flag,
    )


def decode_payload(payload: bytes):
    """Decode a 12-byte IoMT payload."""

    if len(payload) != PAYLOAD_SIZE:
        raise ValueError(
            f"Invalid payload size: {len(payload)} bytes. "
            f"Expected {PAYLOAD_SIZE} bytes."
        )

    timestamp, heart_rate, skin_temp_scaled, eda_value, status_flag = (
        struct.unpack(PAYLOAD_FORMAT, payload)
    )

    return {
        "timestamp": timestamp,
        "heart_rate": heart_rate,
        "skin_temp": skin_temp_scaled / 100.0,
        "eda_value": eda_value,
        "status_flag": status_flag,
    }
