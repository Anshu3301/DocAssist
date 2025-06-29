# UI for application
import gradio as gr
import os
from dotenv import load_dotenv

from brain_of_the_doctor import encode_image,analyze_image
from voice_of_the_doctor import text_to_speech_with_gtts,text_to_speech_with_elevenlabs
from voice_of_the_patient import record_audio,transcribe_with_groq

load_dotenv()

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    print("\nconverting speech_to_text with voice_of_the_patient...")
    speech_to_text_output = transcribe_with_groq(stt_model="whisper-large-v3", GROQ_API_KEY=os.getenv("GROQ_API_KEY"), audio_filepath=audio_filepath)

    # Handle the image input
    if image_filepath:
        print("analyzing image with brain_of_the_doctor...")
        doctor_response = analyze_image(user_input_text=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_response = "No image provided for me to analyze"

    print("converting text_to_speech with voice_of_the_doctor...")
    voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)

# http://127.0.0.1:7860

