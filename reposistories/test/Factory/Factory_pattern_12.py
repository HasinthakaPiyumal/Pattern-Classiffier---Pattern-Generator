import abc

class Document(abc.ABC):
    @abc.abstractmethod
    def open(self):
        pass
    @abc.abstractmethod
    def save(self):
        pass

class PDFDocument(Document):
    def open(self):
        return "Opening PDF document"
    def save(self):
        return "Saving PDF document"

class WordDocument(Document):
    def open(self):
        return "Opening Word document"
    def save(self):
        return "Saving Word document"

class DocumentFactory:
    @staticmethod
    def create_document(doc_type: str) -> Document:
        if doc_type == "pdf":
            return PDFDocument()
        elif doc_type == "word":
            return WordDocument()
        else:
            raise ValueError("Invalid document type")

if __name__ == "__main__":
    pdf = DocumentFactory.create_document("pdf")
    print(pdf.open())
    word = DocumentFactory.create_document("word")
    print(word.save())