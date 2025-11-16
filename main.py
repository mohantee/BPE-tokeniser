# main.py
import json
from tokenizer import HindiTokenizer

def main():
    print("Loading Hindi training text...")

    # ----------------------------------------------
    # Load plain Hindi text file 
    # ----------------------------------------------
    with open("data.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Join lines to form the corpus
    text = "\n".join(lines)

    print(f"Loaded {len(lines)} lines")
    print(f"Total text length: {len(text)} characters")

    print("\nFirst 500 characters:")
    print(text[:500])

    # ----------------------------------------------
    # Train Hindi Tokenizer
    # ----------------------------------------------
    print("\n" + "="*60)
    print("Training Hindi Tokenizer...")
    print("="*60)

    tokenizer = HindiTokenizer()
    tokenizer.train(text, vocab_size=6000)  # you can change vocab_size

    tokenizer.save("hindi_tokenizer.json")

    # ----------------------------------------------
    # Test Tokenizer
    # ----------------------------------------------
    print("\n" + "="*60)
    print("Testing tokenizer...")
    print("="*60)

    test_text = "भारत की अर्थव्यवस्था दुनिया में तेजी से विकसित हो रही है।"
    print("Original text:", test_text)

    encoded = tokenizer.encode(test_text)
    print("\nEncoded:", encoded)
    print("Token count:", len(encoded))

    comp = len(test_text.encode("utf-8")) / len(encoded)
    print(f"Compression Ratio: {comp:.2f}X")

    decoded = tokenizer.decode(encoded)
    print("\nDecoded:", decoded)
    print("Match:", decoded == test_text)


if __name__ == "__main__":
    main()
