# u-uvl-7-bit-kit

A small, pure-Python encoder/decoder for uuencoded text — the 7-bit ASCII format historically used to ship binary attachments over Usenet and SMTP.

## Usage

```python
from u_uvl_7_bit_kit import encode, decode

encoded = encode(b"hello, world")
# b'begin 644 data\n%:&5L;&\^3R!W;W)D$  \nend\n'

decoded = decode(encoded)
# b'hello, world'
```

`decode` also accepts `str` for convenience. Both `encode` and `decode` raise `UUencodeError` (subclass of `ValueError`) on structural problems.

## Why this exists

The standard library ships `binascii.b2a_uu` / `a2b_uu` but leaves the `begin <mode> <filename>` framing entirely to the caller. This module fills that gap with one opinionated choice: the mode is fixed at 644 and the filename is fixed at `data`. The real uuencode format left filename handling ambiguous (is it a path? should the decoder create directories?), and rather than re-litigate that, this library refuses to take part.

## Edge cases

- Empty input encodes to a valid frame with no payload lines, and decodes back to empty bytes.
- Non-ASCII bytes in the encoded text raise `UUencodeError` rather than silently mangling.
- The decoder normalizes CRLF to LF before parsing, so text that transited a Windows mail system still decodes.
