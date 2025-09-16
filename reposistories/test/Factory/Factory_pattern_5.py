class DocumentProcessor:
    def process(self):
        raise NotImplementedError

class PDFProcessor(DocumentProcessor):
    def process(self):
        return "Processing a PDF document."

class WordProcessor(DocumentProcessor):
    def process(self):
        return "Processing a Word document."

class TextProcessor(DocumentProcessor):
    def process(self):
        return "Processing a plain text document."

class DocumentProcessorFactory:
    @staticmethod
    def get_processor(doc_type):
        if doc_type == "pdf":
            return PDFProcessor()
        elif doc_type == "word":
            return WordProcessor()
        elif doc_type == "text":
            return TextProcessor()
        else:
            raise ValueError("Invalid document type")

if __name__ == "__main__":
    pdf_proc = DocumentProcessorFactory.get_processor("pdf")
    print(pdf_proc.process())
    word_proc = DocumentProcessorFactory.get_processor("word")
    print(word_proc.process())
    text_proc = DocumentProcessorFactory.get_processor("text")
    print(text_proc.process())
    try:
        excel_proc = DocumentProcessorFactory.get_processor("excel")
        print(excel_proc.process())
    except ValueError as e:
        print(e)