from .single_prompt import single_prompt
from .multi_prompt import multi_prompt
from .outlines import outlines
from backends.summarize.lib.types import AVAILABLE_REFINEMENT_OPTIONS, SECTIONS
from backends.utils.exceptions import REFINE_SUMMARIZATION_METHOD_DOES_NOT_EXIST


def stringify_sections(sections: SECTIONS):
    result = ""
    for key, value in sections.items():
        result += f"{key}: {value}. "
    return result


def raise_refine_error():
    raise REFINE_SUMMARIZATION_METHOD_DOES_NOT_EXIST


def refine(
    text: str,
    model: str,
    sections: SECTIONS,
    refine_method: AVAILABLE_REFINEMENT_OPTIONS,
):
    section_strings = stringify_sections(sections)

    REFINEMENT_METHODS = {
        "single-prompt": single_prompt,
        "multi-prompt": multi_prompt,
        "outlines": outlines,
    }

    refined_summary = REFINEMENT_METHODS.get(refine_method, lambda: raise_refine_error)(
        text=text, model=model, section_strings=section_strings
    )

    return refined_summary
