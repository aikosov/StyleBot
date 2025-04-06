import openai
import os
from dotenv import load_dotenv
from config import OPENAI_API_KEY

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#openai.api_key = OPENAI_API_KEY


# Инструкции по стилям
STYLE_PROMPTS = {
    "disney": "Create a Disnay-style portrait of the uploaded photo.",
    "ghibli": "Turn this photo into a Ghibli-style drawing.",
    "simpsons": "Make a Simpsons-style cartoon of the person in this image.",
    "southpark": "Transform the photo into South Park style.",
    "cyberpunk": "Create a Cyberpunk 2077 themed version of this photo with neon and futuristic atmosphere.",
    "vangogh": "Redraw the image in the painting style of Vincent van Gogh."
}

# Основная функция генерации изображения
async def stylize_image(image_path: str, style: str, size: str) -> str:
    prompt = STYLE_PROMPTS.get(style, "Transform the photo into an artistic version.")

    try:
        response = await openai.image.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standart",
            n=1
        )
            
        return response["data"][0]["url"]
    except Exception as e:
        print("OpenAI error:", e)
        return None
