#!/usr/bin/env python3
"""
pdf_to_audiobook.py — Convert a PDF's text into an MP3 audiobook.

Uses pdfplumber for text extraction and Microsoft Edge's neural voices
(via edge-tts) for natural-sounding speech. Requires an internet connection.

Install:
    pip install pdfplumber edge-tts

Examples:
    python pdf_to_audiobook.py book.pdf
    python pdf_to_audiobook.py book.pdf --voice es-MX-DaliaNeural
    python pdf_to_audiobook.py book.pdf --start 5 --end 120 --rate +10%
    python pdf_to_audiobook.py book.pdf --pages-per-part 20 --merge
    python pdf_to_audiobook.py --list-voices en
"""

__version__ = "1.0.0"

import argparse
import asyncio
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import pdfplumber
    import edge_tts
except ImportError:
    sys.exit("Missing packages. Run ./install.sh (or: pip install -r requirements.txt)")

MAX_CHUNK_CHARS = 4000  # keep each TTS request a reasonable size


# ---------- Text extraction & cleanup ----------

def extract_pages(pdf_path, start, end):
    """Return a list of (page_number, text) for the requested range."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        end = min(end or total, total)
        for i in range(start - 1, end):
            text = pdf.pages[i].extract_text() or ""
            pages.append((i + 1, text))
            print(f"\rExtracting text: page {i + 1}/{end}", end="", flush=True)
    print()
    return pages


def find_repeated_lines(pages, threshold=0.3):
    """Detect running headers/footers: short lines that appear on many pages."""
    counts = Counter()
    for _, text in pages:
        lines = {l.strip() for l in text.splitlines() if 0 < len(l.strip()) < 80}
        counts.update(lines)
    min_hits = max(3, int(len(pages) * threshold))
    return {line for line, n in counts.items() if n >= min_hits}


def clean_text(text, repeated):
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s in repeated:
            continue
        if re.fullmatch(r"(page\s*)?\d+(\s*of\s*\d+)?", s, re.I):  # page numbers
            continue
        lines.append(s)
    text = "\n".join(lines)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)       # re-join hyphenated words
    text = re.sub(r"(?<![.!?:;])\n(?!\n)", " ", text)  # unwrap mid-sentence line breaks
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_into_chunks(text, max_chars=MAX_CHUNK_CHARS):
    """Split on sentence boundaries so speech never cuts mid-sentence."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) + 1 > max_chars and current:
            chunks.append(current)
            current = s
        else:
            current = f"{current} {s}".strip()
    if current:
        chunks.append(current)
    return chunks


# ---------- Text-to-speech ----------

async def synthesize(text, voice, rate, out_file):
    """Stream TTS audio for one part into an MP3 file."""
    chunks = split_into_chunks(text)
    with open(out_file, "wb") as f:
        for n, chunk in enumerate(chunks, 1):
            for attempt in range(3):
                try:
                    comm = edge_tts.Communicate(chunk, voice, rate=rate)
                    async for msg in comm.stream():
                        if msg["type"] == "audio":
                            f.write(msg["data"])
                    break
                except Exception as e:
                    if attempt == 2:
                        raise
                    print(f"\n  Retry chunk {n} ({e})")
                    await asyncio.sleep(2)
            print(f"\r  {out_file.name}: chunk {n}/{len(chunks)}", end="", flush=True)
    print()


async def list_voices(prefix):
    voices = await edge_tts.list_voices()
    for v in sorted(voices, key=lambda v: v["ShortName"]):
        if v["Locale"].lower().startswith(prefix.lower()):
            print(f'{v["ShortName"]:35} {v["Gender"]:7} {v["Locale"]}')


# ---------- Main ----------

async def main():
    p = argparse.ArgumentParser(description="Convert a PDF into an MP3 audiobook.")
    p.add_argument("pdf", nargs="?", help="Path to the PDF")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("-o", "--outdir", help="Output folder (default: <pdf name>_audiobook)")
    p.add_argument("-v", "--voice", default="en-US-AndrewNeural",
                   help="Voice name (see --list-voices)")
    p.add_argument("-r", "--rate", default="+0%", help="Speed, e.g. -10%% or +15%%")
    p.add_argument("--start", type=int, default=1, help="First page (1-based)")
    p.add_argument("--end", type=int, help="Last page (default: last page)")
    p.add_argument("--pages-per-part", type=int, default=25,
                   help="Pages per MP3 file (default 25)")
    p.add_argument("--merge", action="store_true",
                   help="Also create one combined MP3 of the whole book")
    p.add_argument("--save-text", action="store_true",
                   help="Save the cleaned text for review")
    p.add_argument("--list-voices", metavar="LOCALE", nargs="?", const="",
                   help="List voices, optionally filtered (e.g. en, es-MX)")
    args = p.parse_args()

    if args.list_voices is not None:
        await list_voices(args.list_voices)
        return
    if not args.pdf:
        p.error("please provide a PDF file")

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"File not found: {pdf_path}")
    outdir = Path(args.outdir or f"{pdf_path.stem}_audiobook")
    outdir.mkdir(parents=True, exist_ok=True)

    pages = extract_pages(pdf_path, args.start, args.end)
    repeated = find_repeated_lines(pages)
    cleaned = [(n, clean_text(t, repeated)) for n, t in pages]

    if not any(t for _, t in cleaned):
        sys.exit("No text found. This PDF is probably scanned images — run OCR first "
                 "(e.g. `ocrmypdf input.pdf output.pdf`) and try again.")

    if args.save_text:
        txt = outdir / f"{pdf_path.stem}.txt"
        txt.write_text("\n\n".join(f"[Page {n}]\n{t}" for n, t in cleaned), encoding="utf-8")
        print(f"Saved text to {txt}")

    # Group pages into parts
    parts = [cleaned[i:i + args.pages_per_part]
             for i in range(0, len(cleaned), args.pages_per_part)]
    width = len(str(len(parts)))
    files = []
    print(f"Creating {len(parts)} part(s) with voice {args.voice}...")
    for idx, group in enumerate(parts, 1):
        text = "\n\n".join(t for _, t in group if t)
        if not text:
            continue
        first, last = group[0][0], group[-1][0]
        out = outdir / f"{pdf_path.stem}_part{idx:0{width}d}_p{first}-{last}.mp3"
        await synthesize(text, args.voice, args.rate, out)
        files.append(out)

    if args.merge and files:
        merged = outdir / f"{pdf_path.stem}_full.mp3"
        with open(merged, "wb") as m:
            for f in files:
                m.write(f.read_bytes())  # edge-tts MP3 streams concatenate cleanly
        print(f"Merged audiobook: {merged}")

    print(f"Done! {len(files)} file(s) in {outdir.resolve()}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit("\nCancelled.")
