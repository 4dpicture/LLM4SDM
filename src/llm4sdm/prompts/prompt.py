from pathlib import Path

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
