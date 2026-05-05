"""Batch-run the SDM assessment pipeline over a directory of transcripts."""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

from llm4sdm.pipeline import SDMPipeline

logger = logging.getLogger("llm4sdm.run")

EPILOG = """\
Examples
--------
  # Process every .docx / .json transcript under data/dev, writing one
  # *.json assessment per input under out/dev (relative paths preserved).
  python -m llm4sdm.run_pipeline \\
      --data-root data/dev --output-root out/dev

  # Run on a single file.
  python -m llm4sdm.run_pipeline \\
      --data-root data/dev/110023_NL.docx --output-root out/dev

  # Use a custom config (e.g. switch provider to vllm/ollama/openai).
  python -m llm4sdm.run_pipeline \\
      --data-root data/test --output-root out/test \\
      --config src/llm4sdm/config.yaml

Inputs
------
.docx -- raw transcripts (parsed by MedicalTranscriptProcessor).
.json -- preprocessed segments produced by scripts/preprocess_to_json.py;
         lets you inspect/edit the segmentation before running the LLM chain.

Output
------
For each input, a JSON file is written mirroring its path under --output-root,
with the suffix forced to .json. Contents are the dumped SDMAssessmentResponse
plus `num_chunks` (and `chunk_assessments` when the transcript was split).
"""


def collect_inputs(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted({*root.rglob("*.docx"), *root.rglob("*.json")})


def output_path_for(src: Path, data_root: Path, output_root: Path) -> Path:
    if data_root.is_file():
        rel = Path(src.name)
    else:
        rel = src.relative_to(data_root)
    return (output_root / rel).with_suffix(".json")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Batch-run the SDM assessment pipeline over transcripts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        required=True,
        help="Transcript file, or directory searched recursively for "
        ".docx/.json transcripts.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Directory where one *.json assessment per input is written, "
        "mirroring relative paths under --data-root.",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path(__file__).parent / "config.yaml",
        help="Path to the pipeline config file. Default: %(default)s",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable DEBUG-level logging.",
    )

    args = parser.parse_args()

    logging.getLogger().setLevel(
        logging.DEBUG if args.verbose else logging.INFO
    )

    logger.info("loading pipeline config: %s", args.config)
    pipeline = SDMPipeline(config_path=str(args.config))
    logger.info(
        "provider=%s  model=%s",
        pipeline.provider,
        pipeline.config["providers"][pipeline.provider].get("model_name"),
    )

    inputs = collect_inputs(args.data_root)
    if not inputs:
        logger.error("no .docx or .json inputs found under %s", args.data_root)
        return 1

    args.output_root.mkdir(parents=True, exist_ok=True)
    logger.info(
        "found %d transcript(s); writing results to %s",
        len(inputs),
        args.output_root,
    )

    n_ok = n_failed = 0
    t0 = time.perf_counter()

    for i, src in enumerate(inputs, start=1):
        dst = output_path_for(src, args.data_root, args.output_root)
        logger.info("[%d/%d] processing %s", i, len(inputs), src)
        t1 = time.perf_counter()

        try:
            result = pipeline.run(file_path=str(src))
        except Exception:
            logger.exception("[%d/%d] failed: %s", i, len(inputs), src)
            n_failed += 1
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        with dst.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        logger.info(
            "[%d/%d] wrote %s  (%.1fs, %d chunk(s))",
            i,
            len(inputs),
            dst,
            time.perf_counter() - t1,
            result.get("num_chunks", 1),
        )
        n_ok += 1

    logger.info(
        "done: ok=%d failed=%d  total=%.1fs",
        n_ok,
        n_failed,
        time.perf_counter() - t0,
    )
    return 0 if n_failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
