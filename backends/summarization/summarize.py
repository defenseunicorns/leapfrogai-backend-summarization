from langchain.text_splitter import SpacyTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import logging


from ..utils.openai_client import openai_client_opts, openai_prompt_opts

logger = logging.getLogger("summarize")

CHUNK_SIZE = 2048
CHUNK_OVERLAP = 256


def create_document(text: str, text_len: int) -> Document:
    logger.info(f"Beginning tokenized chunking of text length {text_len}")

    splitter = SpacyTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separator=" ",
        pipeline="sentencizer",
    )
    chunks = splitter.split_text(text)
    docs = [Document(page_content=text_chunk) for text_chunk in chunks]

    logger.info(
        f"Created {len(chunks)} x {CHUNK_SIZE} token chunks for text length {text_len}."
    )
    return docs


def summarize(text: str, model: str) -> str:
    text_len = len(text)

    logger.info(f"Beginning summarization of text length {text_len} using the {model} backend")

    llm = ChatOpenAI(
        **openai_client_opts,
        **openai_prompt_opts,
        model_name=model,
    )
    texts = create_document(text, text_len)

    initial_summary_template = "Your job is to write a coherent, bulleted summary that extracts all important ideas and action items from the given text: {text}"
    initial_summary_prompt = PromptTemplate.from_template(initial_summary_template)

    refine_summary_template = (
        "Your job is to write a coherent, bulleted summary that extracts all important ideas and action items from the given text. "
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary (only if needed) with some more context: {text}\n"
        "Given the new context, refine the original summary. If the context isn't useful, return the original summary."
    )
    refine_summary_prompt = PromptTemplate.from_template(refine_summary_template)
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=initial_summary_prompt,
        refine_prompt=refine_summary_prompt,
        input_key="input",
        output_key="output",
    )

    result = chain({"input": texts}, return_only_outputs=True)

    logger.info(f"Completed summarization of text length {text_len} using the {model} backend")

    summary = result["output"]

    return summary
