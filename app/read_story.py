from gtts import gTTS
import os 

class ReadStory:
    def __init__(self, story):
        self.story = story
        self.language = 'en'   

    def story_reading(self):
        reader = gTTS(text=self.story, lang=self.language, slow=False)
        speech_file = "story.mp3"
        reader.save(speech_file)
        os.system('afplay ' + speech_file)

if __name__ == '__main__':
    reader = ReadStory("This is a test story.")
    reader.story_reading()
