from guidance import gen, models, newline
import guidance
import logging

from ..utils.exceptions import GUIDED_REFINE_SUMMARIZATION_FAILED
from .shared_prompts import BLUF_DESCRIPTION, NOTES_DESCRIPTION, ACTIONS_DESCRIPTION


logger = logging.getLogger("summarize.guidance")


@guidance
def format_summary(lm, text: str):
    lm += f"""{text}
    Extract from the text {BLUF_DESCRIPTION}: {gen('bluf')}
    From the text, generate {NOTES_DESCRIPTION}:\n- {gen('notes')}
    From the text, generate a {ACTIONS_DESCRIPTION}\n- {gen('actions')}
    """

    return lm


def guided_refine(text: str):
    text_len = len(text)

    logger.info(f"Beginning guided refinement of summarization length {text_len}")

    # model location is relative to where the application initializing command is
    llm = models.Transformers(model=".model")

    try:
        result = llm + format_summary(text)
    except Exception as e:
        logger.error(f"{GUIDED_REFINE_SUMMARIZATION_FAILED.detail}: {e}")
        raise GUIDED_REFINE_SUMMARIZATION_FAILED

    summary = (
        f"""BOTTOM LINE UP FRONT (BLUF):
    {result["bluf"]}
    
    DETAILED NOTES:
    {result["notes"]}
    
    CAPTURED ACTION ITEMS:
    {result["actions"]}
    """
    ).strip()

    logger.info(f"Completed guided refinement of summarization length {text_len}")

    return summary
