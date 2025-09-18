class DocumentConverter:
    def convert(self, content: str) -> str:
        pass

class PDFConverter(DocumentConverter):
    def convert(self, content: str) -> str:
        return f"Converting to PDF: '{content[:20]}...' [PDF format]"

class DOCXConverter(DocumentConverter):
    def convert(self, content: str) -> str:
        return f"Converting to DOCX: '{content[:20]}...' [Microsoft Word format]"

class TXTConverter(DocumentConverter):
    def convert(self, content: str) -> str:
        return f"Converting to TXT: '{content[:20]}...' [Plain Text format]"

class DocumentConverterFactory:
    def create_converter(self, file_type: str) -> DocumentConverter:
        if file_type == "pdf":
            return PDFConverter()
        elif file_type == "docx":
            return DOCXConverter()
        elif file_type == "txt":
            return TXTConverter()
        else:
            raise ValueError(f"Unsupported file type for conversion: {file_type}")

factory = DocumentConverterFactory()
doc_content = "This is a sample document content that needs to be converted into various formats."

pdf_converter = factory.create_converter("pdf")
docx_converter = factory.create_converter("docx")
txt_converter = factory.create_converter("txt")

print(pdf_converter.convert(doc_content))
print(docx_converter.convert(doc_content))
print(txt_converter.convert(doc_content))

try:
    html_converter = factory.create_converter("html")
except ValueError as e:
    print(e)