import binascii


class UUencodeError(ValueError):
    """Raised for structural problems in uuencoded text."""


def encode(data: bytes) -> bytes:
    """Encode arbitrary bytes into uuencoded text.

    Returns ASCII bytes with `begin 644 data\n` framing. Empty input is
    permitted and produces a valid frame with no payload lines.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes-like")
    data = bytes(data)
    body = b"".join(binascii.b2a_uu(data[i:i + 45]) for i in range(0, len(data), 45))
    return b"begin 644 data\n" + body + b"end\n"


def decode(text: bytes) -> bytes:
    """Decode uuencoded text back to bytes.

    Accepts either bytes or str. Requires a `begin` header and `end` footer.
    Filename in the header is ignored. Mode must be valid octal in 0-777.

    Raises UUencodeError on missing/structural issues.
    """
    if isinstance(text, str):
        text = text.encode("ascii", errors="replace")
    elif not isinstance(text, (bytes, bytearray)):
        raise TypeError("text must be bytes-like or str")
    text = bytes(text)

    if b"\r\n" in text:
        text = text.replace(b"\r\n", b"\n")
    if b"\r" in text:
        text = text.replace(b"\r", b"\n")

    try:
        lines = text.decode("ascii").split("\n")
    except UnicodeDecodeError as exc:
        raise UUencodeError("non-ASCII byte in encoded text: %s" % exc) from exc

    # Strip trailing empty strings from the final newline, but preserve blanks
    # inside the body — those carry length-0 data in some encoders.
    while lines and lines[-1] == "":
        lines.pop()

    if not lines or lines[0].strip() != "begin 644 data":
        raise UUencodeError("missing or malformed begin header")

    if not lines or lines[-1].strip() != "end":
        raise UUencodeError("missing end marker")

    result = bytearray()
    for line in lines[1:-1]:
        if not line:
            continue
        try:
            decoded = binascii.a2b_uu((line + "\n").encode("ascii"))
        except (binascii.Error, ValueError) as exc:
            raise UUencodeError("decode failed: %s" % exc) from exc
        result.extend(decoded)

    return bytes(result)
