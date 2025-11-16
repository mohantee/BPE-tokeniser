# tokenizer.py
import json
import regex as re
from collections import Counter

class HindiTokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {}
        self.vocab_size = 256  # byte tokens

        # Regex: words, numbers, punctuation, emojis
        self.pattern = re.compile(
            r"\p{L}+|\p{N}+|[^\s\p{L}\p{N}]+"
        )

    # -------------------------------------------------------
    # Pretokenize (NO ▁ prefix)
    # -------------------------------------------------------
    def pretokenize(self, text):
        # Example output: ["भारत", "की", "अर्थव्यवस्था", "।"]
        return re.findall(self.pattern, text)

    # -------------------------------------------------------
    # Byte-level utilities
    # -------------------------------------------------------
    def _get_stats(self, ids):
        stats = Counter()
        for a, b in zip(ids, ids[1:]):
            stats[(a, b)] += 1
        return stats

    def _merge(self, ids, pair, new_id):
        new = []
        i = 0
        while i < len(ids):
            if i < len(ids)-1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                new.append(new_id)
                i += 2
            else:
                new.append(ids[i])
                i += 1
        return new

    # -------------------------------------------------------
    # TRAIN BPE
    # -------------------------------------------------------
    def train(self, text, vocab_size=8000):
        print("→ Pre-tokenizing text using regex...")
        tokens = self.pretokenize(text)
        print(f"  Pretokenized into {len(tokens)} pieces")

        print("→ Converting tokens to UTF-8 byte stream...")
        ids = []
        for t in tokens:
            ids.extend(list(t.encode("utf-8")) + [255])  # 255 = word separator

        print("→ Training BPE merges...")
        next_id = 256
        total = vocab_size - 256

        for i in range(total):
            stats = self._get_stats(ids)
            if not stats:
                break

            pair = max(stats, key=stats.get)
            self.merges[pair] = next_id

            ids = self._merge(ids, pair, next_id)
            next_id += 1

            if i % 100 == 0:
                print(f"  Step {i}/{total}")

        # Build final vocab
        print("→ Building vocabulary table...")
        self.vocab = {i: bytes([i]) for i in range(256)}
        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]

        print("✓ Training complete.")
        orig_bytes = sum(len(t.encode('utf-8')) for t in tokens)
        print(f"Compression: {orig_bytes / len(ids):.2f}X")

    # -------------------------------------------------------
    # ENCODE
    # -------------------------------------------------------
    def encode(self, text):
        tokens = self.pretokenize(text)
        ids = []
        for t in tokens:
            ids.extend(list(t.encode("utf-8")) + [255])

        while True:
            stats = self._get_stats(ids)
            if not stats:
                break
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            ids = self._merge(ids, pair, self.merges[pair])

        return ids

    # -------------------------------------------------------
    # DECODE
    # -------------------------------------------------------
    def decode(self, ids):
        out = b"".join(self.vocab[i] for i in ids)
        out = out.replace(b"\xff", b" ")  # remove 255 separator
        return out.decode("utf-8", errors="replace")

    # -------------------------------------------------------
    # SAVE / LOAD
    # -------------------------------------------------------
    def save(self, path):
        data = {
            "merges": {f"{a},{b}": v for (a, b), v in self.merges.items()},
            "vocab": {str(k): v.decode("latin1") for k, v in self.vocab.items()}
        }
        json.dump(data, open(path, "w", encoding="utf-8"))
        print(f"✓ Tokenizer saved to {path}")

    def load(self, path):
        data = json.load(open(path, encoding="utf-8"))

        self.merges = {
            tuple(map(int, k.split(","))): v
            for k, v in data["merges"].items()
        }
        self.vocab = {
            int(k): v.encode("latin1")
            for k, v in data["vocab"].items()
        }
        print(f"✓ Loaded tokenizer from {path}")
