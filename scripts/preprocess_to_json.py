"""
Manual inspection helper: convert .docx transcripts to .json using the
MedicalTranscriptProcessor so the parsing/segmentation can be eyeballed.

Examples:
    python scripts/preprocess_to_json.py data/dev/filename.docx
    python scripts/preprocess_to_json.py data/dev -o data/dev_json --metadata
    python scripts/preprocess_to_json.py data/dev/*.docx -o /tmp/inspect
"""

import argparse
import json
import sys
from pathlib import Path

from llm4sdm.preprocessor import MedicalTranscriptProcessor


def collect_docx(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            files.extend(sorted(p.rglob("*.docx")))
        elif p.suffix.lower() == ".docx":
            files.append(p)
        else:
            print(f"skipping non-docx path: {p}", file=sys.stderr)
    return files


def output_path(src: Path, out_dir: Path | None) -> Path:
    name = src.stem + "_processed.json"
    return (out_dir / name) if out_dir else src.with_name(name)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="One or more .docx files or directories containing .docx files.",
    )
    ap.add_argument(
        "-o",
        "--out-dir",
        type=Path,
        default=None,
        help="Directory to write JSON files into. Defaults to next to the source.",
    )
    ap.add_argument(
        "--metadata",
        action="store_true",
        help="Also write a *_metadata.json sibling file per transcript.",
    )
    ap.add_argument(
        "--max-chars",
        type=int,
        default=4000,
        help="Chunk size for the preprocessor (only affects metadata stats).",
    )
    ap.add_argument(
        "--overlap-segments",
        type=int,
        default=2,
        help="Segment overlap between chunks (only affects metadata stats).",
    )
    args = ap.parse_args()

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)

    files = collect_docx(args.inputs)
    if not files:
        print("no .docx files found", file=sys.stderr)
        return 1

    proc = MedicalTranscriptProcessor(
        max_chars=args.max_chars,
        overlap_segments=args.overlap_segments,
    )

    for src in files:
        segments, metadata = proc.process(
            str(src), extract_metadata=args.metadata
        )
        dst = output_path(src, args.out_dir)
        proc.to_json(segments, str(dst))
        print(f"{src} -> {dst}  ({len(segments)} segments)")

        if args.metadata:
            meta_path = dst.with_name(dst.stem + "_metadata.json")
            with meta_path.open("w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            print(f"  metadata -> {meta_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
