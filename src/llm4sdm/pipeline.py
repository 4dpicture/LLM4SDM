import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from .backends import BackendFactory
from .preprocessor import MedicalTranscriptProcessor
from .prompt import build_sdm_prompt
from .structured_output import SDMAssessmentResponse

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

        self.backend = BackendFactory.create_backend(
            self.provider,
            self.config["providers"][self.provider],
        )
        logger.info(f"SDM pipeline initialized with provider={self.provider}.")

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
        prompt = build_sdm_prompt(
            document_text=chunk,
            chunk_id=chunk_id,
            total_chunks=total_chunks,
        )
        return self.backend.generate(prompt)

    def _post_process(self, response):
        # If processing a single chunk, we can add any overall summary or adjustments here
        result = response.model_dump()
        return result

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
            f"Conversation split into {len(chunks)} chunks. Processing each chunk..."
        )

        chunk_assessments = []
        total = len(chunks)
        if total > 1:
            for idx, chunk in enumerate(chunks):
                logger.info(f"Running SDM assessment on chunk-{idx}...")
                response = self._assess(
                    chunk, chunk_id=idx, total_chunks=total
                )
                chunk_assessments.append(self._post_process(response))
                logger.info(
                    f"Chunk-{idx} processed. Mean score: {response.mean:.2f}"
                )
        else:
            response = self._assess(chunks[0])
            logger.info(
                f"SDM assessment complete. Mean score: {response.mean:.2f}"
            )
            return self._post_process(response)

        logger.info(f"SDM assessment complete for {total} chunks.")
        return {
            "num_chunks": total,
            "chunk_assessments": chunk_assessments,
        }
