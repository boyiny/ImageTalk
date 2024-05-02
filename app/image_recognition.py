from transformers import DetrImageProcessor, DetrForObjectDetection, VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import os

class ImageRecognition:
    def __init__(self, model_name="nlpconnect/vit-gpt2-image-captioning", max_length=16, num_beams=4):
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.feature_extractor = ViTImageProcessor.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        self.gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

        # Initialize DETR object detection model
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
        self.detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    @staticmethod
    def get_image_paths(dir_path):
        return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    def detect_objects(self, image, threshold=0.9):
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.detection_model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]
        return [self.detection_model.config.id2label[label.item()] for label, score in zip(results["labels"], results["scores"])]

    def caption_image(self, image):
        pixel_values = self.feature_extractor(images=[image], return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)
        output_ids = self.model.generate(pixel_values, **self.gen_kwargs)
        caption = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption.strip()

    def predict_and_format(self, image_paths):
        image_info_list = []
        for i, image_path in enumerate(image_paths):
            image = Image.open(image_path).convert("RGB")
            detected_objects = self.detect_objects(image)
            caption = self.caption_image(image)
            detected_objects = list(set(detected_objects))
            # print(f"Img{i+1}: {detected_objects}, [{caption}];")
            image_info_list.append({'img': f'Img{i+1}', 'detected_objects': detected_objects, 'caption': caption})
            # image_info_list.append(f"Img{i+1}: {detected_objects}, [{caption}];")
        return image_info_list
    
if __name__ == '__main__':
    captioner = ImageRecognition()
    folder_location = '/Users/yangboyin/Code/Cambridge/ImageTalk/backend/test_img'
    image_paths = captioner.get_image_paths(folder_location)

    image_info_list = captioner.predict_and_format(image_paths)
