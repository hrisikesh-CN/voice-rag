import os, sys
from src.exception import CustomException
from langchain_text_splitters.base import TextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    UnstructuredCSVLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    UnstructuredHTMLLoader,
    UnstructuredImageLoader,
    ImageCaptionLoader,
    Docx2txtLoader,
    AmazonTextractPDFLoader)

from src.utils.convert_docx import convert_docx_to_pdf


class Readers:
    """Class to handle reading documents."""

    @staticmethod
    def load_and_split_document(loader_class, file_path, splitter: TextSplitter, **loader_kwargs):
        """
        Generic function to load and split documents using a specified loader class and text splitter.


        :param loader_class: The document loader class to use.
        :param file_path: The path to the document file.
        :param splitter: The text splitter to use for splitting the document.
        :param loader_kwargs: Additional keyword arguments to pass to the loader.
        :return: Chunks of documents.
        """
        try:
            loader = loader_class(file_path, **loader_kwargs)
            docs = loader.load()
            doc_splits = splitter.split_documents(docs)
            return doc_splits
        except Exception as e:
            raise CustomException(e, sys)

    def read_pdf_pypdf(self, file_path, splitter: TextSplitter):
        """Read PDFs, implement OCR for images within PDF, and return a list of chunks of documents."""
        return self.load_and_split_document(PyPDFLoader, file_path, splitter, extract_images=True)

    def read_with_aws(self, file_path, splitter: TextSplitter, **kwargs):
        """Read PDFs,images using amazon texract, and return a list of chunks of documents.
        This can read texts from images,
        images within pdfs,
        text in pdfs,"""
        return self.load_and_split_document(AmazonTextractPDFLoader, file_path, splitter, **kwargs)

    def read_txt(self, file_path, splitter: TextSplitter):
        """Read text files and return a list of chunks of documents."""
        return self.load_and_split_document(TextLoader, file_path, splitter)

    # Additional functions for other document types can be implemented similarly.
    def read_excel(self, file_path, splitter: TextSplitter):
        """Read Excel files and return a list of chunks of documents."""
        return self.load_and_split_document(UnstructuredExcelLoader, file_path, splitter)

    def read_csv(self, file_path, splitter: TextSplitter):
        """Read CSV files and return a list of chunks of documents."""
        return self.load_and_split_document(UnstructuredCSVLoader, file_path, splitter)

    def read_markdown(self, file_path, splitter: TextSplitter):
        """Read Markdown files and return a list of chunks of documents."""
        return self.load_and_split_document(UnstructuredMarkdownLoader, file_path, splitter)

    def read_ppt(self, file_path, splitter: TextSplitter):
        """Read PowerPoint files and return a list of chunks of documents."""
        return self.load_and_split_document(UnstructuredPowerPointLoader, file_path, splitter)

    def read_docx(self, file_path, splitter: TextSplitter):
        """Read Docx files and return a list of chunks of documents."""
        # convert docx to pdf to extract texts from images within the doc effectively
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path).split('.')[0]
        convert_docx_to_pdf(source_file_path=file_path, dest_folder=file_dir)
        converted_pdf_path = os.path.join(
            file_dir,
            file_name + ".pdf"
        )

        return self.read_pdf_pypdf(converted_pdf_path, splitter)

    def read_html(self, file_path, splitter: TextSplitter):
        """Read HTML files and return a list of chunks of documents."""
        return self.load_and_split_document(UnstructuredHTMLLoader, file_path, splitter)

    def read_image(self, file_path, splitter: TextSplitter):
        """Read image files and return a list of chunks of documents."""
        return self.load_and_split_document(UnstructuredImageLoader, file_path, splitter)

    def read_image_caption(self, file_path, splitter: TextSplitter):
        """Read image files and return a list of chunks of documents with captions."""
        return self.load_and_split_document(ImageCaptionLoader, file_path, splitter)
