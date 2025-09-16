import abc

class CompressionStrategy(abc.ABC):
    @abc.abstractmethod
    def compress(self, data):
        pass

class ZipCompression(CompressionStrategy):
    def compress(self, data):
        print(f"Compressing data with ZIP: '{data}' -> '{data[:5]}...[ZIP]'")
        return f"{data[:5]}...[ZIP]"

class GzipCompression(CompressionStrategy):
    def compress(self, data):
        print(f"Compressing data with GZIP: '{data}' -> '{data[:5]}...[GZIP]'")
        return f"{data[:5]}...[GZIP]"

class FileCompressor:
    def __init__(self, strategy: CompressionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: CompressionStrategy):
        self._strategy = strategy

    def process_file(self, file_content):
        return self._strategy.compress(file_content)

if __name__ == "__main__":
    compressor = FileCompressor(ZipCompression())
    compressed_data_zip = compressor.process_file("This is a long text file content that needs to be compressed.")

    compressor.set_strategy(GzipCompression())
    compressed_data_gzip = compressor.process_file("Another piece of text content for GZIP compression.")