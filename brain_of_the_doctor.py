import os
import base64  # for encoding the image
from groq import Groq # for interacting with the Groq API
from dotenv import load_dotenv # for loading environment variables
from PIL import Image # for image processing


# image_path = "C:/Users/saina/Downloads/dandruff.jpeg"
# image_path = "C:/Users/saina/Downloads/pimple.jpg"


def resize_image(image_path, max_size=(512, 512)):
    img = Image.open(image_path)
    img.thumbnail(max_size)
    img.save(image_path)

# Encode the image to base64
def encode_image(image_path): # for sharing with gradio
    print("resizing image...")
    resize_image(image_path)  # Resize the image first
    print("Encoding image...")
    with open(image_path, "rb") as image_file:   # supports jpg and png formats
        return base64.b64encode(image_file.read()).decode('utf-8')


# loading env. variables from .env file
load_dotenv()
key = os.getenv("GROQ_API_KEY")

# print(key)

def analyze_image(encoded_image, model="meta-llama/llama-4-scout-17b-16e-instruct", user_input_text = 'Is there any problem you see?'):
    client = Groq(api_key=f"{key}")

    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{user_input_text}. "
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ]

    response = client.chat.completions.create(
        messages = messages,
        model = model,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    # print(response)
    return response.choices[0].message.content