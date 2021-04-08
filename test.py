# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os

# The text that you want to convert to audio
mytext = 'alert'

# Language in which you want to convert
language = 'en'


from pydub import AudioSegment
from pydub.playback import play



# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("alert.mp3")

song = AudioSegment.from_wav("alert.mp3")
play(song)

