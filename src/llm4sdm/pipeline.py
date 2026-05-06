import concurrent.futures as cf
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .backends import BackendFactory
from .preprocessor import MedicalTranscriptProcessor
from .prompts.item_descriptions import OPTION_ITEMS
from .prompts.prompt import build_sdm_item_prompt, build_sdm_prompt
from .structured_output import SDMAssessmentResponse, SDMItemAssessment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class SDMPipeline:
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = str(Path(__file__).parent / "config.yaml")

        self.config = self.load_config(config_path)
        self.provider = self.config["default_provider"]

        prep_cfg = self.config.get("preprocessor", {})
        self.preprocessor = MedicalTranscriptProcessor(
            max_chars=prep_cfg.get("max_chars", 4000),
            overlap_segments=prep_cfg.get("overlap_segments", 2),
        )
        self.speaker_mapping = prep_cfg.get("speaker_mapping", None)
        self.chunk = prep_cfg.get("chunk", False)

        self.per_item_prompts = self.config.get("per_item_prompts", False)
        self.max_workers = self.config.get("max_workers", 12)

        self.backend = BackendFactory.create_backend(
            self.provider,
            self.config["providers"][self.provider],
        )
        logger.info(
            f"SDM pipeline initialized with provider={self.provider}, "
            f"per_item_prompts={self.per_item_prompts}."
        )

    def load_config(self, config_path: str) -> Dict:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    def _assess(
        self,
        chunk: str,
        chunk_id: Optional[int] = None,
        total_chunks: Optional[int] = None,
    ) -> SDMAssessmentResponse:
        if self.per_item_prompts:
            return self._assess_per_item(chunk)
        prompt = build_sdm_prompt(
            document_text=chunk,
            chunk_id=chunk_id,
            total_chunks=total_chunks,
        )
        return self.backend.generate(prompt)

    def _assess_one_item(
        self, chunk: str, item_index: int
    ) -> SDMItemAssessment:
        prompt = build_sdm_item_prompt(
            document_text=chunk, item_index=item_index
        )
        last_err: Optional[Exception] = None
        for attempt in (1, 2):
            try:
                return self.backend.generate(
                    prompt, response_model=SDMItemAssessment
                )
            except Exception as e:
                last_err = e
                logger.warning(
                    f"  item {item_index} attempt {attempt}/2 failed: "
                    f"{type(e).__name__}: {e}"
                )
        logger.error(
            f"  item {item_index} failed after 2 attempts; inserting sentinel"
        )
        err_name = type(last_err).__name__ if last_err else "Unknown"
        return SDMItemAssessment(
            score=0,
            evidence="GENERATION FAILED",
            justification=f"Item {item_index} failed after retry ({err_name})",
        )

    def _assess_per_item(self, chunk: str) -> SDMAssessmentResponse:
        n = len(OPTION_ITEMS)
        results: List[Optional[SDMItemAssessment]] = [None] * n

        if self.max_workers <= 1:
            logger.info(f"Running {n} per-item assessments sequentially...")
            for i in range(n):
                idx = i + 1
                item = self._assess_one_item(chunk, idx)
                results[i] = item
                logger.info(f"  item {idx}/{n} done (score={item.score})")
        else:
            logger.info(
                f"Running {n} per-item assessments in parallel "
                f"(max_workers={self.max_workers})..."
            )
            with cf.ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                futs = {
                    ex.submit(self._assess_one_item, chunk, i + 1): i + 1
                    for i in range(n)
                }
                for fut in cf.as_completed(futs):
                    idx = futs[fut]
                    item = fut.result()
                    results[idx - 1] = item
                    logger.info(f"  item {idx}/{n} done (score={item.score})")

        items = [r for r in results if r is not None]
        return SDMAssessmentResponse(items=items)

    def _post_process(self, response: SDMAssessmentResponse) -> Dict[str, Any]:
        return response.model_dump()

    def run(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        chunks = self.preprocessor.process_for_llm(
            file_path,
            speaker_mapping=self.speaker_mapping,
            chunk=self.chunk,
        )

        if len(chunks) == 1:
            logger.info("Processing conversation as a single transcript...")
            response = self._assess(chunks[0])
            result = response.model_dump()
            result["num_chunks"] = 1
            logger.info(
                f"SDM assessment complete. Mean score: {response.mean:.2f}"
            )
            return result

        logger.info(
            f"Conversation split into {len(chunks)} chunks. "
            "Processing each chunk..."
        )
        chunk_assessments = []
        total = len(chunks)
        for idx, chunk in enumerate(chunks):
            logger.info(f"Running SDM assessment on chunk-{idx}...")
            response = self._assess(chunk, chunk_id=idx, total_chunks=total)
            chunk_assessments.append(self._post_process(response))
            logger.info(
                f"Chunk-{idx} processed. Mean score: {response.mean:.2f}"
            )

        logger.info(f"SDM assessment complete for {total} chunks.")
        return {
            "num_chunks": total,
            "chunk_assessments": chunk_assessments,
        }
