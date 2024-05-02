from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from image_recognition import ImageRecognition
from story_generation import StoryGeneration
from read_story import ReadStory

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize_image_route():
    # Get the image data from the client
    image_paths = request.json['imagePaths']
    print("Image path:", image_paths)
    
    # Call the image recognition function
    image_recognition = ImageRecognition()

    # Get the image paths
    predictions = image_recognition.predict_and_format(image_paths)
    print("Captions:", predictions)
    print("JSON:", jsonify(predictions))

    # Update the image info to client
    return jsonify(predictions), 200, {'Content-Type': 'application/json'}

@app.route('/generate_story', methods=['POST'])
def generate_story_route():
    language_material = request.json['languageMaterial']
    print("Language material: \n", language_material)

    # Generate the story
    story_generation = StoryGeneration()

    image_obj = language_material['objects']
    image_caption = language_material['captions']
    keywords = language_material['keywords']
    language_style = language_material['languageStyle']
    # print("Image objects: \n" + image_obj)
    # print("Image captions: \n" + image_caption)
    # print("Keywords: \n" + keywords)
    # print("Language style: \n" + language_style)
    
    generated_story=[]
    generated_story = story_generation.generate_story(image_obj_all=image_obj, image_caption_all=image_caption, keywords_all=keywords, language_style=language_style)
    return jsonify(generated_story), 200, {'Content-Type': 'application/json'}

@app.route('/read_story', methods=['POST'])
def read_story_route():
    story = request.json['story']
    reader = ReadStory(story)
    reader.story_reading()
    print("Story: \n", story)
    return jsonify(story), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)  
