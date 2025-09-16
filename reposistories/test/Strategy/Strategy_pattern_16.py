class FilterStrategy:
    def apply_filter(self, image_data):
        raise NotImplementedError
class GrayscaleFilter(FilterStrategy):
    def apply_filter(self, image_data):
        return f"Applied Grayscale to '{image_data}'"
class SepiaFilter(FilterStrategy):
    def apply_filter(self, image_data):
        return f"Applied Sepia to '{image_data}'"
class ImageProcessor:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def process_image(self, image_data):
        return self._strategy.apply_filter(image_data)
processor = ImageProcessor(GrayscaleFilter())
print(processor.process_image("photo.jpg"))
processor.set_strategy(SepiaFilter())
print(processor.process_image("selfie.png"))