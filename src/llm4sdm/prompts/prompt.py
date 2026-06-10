from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader

from .item_descriptions import OPTION_ITEMS
from .item_examples import EXAMPLE_ASSESSMENTS_SYNTHETIC

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)

template = env.get_template("sdm_prompt.jinja")
item_template = env.get_template("sdm_item_prompt.jinja")
summary_template = env.get_template("sdm_summary_prompt.jinja")
item_summary_template = env.get_template("sdm_item_summary_prompt.jinja")

examples = EXAMPLE_ASSESSMENTS_SYNTHETIC
# examples = None


def build_sdm_prompt(
    document_text: str,
    examples=None,
    chunk_id=None,
    total_chunks=None,
) -> str:
    return template.render(
        items=OPTION_ITEMS,
        examples=examples or [],
        document_text=document_text,
        chunk_id=chunk_id,
        total_chunks=total_chunks,
    )


def build_sdm_item_prompt(
    document_text: str, item_index: int, examples=examples
) -> str:
    """Build a prompt scoped to a single OPTION-12 item.

    `item_index` is 1-based (1..12).
    """
    if not 1 <= item_index <= len(OPTION_ITEMS):
        raise ValueError(
            f"item_index must be 1..{len(OPTION_ITEMS)}, got {item_index}"
        )
    return item_template.render(
        document_text=document_text,
        item_index=item_index,
        item=OPTION_ITEMS[item_index - 1],
        examples=(examples or {}).get(item_index, []),
    )


def build_sdm_summary_prompt(chunk_assessments: List[Dict[str, Any]]) -> str:
    """Build a prompt that reduces per-chunk 12-item assessments into a final
    12-item assessment for the full conversation.

    `chunk_assessments` is a list of dicts as produced by
    `SDMAssessmentResponse.model_dump()`, each containing an `"items"` list of
    12 per-item evaluations.
    """
    return summary_template.render(
        items=OPTION_ITEMS,
        chunk_assessments=chunk_assessments,
    )


def build_sdm_item_summary_prompt(
    evaluations: List[Any], item_index: int
) -> str:
    """Build a prompt that reduces per-excerpt evaluations of a single
    OPTION-12 item into a final evaluation.

    `evaluations` is a list of per-chunk evaluations for the given item
    (objects or dicts with `score`, `evidence`, `justification`).
    `item_index` is 1-based (1..12).
    """
    if not 1 <= item_index <= len(OPTION_ITEMS):
        raise ValueError(
            f"item_index must be 1..{len(OPTION_ITEMS)}, got {item_index}"
        )
    return item_summary_template.render(
        evaluations=evaluations,
        item_index=item_index,
        item=OPTION_ITEMS[item_index - 1],
    )
