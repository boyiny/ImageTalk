from openai import OpenAI
import ctypes
import re

class StoryGeneration:

    def __init__(self) -> None:
        self.API_KEY = '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'
        self.client = OpenAI(api_key=self.API_KEY)
        self.image_info_list = []
        self.keyword_list = []
        self.avoid_list = []
        self.iteration = 0
        self.TEMPERATURE = 0.5
        self.last_storystory=[]


    def pop_up_chatgpt_error_notification(self) -> None:
        ctypes.windll.user32.MessageBoxW(0, "ChatGPT server has reached the capacity, please try this function later.", "Info", 0)

    def extract_image_info(self) -> None:
        pass

    def generate_story(self, image_obj_all, image_caption_all , keywords_all, language_style):
        

        material_list = []

        image_obj_list = image_obj_all.split("\n")
        image_caption_list = image_caption_all.split("\n")
        keywords_list = keywords_all.split("\n")
        
        edit_image_obj_list = []
        edit_image_caption_list = []
        edit_keywords_list = []

        if image_obj_list != None:
            for image_obj in image_obj_list:
                image_obj_in_one_img = image_obj.split(": ")[-1]
                image_obj_in_one_img_list = image_obj_in_one_img.split(",")
                obj_list = []
                for obj in image_obj_in_one_img_list:
                    obj = re.sub(r'[^\w]', '', obj)
                    obj_list.append(obj)
                edit_image_obj_list.append(obj_list)
        
        if image_caption_list != None:
            for image_caption in image_caption_list:
                image_caption_in_one_img = image_caption.split(": ")[-1]
                edit_image_caption_list.append(image_caption_in_one_img)
        
        if keywords_list != None:
            for keywords in keywords_list:
                keywords_in_one_img = keywords.split(": ")[-1]
                keywords_in_one_img_list = keywords_in_one_img.split(",")
                edit_keywords_list.append(keywords_in_one_img_list)

        for obj, caption, keyword in zip(edit_image_obj_list, edit_image_caption_list, edit_keywords_list):
            material_list.append({'object': obj, 
                                  'caption': caption, 
                                  'keyword': keyword})
            
        story_material = f"language_style: {language_style}; "    
        for i, material in enumerate(material_list):
            story_material += f"Material {i}: image_insights: ['{material['caption']}'], {material['object']}, keywords: {material['keyword']}; "

        print(f"Story material: {story_material}")


        prompt = [
            {"role": "system", "content": f"Based on the details provided below, craft a concise story that accurately reflects the information given without adding extraneous details: \
            1. 'image_insights': These insights can be utilized in the story or serve as background information; \
            however, be aware that the accuracy of the detected objects might vary. Feel free to disregard irrelevant or less confident details.\
            2. 'keywords': These must be included in the narrative as a key part.\
            Please craft a first-person account, from my perspective, of an event I actively participated in, maintaining a coherent and true-to-source narrative. \
            Do not add made-up content.\
            3. 'language_style': Use the language style to construct the narrative."},
            {"role": "user", "content": f"{story_material}"}
            ]

        story = []

        response = self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=prompt
                )
        story = response.choices[0].message.content
        print(story)
        
        return story

if __name__ == '__main__':
    model_chatgpt = StoryGeneration()


    image_obj = "Img1: mountain; \nImg2: sky, cloud; \nImg3: tree, leaves, water; \nImg4: building."
    image_caption = "Img1: A mountain range with an elevator. \nImg2: A clear sky with a few clouds. \nImg3: A tree with green leaves standing near water. \nImg4: A tall building with many windows."
    keywords = "Img1: happy, tired; \nImg2: excited, curious; \nImg3: calm, peaceful; \nImg4: busy, noisy."
    language_style = "Use short sentences and simple words."
    
    story_list=[]
    story_list = model_chatgpt.generate_story(image_obj_all=image_obj, image_caption_all=image_caption, keywords_all=keywords, language_style=language_style)