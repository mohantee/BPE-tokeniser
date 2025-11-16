# 🔤 BPE Tokenizer - Hindi Text

A lightweight **Byte Pair Encoding (BPE)** tokenizer trained on Hindi text, featuring an interactive web UI built with Gradio (similar to Tiktokenizer).

## 🌟 Quick Start

### Try Online
👉 **[Try the demo on Hugging Face Spaces](https://huggingface.co/spaces)** (coming soon!)

### Local Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Train tokenizer (optional - if hindi_tokenizer.json doesn't exist)
python main.py

# Run the web UI
python app.py
```

Then open your browser to `http://localhost:7860` 🚀

## 📝 How to Use

### Encoding (Text → Tokens)
1. Go to the **Encode** tab
2. Paste Hindi text
3. Click **🔐 Encode**
4. See token IDs and compression statistics

### Decoding (Tokens → Text)
1. Go to the **Decode** tab
2. Paste token IDs like `[256, 257, 258]` or `256, 257, 258`
3. Click **🔓 Decode**
4. Get back the original text

## 🎨 Features

✅ **Web Interface**
- Clean, intuitive Gradio UI (like Tiktokenizer)
- Encode and decode in real-time
- Copy-paste token IDs easily
- Pre-loaded example texts

📊 **Statistics**
- Token count
- Compression ratio
- Byte-level analysis
- Input/output size comparison

🇮🇳 **Hindi Support**
- Handles Devanagari script perfectly
- UTF-8 encoding support
- Proper Unicode handling

## 📂 Project Structure

```
BPE-tokeniser/
├── app.py                    # 🎨 Gradio web interface (main app)
├── tokenizer.py             # 🔧 BPE tokenizer implementation
├── main.py                  # 🚂 Training script
├── hindi_tokenizer.json     # 📦 Pre-trained tokenizer
├── data.txt                 # 📚 Training data
├── requirements.txt         # 📋 Dependencies
├── README.md               # 📖 This file
├── DEPLOY.md               # 🚀 Deployment guide
└── .gitignore              # 🙈 Git ignore rules
```

## 🔬 Technical Details

### Algorithm: Byte Pair Encoding (BPE)

**What it does:**
- Starts with 256 byte-level tokens (0-255)
- Iteratively merges most frequent byte pairs
- Creates new token IDs (256+)
- Reaches desired vocabulary size (default: 6,000)

**Why BPE?**
- ✅ Handles any Unicode text
- ✅ Balances vocabulary size and sequence length
- ✅ Better compression than character-level tokenization
- ✅ Better context preservation than word-level tokenization

### Example Tokenization

```
Input Text:    "नमस्ते कैसे हो"
                     ↓
Pre-tokenize:  ["नमस्ते", "कैसे", "हो"]
                     ↓
UTF-8 Bytes:   [224, 164, ..., 255, 224, 165, ..., 255, ...]
                     ↓
Apply BPE:     [512, 513, 514, 515]  ← Token IDs
                     ↓
Compression:   32 bytes → 4 tokens (8X compression)
```

### Tokenizer Configuration

| Setting | Value |
|---------|-------|
| **Language** | Hindi (Devanagari) |
| **Vocabulary Size** | 6,000 tokens |
| **Base Tokens** | 256 (bytes) + 1 (separator) |
| **Training Data** | `data.txt` |
| **Output Format** | List of integers |

## 🚀 Deploy to Hugging Face Spaces

### Option 1: Using Hugging Face Web Interface
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **Create new Space**
3. Choose **Gradio** as SDK
4. Upload files from this repo
5. Done! Your app runs automatically

### Option 2: Using Git (Git LFS for large files)
```bash
# Clone your space repo
git clone https://huggingface.co/spaces/[username]/bpe-tokenizer

# Copy files
cp app.py tokenizer.py requirements.txt hindi_tokenizer.json /path/to/space/

# Push (with LFS for json file)
cd /path/to/space/
git lfs track "*.json"
git add .
git commit -m "Add BPE tokenizer"
git push
```

### Option 3: Docker Deployment
```bash
# Build Docker image
docker build -t bpe-tokenizer .

# Run container
docker run -p 7860:7860 bpe-tokenizer
```

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

## 🛠️ Installation

### Requirements
- Python 3.7+
- pip or conda

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Dependencies
- **gradio** - Web UI framework
- **regex** - Advanced regex for Unicode handling

## 📚 Usage Examples

### Example 1: Simple Greeting
```
Input:  "नमस्ते"
Output: [256, 257, 258]
Stats:  12 bytes → 3 tokens (4X compression)
```

### Example 2: Full Sentence
```
Input:  "भारत की अर्थव्यवस्था दुनिया में तेजी से विकसित हो रही है।"
Output: [256, 257, 258, 259, ...] (60+ tokens)
Stats:  112 bytes → 60 tokens (1.9X compression)
```

## 🔄 Training Your Own Tokenizer

### Using Your Data

1. Replace `data.txt` with your Hindi text
2. Update `main.py` if needed:
   ```python
   tokenizer.train(text, vocab_size=8000)  # Change vocab size if desired
   ```
3. Run training:
   ```bash
   python main.py
   ```
4. New `hindi_tokenizer.json` will be created

### Training Parameters
- `vocab_size`: Number of tokens (default: 6000, range: 256-50000)
- Larger vocab → better compression but more memory
- Smaller vocab → worse compression but faster inference

## 📖 API Reference

### Initialize
```python
from tokenizer import HindiTokenizer

tokenizer = HindiTokenizer()
tokenizer.load("hindi_tokenizer.json")
```

### Encode Text to Tokens
```python
tokens = tokenizer.encode("नमस्ते")
print(tokens)  # [256, 257, 258]
```

### Decode Tokens to Text
```python
text = tokenizer.decode([256, 257, 258])
print(text)  # "नमस्ते"
```

### Save/Load Tokenizer
```python
# Save
tokenizer.save("my_tokenizer.json")

# Load
tokenizer.load("my_tokenizer.json")
```

## 🎯 Tips & Tricks

### For Best Results
1. **Use UTF-8 encoding** - Ensure all input files are UTF-8
2. **Clean data** - Remove duplicates and irrelevant content
3. **Large dataset** - Use more training data for better tokenization
4. **Tune vocab size** - Test different sizes for your use case

### Troubleshooting
- **Tokenizer not loading?** - Check `hindi_tokenizer.json` exists
- **Wrong encoding?** - Ensure input is valid Hindi text
- **Memory issues?** - Reduce vocabulary size
- **Slow inference?** - Use smaller vocabulary

## 🤝 Contributing

Want to improve this? 
- Add support for other languages
- Optimize tokenization speed
- Improve UI/UX
- Add more examples
- Better documentation

Feel free to fork and submit PRs!

## 📄 License

MIT License - Use freely!

## 🙏 Acknowledgments

- Based on [BPE algorithm](https://en.wikipedia.org/wiki/Byte_pair_encoding)
- UI inspired by [Tiktokenizer](https://tiktokenizer.vercel.app/)
- Built with [Gradio](https://www.gradio.app/) 
- Python's excellent [regex](https://github.com/mrabarnett/regex) library

---

## 📞 Support

- 📖 Check [DEPLOY.md](DEPLOY.md) for deployment help
- 🐛 Open an issue for bugs
- 💡 Suggestions welcome!
- 📧 Contact maintainer

---

Made with ❤️ for Hindi NLP | Last updated: November 2025