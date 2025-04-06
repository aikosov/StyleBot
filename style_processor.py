import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from config import OPENAI_API_KEY

load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=OPENAI_API_KEY,
    project=os.getenv("OPENAI_PROJECT_ID"),
    organization=os.getenv("OPENAI_ORG_ID")
)
#openai.api_key = OPENAI_API_KEY


# Инструкции по стилям
STYLE_PROMPTS = {
    "disney": "Create a Disney-style portrait of the uploaded photo.",
    "ghibli": "Turn this photo into a Ghibli-style drawing.",
    "simpsons": "Make a Simpsons-style cartoon of the person in this image.",
    "southpark": "Transform the photo into South Park style.",
    "cyberpunk": "Create a Cyberpunk 2077 themed version of this photo with neon and futuristic atmosphere.",
    "vangogh": "Redraw the image in the painting style of Vincent van Gogh."
}

# Основная функция генерации изображения
def stylize_image(image_path: str, style: str, size: str) -> str:
    prompt = STYLE_PROMPTS.get(style, "Transform the photo into an artistic version.")

    try:
        with open(image_path, "rb") as image_file:
            #response = await openai.images.generate(
            response = client.images.edit(
                #model="dall-e-3",
                image=image_file,
                prompt=prompt,
                #quality="standart",
                n=1,
                size=size
            )
            
        return response.data[0].url
    except Exception as e:
        print("OpenAI error:", e)
        return None
