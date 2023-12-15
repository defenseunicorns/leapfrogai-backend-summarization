from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import logging

from backends.utils.exceptions import (
    TEXT_STUFFING_FAILED,
    TEXT_CHUNKING_FAILED,
)

logger = logging.getLogger("utils")


def create_document(
    text: str,
    text_len: int,
    chunk_size: int = 1,
    chunk_overlap: int = 0,
    stuff: bool = False,
) -> list[Document]:
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
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separator=" ",
            )
            chunks = splitter.split_text(text)
            docs = [Document(page_content=text_chunk) for text_chunk in chunks]

            logger.info(
                f"Created {len(chunks)} x {chunk_size} token chunks for text length {text_len}."
            )

        except Exception as e:
            logger.error(f"{TEXT_CHUNKING_FAILED.detail}: {e}")
            raise TEXT_CHUNKING_FAILED

        return docs
