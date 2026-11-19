#!/usr/bin/env python3
"""
Transcribe audio recordings locally, on a Mac, without sending anything anywhere.

Usage:
    python tools/transcribe.py [--language xx] [--out DIR] <audio file> [<audio file> ...]

For each file:
  1. decode to 16 kHz mono WAV with `afconvert` (a built-in macOS tool);
  2. transcribe with mlx-whisper (runs on the Apple Silicon GPU);
  3. write the transcript into the Ghostwriter incoming folder, in the turn format
     the skills expect: [mm:ss] text

Output folder, unless --out is given:
  ./.ghostwriter/transcripts/incoming   if ./.ghostwriter exists in the current folder
  ~/.ghostwriter/transcripts/incoming   otherwise

No diarisation: whisper does not tell speakers apart. The agent attributes speakers
from the content at step P0 of the method, and declares it.

Requires an environment created with:
    uv venv --python 3.11 .venv && uv pip install --python .venv/bin/python mlx-whisper numpy
"""
import argparse
import datetime as dt
import pathlib
import subprocess
import sys
import tempfile
import wave

import numpy as np

MODEL = "mlx-community/whisper-large-v3-turbo"


def default_output_dir() -> pathlib.Path:
    local = pathlib.Path.cwd() / ".ghostwriter"
    home = local if local.is_dir() else pathlib.Path.home() / ".ghostwriter"
    return home / "transcripts" / "incoming"


def decode(source: pathlib.Path, wav: pathlib.Path) -> None:
    subprocess.run(
        ["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", str(source), str(wav)],
        check=True,
    )


def load_wav(wav: pathlib.Path) -> np.ndarray:
    with wave.open(str(wav), "rb") as w:
        assert w.getnchannels() == 1 and w.getframerate() == 16000 and w.getsampwidth() == 2
        pcm = w.readframes(w.getnframes())
    return np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0


def mmss(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def transcribe(source: pathlib.Path, out_dir: pathlib.Path, language: str | None) -> pathlib.Path:
    import mlx_whisper  # late import: so --help works even without the venv

    with tempfile.TemporaryDirectory() as tmp:
        wav = pathlib.Path(tmp) / "audio.wav"
        print(f"[{source.name}] decoding…", flush=True)
        decode(source, wav)
        audio = load_wav(wav)
        duration = len(audio) / 16000
        print(f"[{source.name}] {mmss(duration)} of audio, transcribing with {MODEL}…", flush=True)
        result = mlx_whisper.transcribe(
            audio,
            path_or_hf_repo=MODEL,
            language=language,  # None = automatic language detection
            verbose=False,
            condition_on_previous_text=False,  # avoids repetition loops on silences
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    date = dt.datetime.fromtimestamp(source.stat().st_mtime).strftime("%Y-%m-%d")
    slug = source.stem.lower().replace(" ", "-")
    output = out_dir / f"{date}_manual_{slug}.txt"
    detected = result.get("language") or language or "auto"
    with output.open("w", encoding="utf-8") as f:
        f.write(f"# Transcript of: {source.name}\n")
        f.write(f"# Duration: {mmss(duration)} · model: {MODEL} · language: {detected}\n")
        f.write("# Speakers NOT separated: attribution to be done from the content.\n\n")
        for seg in result["segments"]:
            text = seg["text"].strip()
            if text:
                f.write(f"[{mmss(seg['start'])}] {text}\n")
    print(f"[{source.name}] → {output} ({len(result['segments'])} segments)", flush=True)
    return output


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Transcribe audio locally with mlx-whisper into the Ghostwriter incoming folder.",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="+", help="audio files to transcribe")
    parser.add_argument("--language", default=None, help="ISO code, e.g. en, it, de (default: auto-detect)")
    parser.add_argument("--out", default=None, help="output folder (default: Ghostwriter incoming folder)")
    args = parser.parse_args(argv[1:])

    out_dir = pathlib.Path(args.out).expanduser() if args.out else default_output_dir()
    for arg in args.files:
        p = pathlib.Path(arg).expanduser()
        if not p.exists():
            print(f"not found: {p}", file=sys.stderr)
            return 2
        transcribe(p, out_dir, args.language)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
