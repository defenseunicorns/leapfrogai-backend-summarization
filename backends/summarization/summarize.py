from langchain.text_splitter import SpacyTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document

from ..utils.openai_client import openai_client_opts


def create_document(text: str) -> Document:
    splitter = SpacyTextSplitter(
        chunk_size=4000,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(text)
    docs = [Document(page_content=text_chunk) for text_chunk in chunks]
    return docs


def summarize(text: str, model: str) -> str:
    llm = ChatOpenAI(
        **openai_client_opts,
        model_name=model,
        max_tokens=2048,
        temperature=0.5,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    texts = create_document(text)

    prompt_template = """Write a concise summary of the following:
    {text}
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    refine_template = (
        "Your job is to produce a final summary in the form of clear and coherent bullets\n"
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "Given the new context, refine the original summary"
        "If the context isn't useful, return the original summary."
    )
    refine_prompt = PromptTemplate.from_template(refine_template)
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
        input_key="texts",
        output_key="summary",
    )

    result = chain({"texts": texts}, return_only_outputs=True)

    summary = result["summary"]

    return summary
