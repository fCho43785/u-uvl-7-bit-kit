import unittest
from u_uvl_7_bit_kit import encode, decode, UUencodeError


class TestRoundTrip(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(decode(encode(b"")), b"")

    def test_one_byte(self):
        self.assertEqual(decode(encode(b"A")), b"A")

    def test_two_bytes(self):
        self.assertEqual(decode(encode(b"AB")), b"AB")

    def test_three_bytes(self):
        self.assertEqual(decode(encode(b"ABC")), b"ABC")

    def test_45_bytes_one_line(self):
        payload = b"X" * 45
        self.assertEqual(decode(encode(payload)), payload)

    def test_46_bytes_two_lines(self):
        payload = b"Y" * 46
        self.assertEqual(decode(encode(payload)), payload)

    def test_large_block(self):
        payload = bytes(range(256)) * 10
        self.assertEqual(decode(encode(payload)), payload)

    def test_all_byte_values(self):
        payload = bytes(range(256))
        self.assertEqual(decode(encode(payload)), payload)

    def test_accepts_bytearray(self):
        self.assertEqual(decode(encode(bytearray(b"hello"))), b"hello")


class TestDecodeErrors(unittest.TestCase):
    def test_missing_begin(self):
        with self.assertRaises(UUencodeError):
            decode(b"end\n")

    def test_missing_end(self):
        with self.assertRaises(UUencodeError):
            decode(b"begin 644 data\n")

    def test_non_ascii_input(self):
        bad = b"begin 644 data\n\xff\nend\n"
        with self.assertRaises(UUencodeError):
            decode(bad)

    def test_accepts_str(self):
        encoded = encode(b"cat").decode("ascii")
        self.assertEqual(decode(encoded), b"cat")

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            encode(42)
        with self.assertRaises(TypeError):
            decode(42)


class TestEncodeStructure(unittest.TestCase):
    def test_has_begin_and_end(self):
        out = encode(b"")
        self.assertIn(b"begin 644 data\n", out)
        self.assertIn(b"\nend\n", out)

    def test_empty_has_no_body(self):
        out = encode(b"")
        lines = out.split(b"\n")
        self.assertEqual(lines[0], b"begin 644 data")
        self.assertEqual(lines[1], b"end")


if __name__ == "__main__":
    unittest.main()
