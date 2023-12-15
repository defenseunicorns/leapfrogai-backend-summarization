from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.llm import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import logging


from ..utils.openai_config import OPENAI_CLIENT_OPTS, OPENAI_PROMPT_OPTS
from ..utils.exceptions import (
    CHAIN_SUMMARIZATION_FAILED,
    TEXT_STUFFING_FAILED,
    TEXT_CHUNKING_FAILED,
    UNGUIDED_REFINE_SUMMARIZATION_FAILED,
)
from .shared_prompts import BLUF_DESCRIPTION, NOTES_DESCRIPTION, ACTIONS_DESCRIPTION

logger = logging.getLogger("summarize.langchain")

CHUNK_SIZE = 2048
CHUNK_OVERLAP = 128


def create_document(text: str, text_len: int, stuff: bool = False) -> list[Document]:
    if stuff:
        try:
            logger.info(f"Stuffing text of length {text_len} into document")

            doc = [Document(page_content=text)]

            return doc

        except Exception as e:
            logger.error(f"{TEXT_STUFFING_FAILED.detail}: {e}")
            raise TEXT_STUFFING_FAILED
    else:
        logger.info(f"Beginning tokenized chunking of text length {text_len}")
        try:
            splitter = CharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                separator=" ",
            )
            chunks = splitter.split_text(text)
            docs = [Document(page_content=text_chunk) for text_chunk in chunks]

            logger.info(
                f"Created {len(chunks)} x {CHUNK_SIZE} token chunks for text length {text_len}."
            )

        except Exception as e:
            logger.error(f"{TEXT_CHUNKING_FAILED.detail}: {e}")
            raise TEXT_CHUNKING_FAILED

        return docs


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

        texts = create_document(text, text_len)

        SUMMARY_SYSTEM_PROMPT = (
            "Your job is to write an exhaustive summary that extracts all important details and open action items while "
            "losing as little context and content as possible in the process. Be wary of action items that may already be closed. "
            "The summary should preserve all important data, to include numbers, dates, locations and names. "
            "The summary should be in paragraph format with full sentences. "
        )

        initial_summary_template = (
            SUMMARY_SYSTEM_PROMPT + "The following is the text to be summarized: {text}"
        )

        initial_summary_prompt = PromptTemplate.from_template(initial_summary_template)

        iterative_summary_template = SUMMARY_SYSTEM_PROMPT + (
            "You have been provided an existing summary up to a certain point: {existing_answer}\n"
            "You have the opportunity to refine the existing summary (only if needed) with some more context: {text}\n"
            "Given the new context, refine the original summary. If the context isn't useful, return the original summary."
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


def unguided_refine(text: str, model: str) -> str:
    try:
        text_len = len(text)

        logger.info(
            f"Beginning refinement of summarization length {text_len} using the {model} backend"
        )

        llm = ChatOpenAI(
            **OPENAI_CLIENT_OPTS,
            **OPENAI_PROMPT_OPTS,
            model_name=model,
        )

        text = create_document(text, text_len, stuff=True)

        refine_summary_template = (
            "Your job is to reformat an exhaustive summary into 3 concise sections that are each separated by a newline character: "
            f"1. BOTTOM LINE UP FRONT: this section will be a {BLUF_DESCRIPTION}. "
            f"2. NOTES: this section will be a {NOTES_DESCRIPTION}. "
            f"3. ACTION ITEMS: this section will be a {ACTIONS_DESCRIPTION}. "
            "The summary should preserve all important data, to include numbers, dates, locations and names. "
            "The following is the summary to be reformatted: {text}"
        )
        refine_summary_prompt = PromptTemplate.from_template(refine_summary_template)

        llm_chain = LLMChain(llm=llm, prompt=refine_summary_prompt)
        stuff_chain = StuffDocumentsChain(
            llm_chain=llm_chain, document_variable_name="text"
        )
        summary = stuff_chain.run(text).strip()

        logger.info(
            f"Completed refinement of summary length {text_len} using the {model} backend"
        )

        return summary

    except Exception as e:
        logger.error(f"{UNGUIDED_REFINE_SUMMARIZATION_FAILED.detail}: {e}")
        raise UNGUIDED_REFINE_SUMMARIZATION_FAILED
