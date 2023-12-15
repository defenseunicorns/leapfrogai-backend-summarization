from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import logging

from backends.utils.create_document import create_document
from backends.utils._openai import OPENAI_CLIENT_OPTS, OPENAI_PROMPT_OPTS
from backends.utils.exceptions import (
    CHAIN_SUMMARIZATION_FAILED,
)

logger = logging.getLogger("summarization")

CHUNK_SIZE = 2048
CHUNK_OVERLAP = 128
MAX_SIZE = 5000


def summarize(text: str, model: str) -> str:
    try:
        text_len = len(text)

        logger.info(
            f"Beginning summarization of text length {text_len} using the {model} backend"
        )

        llm = ChatOpenAI(
            **OPENAI_CLIENT_OPTS,
            **OPENAI_PROMPT_OPTS,
            model_name=model,
        )

        texts = create_document(
            text, text_len, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )

        summary_system_prompt = (
            "Your job is to write an exhaustive summary that extracts all important details and action items while "
            "losing as little context and content as possible in the process. "
            "The summary should preserve all information and context, numbers, dates, locations and names."
            "The summary should be in paragraph format with full sentences. "
        )

        initial_summary_template = (
            summary_system_prompt + "The following is the text to be summarized: {text}"
        )
        initial_summary_prompt = PromptTemplate.from_template(initial_summary_template)

        iterative_summary_template = summary_system_prompt + (
            "You have been provided an existing summary up to a certain point: {existing_answer}\n"
            "You have the opportunity to refine and expand upon the existing summary (only if needed) with some more context: {text}\n"
            "Given the new context, refine and expand upon the the original summary. "
            "If the context isn't useful, return the original summary."
        )
        iterative_summary_prompt = PromptTemplate.from_template(
            iterative_summary_template
        )

        chain = load_summarize_chain(
            llm=llm,
            chain_type="refine",
            question_prompt=initial_summary_prompt,
            refine_prompt=iterative_summary_prompt,
            input_key="input",
            output_key="output",
        )
        result = chain({"input": texts}, return_only_outputs=True)

        logger.info(
            f"Completed summarization of text length {text_len} using the {model} backend"
        )

        summary = result["output"].strip()

        return summary

    except Exception as e:
        logger.error(f"{CHAIN_SUMMARIZATION_FAILED.detail}: {e}")
        raise CHAIN_SUMMARIZATION_FAILED
