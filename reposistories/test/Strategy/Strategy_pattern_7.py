import abc

class ImageFilterStrategy(abc.ABC):
    @abc.abstractmethod
    def apply_filter(self, image_data):
        pass

class GrayscaleFilter(ImageFilterStrategy):
    def apply_filter(self, image_data):
        # Simulate grayscale conversion
        processed_data = f"Grayscale({image_data})"
        print(f"Applied Grayscale filter: {image_data} -> {processed_data}")
        return processed_data

class SepiaFilter(ImageFilterStrategy):
    def apply_filter(self, image_data):
        # Simulate sepia conversion
        processed_data = f"Sepia({image_data})"
        print(f"Applied Sepia filter: {image_data} -> {processed_data}")
        return processed_data

class ImageProcessor:
    def __init__(self, strategy: ImageFilterStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ImageFilterStrategy):
        self._strategy = strategy

    def process_image(self, image_data):
        return self._strategy.apply_filter(image_data)

if __name__ == "__main__":
    processor = ImageProcessor(GrayscaleFilter())
    processor.process_image("color_photo.jpg")

    processor.set_strategy(SepiaFilter())
    processor.process_image("vacation_pic.png")