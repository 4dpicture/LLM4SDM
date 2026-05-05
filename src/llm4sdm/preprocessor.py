"""
Medical Conversation Transcript Preprocessor
Handles transcripts with format: TIMESTAMP SPEAKER: TEXT
"""

import re
import unicodedata
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from docx import Document as DocxDocument


@dataclass
class TranscriptSegment:
    """Represents a single segment of the transcript"""

    timestamp: str
    duration: float
    speaker: str
    speaker_full: str
    raw_text: str
    text: str
    text_length: int

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "duration": self.duration,
            "speaker": self.speaker,
            "speaker_full": self.speaker_full,
            "raw_text": self.raw_text,
            "text": self.text,
            "text_length": self.text_length,
        }


class MedicalTranscriptProcessor:
    """Processor for medical conversation transcripts"""

    # Speaker abbreviation mappings
    DEFAULT_SPEAKER_MAPPING = {
        "DR": "Dokter",
        "PT": "Patiënt",
        "CG": "Verzorgende",
        "CG1": "Verzorgende A",
        "CG2": "Verzorgende B",
        "CG11": "Verzorgende A",  # For typo in one of the transcripts
        # Add more mappings as needed
    }

    def __init__(self, max_chars: int = 4000, overlap_segments: int = 2):
        """
        Initialize processor with optional configuration

        Args:
            config: Configuration dictionary for text splitter settings
        """
        self.max_chars = max_chars
        self.overlap_segments = overlap_segments

    @staticmethod
    def clean_raw_text(text: str) -> str:
        # Normalize unicode (handles weird composed chars)
        text = unicodedata.normalize("NFKC", text)

        # Replace non-breaking spaces with normal spaces
        text = text.replace("\xa0", " ")

        # Normalize whitespace (but keep line structure)
        text = re.sub(r"[ \t]+", " ", text)  # collapse spaces, keep newlines

        return text.strip()

    @staticmethod
    def clean_sentence_start(text: str) -> str:
        """
        Remove leading punctuation/symbol characters from the beginning
        of a sentence, such as :, -, –, —, ;, ., commas, etc.

        Examples:
            ": hello world"      -> "hello world"
            "---Test sentence"   -> "Test sentence"
            "—  Example text"   -> "Example text"
            "  : - — Hi there"  -> "Hi there"
        """
        if not text:
            return text

        # Remove whitespace first, then leading unwanted chars
        cleaned = re.sub(r'^\s*[:;,\.\-–—_~!?\(\)\[\]{}"\']+\s*', "", text)

        # Repeat in case there are mixed groups separated by spaces
        cleaned = re.sub(
            r'^(?:\s*[:;,\.\-–—_~!?\(\)\[\]{}"\']+\s*)+', "", cleaned
        )

        return cleaned.strip()

    @staticmethod
    def _estimate_last_segment_duration(segments):
        ts = segments[-1]
        estimated_duration = sorted(
            [
                segment
                for segment in segments[:-1]
                if segment.speaker == ts.speaker
            ],
            key=lambda s: abs(s.text_length - ts.text_length),
        )[0].duration
        return estimated_duration

    @staticmethod
    def merge_consecutive_same_speaker(segments):
        """Collapse runs of the same speaker into one utterance."""
        merged = []
        for seg in segments:
            if merged and merged[-1].speaker == seg.speaker:
                merged[-1].text += " " + seg.text
                merged[-1].raw_text += " " + seg.raw_text
                merged[-1].text_length += seg.text_length
                merged[-1].duration += seg.duration
            else:
                merged.append(deepcopy(seg))
        return merged

    def _get_time_difference(self, time1: str, time2: str):
        """Calculate time difference in seconds between two timestamps"""
        try:
            t1 = datetime.strptime(time1, "%H:%M:%S")
            t2 = datetime.strptime(time2, "%H:%M:%S")
            diff = (t2 - t1).total_seconds()
            if diff == 0:
                return 0.5  # Assign a small default duration for zero-length segmentss
            return abs(diff)
        except Exception as e:
            print(f"Error parsing timestamps '{time1}' and '{time2}': {e}")
            return 0

    def read_docx(self, file_path: str) -> str:
        """Read text from a .docx file"""
        doc = DocxDocument(file_path)
        full_text = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(full_text)

    def parse_transcript(
        self, raw_text: str, speaker_mapping: dict | None = None
    ) -> List[TranscriptSegment]:
        """
        Parse raw transcript text into structured segments
        Args:
            raw_text: Raw transcript text with timestamps and speakers
        Returns:
            List of TranscriptSegment objects
        """
        segments = []
        speaker_mapping = speaker_mapping or self.DEFAULT_SPEAKER_MAPPING
        # Regex pattern to match both formats:
        # - 00:04:40 DR1 Text
        # - [00:04:40] D2 Text
        pattern = (
            r"^\[?(\d{2}:\d{2}:\d{2})\]?\s+([A-Z][A-Z0-9]+)[-:—]?\s+(.*)$"
        )
        lines = raw_text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(pattern, line)
            if match:
                timestamp, speaker, text = match.groups()
                if len(segments) >= 1:
                    segments[-1].duration = self._get_time_difference(
                        time1=timestamp, time2=segments[-1].timestamp
                    )

                speaker_full = speaker_mapping.get(speaker, speaker)
                clean_text = self.clean_sentence_start(text)
                text_length = len(clean_text)
                segments.append(
                    TranscriptSegment(
                        timestamp=timestamp,
                        speaker=speaker,
                        duration=-1,  # unavailable at the moment
                        speaker_full=speaker_full,
                        raw_text=text,
                        text=clean_text,
                        text_length=text_length,
                    )
                )
            else:
                # Handle continuation of previous segment or malformed lines
                if segments and not re.match(r"^\[?\d{2}:", line):
                    # Append to previous segment's text
                    segments[-1].text += " " + line.strip()

        segments[-1].duration = self._estimate_last_segment_duration(segments)
        segments = self.merge_consecutive_same_speaker(segments)
        return segments

    def to_json(self, segments: List[TranscriptSegment], output_path: str):
        """Save segments to JSON file"""
        import json

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                [s.to_dict() for s in segments],
                f,
                ensure_ascii=False,
                indent=2,
            )

    def process(
        self,
        file_path: str,
        speaker_mapping: dict | None = None,
        save_json: bool = False,
        extract_metadata: bool = False,
    ):
        """Processed segments can be saved as json for manual inspection"""
        assert file_path.endswith(".docx"), "Only .docx files are supported"
        raw_text = self.read_docx(file_path)
        cleaned_text = self.clean_raw_text(raw_text)
        segments = self.parse_transcript(cleaned_text, speaker_mapping)
        if save_json:
            output_path = file_path.rsplit(".", 1)[0] + "_processed.json"
            self.to_json(segments, output_path)
        metadata = {}
        if extract_metadata:
            metadata = self._extract_metadata(segments)
            return segments, metadata
        return segments, metadata

    def _extract_metadata(self, segments: List[TranscriptSegment]) -> Dict:
        """Extract useful metadata from transcript segments"""
        if not segments:
            return {}

        # Per-speaker accumulators
        speaker_duration = {}
        speaker_turns = {}
        speaker_text_length = {}

        for segment in segments:
            speaker = segment.speaker_full

            speaker_duration[speaker] = (
                speaker_duration.get(speaker, 0) + segment.duration
            )
            speaker_turns[speaker] = speaker_turns.get(speaker, 0) + 1
            speaker_text_length[speaker] = (
                speaker_text_length.get(speaker, 0) + segment.text_length
            )

        # Total conversation duration
        start_time = segments[0].timestamp
        end_time = segments[-1].timestamp
        last_duration = (
            segments[-1].duration if segments[-1].duration > 0 else 0
        )
        total_duration = (
            self._get_time_difference(start_time, end_time) + last_duration
        )

        # Speaking ratios (fraction of total duration)
        speaker_ratio = {
            speaker: round(dur / total_duration, 4)
            if total_duration > 0
            else 0
            for speaker, dur in speaker_duration.items()
        }

        return {
            "start_time": start_time,
            "end_time": end_time,
            "total_duration_seconds": total_duration,
            "total_segments": len(segments),
            "speakers": list(speaker_turns.keys()),
            "speaker_turns": speaker_turns,
            "speaker_duration_seconds": speaker_duration,
            "speaker_ratio": speaker_ratio,
            "speaker_text_length": speaker_text_length,
        }

    def chunk_segments(self, segments: List[TranscriptSegment]) -> List[str]:
        """
        Group whole segments into chunks under a soft token budget.
        Never splits a segment. Overlaps by N segments for context continuity.
        """

        def render(seg: TranscriptSegment) -> str:
            return f"{seg.speaker_full}: {seg.text}"

        chunks: List[str] = []
        current: List[TranscriptSegment] = []
        current_chars = 0

        for seg in segments:
            seg_chars = len(render(seg)) + 1  # +1 for newline

            if current_chars + seg_chars > self.max_chars and current:
                chunks.append("\n".join(render(s) for s in current))
                current = (
                    current[-self.overlap_segments :]
                    if self.overlap_segments
                    else []
                )
                current_chars = sum(len(render(s)) + 1 for s in current)

            current.append(seg)
            current_chars += seg_chars

        if current:
            chunks.append("\n".join(render(s) for s in current))

        return chunks

    def process_for_llm(
        self,
        file_path: str,
        speaker_mapping: dict | None = None,
        chunk: bool = False,
    ) -> List[str]:
        if file_path.endswith(".docx"):
            segments, _ = self.process(
                file_path,
                speaker_mapping=speaker_mapping,
                save_json=False,
                extract_metadata=False,
            )
        elif file_path.endswith(".json"):
            import json

            with open(file_path, "r", encoding="utf-8") as f:
                segments = [TranscriptSegment(**d) for d in json.load(f)]
        else:
            raise ValueError("Unsupported file format. Use .docx or .json")

        if not chunk:
            return ["\n".join(f"{s.speaker_full}: {s.text}" for s in segments)]
        return self.chunk_segments(segments)
