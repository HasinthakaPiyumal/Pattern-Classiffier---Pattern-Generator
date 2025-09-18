class ImageOperation:
    def apply(self, image_data: str) -> str:
        pass

class GrayscaleFilter(ImageOperation):
    def apply(self, image_data: str) -> str:
        return f"Applied Grayscale filter to '{image_data[:20]}...'"

class SepiaFilter(ImageOperation):
    def apply(self, image_data: str) -> str:
        return f"Applied Sepia filter to '{image_data[:20]}...'"

class ResizeOperation(ImageOperation):
    def apply(self, image_data: str) -> str:
        return f"Resized '{image_data[:20]}...' to new dimensions"

class ImageProcessorFactory:
    def create_operation(self, operation_type: str) -> ImageOperation:
        if operation_type == "grayscale":
            return GrayscaleFilter()
        elif operation_type == "sepia":
            return SepiaFilter()
        elif operation_type == "resize":
            return ResizeOperation()
        else:
            raise ValueError(f"Unknown image operation: {operation_type}")

factory = ImageProcessorFactory()
image_file = "my_vacation_photo.jpg"

grayscale_op = factory.create_operation("grayscale")
sepia_op = factory.create_operation("sepia")
resize_op = factory.create_operation("resize")

print(grayscale_op.apply(image_file))
print(sepia_op.apply(image_file))
print(resize_op.apply(image_file))

try:
    crop_op = factory.create_operation("crop")
except ValueError as e:
    print(e)