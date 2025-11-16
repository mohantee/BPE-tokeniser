"""
BPE Tokenizer Gradio App
A simple interface to encode/decode text using a BPE tokenizer, similar to Tiktokenizer.
"""

import gradio as gr
import json
import os
from tokenizer import HindiTokenizer

# Initialize tokenizer
tokenizer = HindiTokenizer()

# Load pre-trained tokenizer if it exists
tokenizer_path = "hindi_tokenizer.json"
if os.path.exists(tokenizer_path):
    tokenizer.load(tokenizer_path)
    loaded = True
else:
    loaded = False
    print(f"Warning: {tokenizer_path} not found. Tokenizer not loaded.")


def encode_text(text):
    """Encode text to token IDs."""
    if not loaded:
        return "Error: Tokenizer not loaded. Please ensure hindi_tokenizer.json exists.", ""
    
    if not text.strip():
        return "Please enter some text to encode.", ""
    
    try:
        tokens = tokenizer.encode(text)
        
        # Create output display
        token_count = len(tokens)
        original_bytes = len(text.encode("utf-8"))
        compression_ratio = original_bytes / token_count if token_count > 0 else 0
        
        output = f"""**Encoded Tokens:**
        
Token IDs: {tokens}

**Statistics:**
- Input text length: {len(text)} characters
- Input bytes: {original_bytes} bytes
- Token count: {token_count}
- Compression ratio: {compression_ratio:.2f}X
"""
        return output, str(tokens)
    except Exception as e:
        return f"Error encoding text: {str(e)}", ""


def decode_tokens(token_str):
    """Decode token IDs back to text."""
    if not loaded:
        return "Error: Tokenizer not loaded. Please ensure hindi_tokenizer.json exists."
    
    if not token_str.strip():
        return "Please enter token IDs to decode."
    
    try:
        # Parse the token string
        # Handle formats like "[1, 2, 3]" or "1, 2, 3"
        token_str = token_str.strip()
        if token_str.startswith('[') and token_str.endswith(']'):
            token_str = token_str[1:-1]
        
        tokens = [int(t.strip()) for t in token_str.split(',')]
        decoded = tokenizer.decode(tokens)
        
        output = f"""**Decoded Text:**

{decoded}

**Statistics:**
- Token count: {len(tokens)}
- Output text length: {len(decoded)} characters
- Output bytes: {len(decoded.encode("utf-8"))} bytes
"""
        return output
    except ValueError as e:
        return f"Error: Invalid token format. Please enter comma-separated integers. Error: {str(e)}"
    except Exception as e:
        return f"Error decoding tokens: {str(e)}"


def create_interface():
    """Create and return the Gradio interface."""
    
    with gr.Blocks(title="BPE Tokenizer", theme=gr.themes.Soft()) as demo:
        gr.HTML("""
        <div style="text-align: center; margin-bottom: 10px;">
            <h1>🔤 BPE Tokenizer</h1>
            <p>Encode Hindi text to tokens and decode tokens back to text</p>
        </div>
        """)

        with gr.Accordion("ℹ️ About BPE Tokenizer", open=False):
            gr.Markdown("""
            ## About BPE Tokenizer
            This is a **Byte Pair Encoding (BPE)** tokenizer trained on Hindi text.
            ### How it works:
            1. **Encoding**: Converts text into token IDs that can be processed by language models
            2. **Decoding**: Converts token IDs back to readable text
            3. **Compression**: Shows how much the text is compressed during tokenization
            ### Features:
            - 🇮🇳 Supports Hindi text with proper Unicode handling
            - 📊 Shows compression statistics
            - ↔️ Bidirectional encoding/decoding
            - 🎯 Character and byte-level analysis
            ### Technical Details:
            - **Algorithm**: Byte Pair Encoding (BPE)
            - **Language**: Hindi (Devanagari script)
            - **Vocab Size**: 6000 tokens
            - **Input Format**: UTF-8 encoded text
            Built with ❤️ using Python and Gradio
            """)

        with gr.Row():
            # Encode Section
            with gr.Column():
                gr.Markdown("### Encode Text → Tokens")
                input_text = gr.Textbox(
                    label="Input Text",
                    placeholder="Enter text to encode...",
                    lines=5,
                    max_lines=10
                )
                encode_button = gr.Button("🔐 Encode", size="lg", variant="primary")
                encode_output = gr.Markdown(label="Output")
                token_ids = gr.Textbox(
                    label="Token IDs (for copying)",
                    interactive=False,
                    lines=3
                )
                encode_button.click(
                    fn=encode_text,
                    inputs=input_text,
                    outputs=[encode_output, token_ids]
                )
                gr.Examples(
                    examples=[
                        ["भारत की अर्थव्यवस्था दुनिया में तेजी से विकसित हो रही है।"],
                        ["नमस्ते, कैसे हो?"],
                        ["मेरा नाम राज है।"]
                    ],
                    inputs=input_text,
                    label="Example Texts"
                )

            # Decode Section
            with gr.Column():
                gr.Markdown("### Decode Tokens → Text")
                decode_input = gr.Textbox(
                    label="Token IDs",
                    placeholder="Enter token IDs like: 1, 2, 3 or [1, 2, 3]",
                    lines=5,
                    max_lines=10
                )
                decode_button = gr.Button("🔓 Decode", size="lg", variant="primary")
                decode_output = gr.Markdown(label="Output")
                decode_button.click(
                    fn=decode_tokens,
                    inputs=decode_input,
                    outputs=decode_output
                )
                gr.Examples(
                    examples=[
                        ["256, 257, 258"],
                    ],
                    inputs=decode_input,
                    label="Example Format"
                )
    return demo


if __name__ == "__main__":
    if not loaded:
        print("\n⚠️  WARNING: Tokenizer not loaded!")
        print(f"Make sure '{tokenizer_path}' exists in the same directory as this script.")
        print("\nTo train a new tokenizer, run: python main.py\n")
    
    demo = create_interface()
    demo.launch(share=True)
