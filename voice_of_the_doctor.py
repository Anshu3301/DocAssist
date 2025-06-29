import os
from gtts import gTTS  # Google Text-to-speech
import elevenlabs      # ElevenLabs Text-to-speech
from elevenlabs.client import ElevenLabs   
import subprocess   # to interact with CLI (here playing audio files)
import platform


from dotenv import load_dotenv
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


# Use either gTTS or ElevenLabs for text-to-speech conversion
def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows": 
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath])
        elif os_name == "Linux": 
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text="Artificial intelligence (AI) is the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making."
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


# a bit SLOW
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio_stream = client.text_to_speech.stream(
        text= input_text,
        voice_id= "A5W9pR9OjIbu80J0WuDW",
        output_format= "mp3_22050_32", # .wav format
        model_id= "eleven_turbo_v2"
    )
    elevenlabs.save(audio_stream, output_filepath)   # save the file
    
    # play the audio file
    os_name = platform.system()
    try:        
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath])
            # subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])   # not working properly
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="elevenlabs_testing.mp3")