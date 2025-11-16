# build_hi_corpus_static.py
# Deterministic ~1MB Hindi Corpus Builder (NO randomness)

import unicodedata
from pathlib import Path

# -----------------------------------------------------------
# Fixed content chunks (these never change)
# -----------------------------------------------------------
NEWS = [
    "सरकार ने आज नए सुधारों की घोषणा की।",
    "दिल्ली में प्रदूषण का स्तर लगातार बढ़ रहा है।",
    "मौसम विभाग ने अगले सप्ताह बारिश की चेतावनी दी है।",
    "शेयर बाजार में तेजी का रुझान जारी है।",
    "शिक्षा नीति में बड़े बदलाव प्रस्तावित किए गए हैं।",
]

WIKI = [
    "भारत दक्षिण एशिया में स्थित एक विशाल देश है।",
    "हिमालय पर्वत विश्व की सबसे ऊँची पर्वत श्रृंखला है।",
    "गंगा और यमुना भारत की प्रमुख नदियाँ हैं।",
    "दिल्ली भारत की राजधानी है और ऐतिहासिक धरोहरों से समृद्ध है।",
    "कृषि भारत की अर्थव्यवस्था का प्रमुख स्तंभ है।",
]

STORY = [
    "रवि सुबह जल्दी उठकर बगीचे में टहलने गया।",
    "वहाँ फूलों की खुशबू और पक्षियों की चहचहाहट फैली हुई थी।",
    "अनुष्का ने पुराने घर का दरवाज़ा धीरे से खोला।",
    "सूरज की किरणें खिड़की से कमरे में प्रवेश कर रही थीं।",
    "रात की ख़ामोशी में अचानक एक आवाज़ गूँज उठी।",
]

DIALOGUE = [
    "अरे सुनो, आज शाम को कहाँ चलना है?",
    "कुछ नहीं, बस सोच रहा था कि कॉफ़ी पीने चलें।",
    "ठीक है, मैं आधे घंटे में पहुँचता हूँ।",
    "अच्छा, लेकिन पहले मुझे एक काम निपटाना है।",
    "ठीक है, कोई बात नहीं।",
]

PROVERBS = [
    "मेहनत का फल मीठा होता है।",
    "डर के आगे जीत है।",
    "जैसा बोओगे, वैसा काटोगे।",
    "नाच न जाने आँगन टेढ़ा।",
    "ऊँट के मुंह में जीरा।",
]

POETRY = [
    "चाँदनी रात में हवाएँ एक गीत गाती रहीं।",
    "समंदर की लहरों ने किनारे को पुकारा।",
    "दिल की धड़कनों में छिपी एक अजीब सी तान है।",
    "जंगलों की ख़ामोशी में भी जीवन की सरगम है।",
    "बारिश की बूंदों ने धरती पर अपनी कहानी लिखी।",
]

HINGLISH = [
    "आज का दिन काफी hectic था।",
    "तुमने वो movie देखी क्या?",
    "meeting थोड़ा लंबा हो गया।",
    "यह design काफ़ी cool लग रहा है।",
    "मेरे laptop की battery फिर खत्म हो गई।",
]

# -----------------------------------------------------------
# STATIC SYNTHETIC (NO randomness)
# -----------------------------------------------------------
# Pre-generate a fixed list of synthetic words
SYN_FIXED = []
syllables = [
    "क","ख","ग","घ","च","छ","ज","झ","ट","ठ","ड","ढ","त","थ",
    "द","ध","न","प","फ","ब","भ","म","य","र","ल","व","स","ह",
    "ा","ि","ी","ु","ू","े","ै","ो","ौ","ं","ः","्"
]

# deterministic synthetic words (fixed order)
for i in range(3000):  
    base = syllables[i % len(syllables)]
    matra = syllables[(i * 7) % len(syllables)]
    tail = syllables[(i * 13) % len(syllables)]
    SYN_FIXED.append(base + matra + tail + "।")

# -----------------------------------------------------------
# Combine into a deterministic 1MB corpus
# -----------------------------------------------------------

ALL = NEWS + WIKI + STORY + DIALOGUE + PROVERBS + POETRY + HINGLISH + SYN_FIXED

def build_static_corpus(outfile="hi_train.txt", size_bytes=1_000_000):
    lines = []
    total = 0

    # Deterministic loop through ALL repeatedly
    idx = 0
    L = len(ALL)

    while total < size_bytes:
        line = unicodedata.normalize("NFC", ALL[idx % L])
        idx += 1

        lines.append(line)
        total += len(line.encode("utf-8")) + 1

    corpus = "\n".join(lines)
    Path(outfile).write_text(corpus, encoding="utf-8")

    print("✓ Static corpus generated.")
    print(f"✓ File: {outfile}")
    print(f"✓ Size: {len(corpus.encode('utf-8'))} bytes")
    print(f"✓ Lines: {len(lines)}")

if __name__ == "__main__":
    build_static_corpus()
