import openai
import os
from dotenv import load_dotenv
from config import OPENAI_API_KEY

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#openai.api_key = OPENAI_API_KEY


# Инструкции по стилям
STYLE_PROMTS = {
    "disnay": "Create a Disnay-style portrait of the uploaded photo.",
    "ghibly": "Turn this photo into a Ghibli-style drawing.",
    "simpsons": "Make a Simpsons-style cartoon of the person in this image.",
    "southpark": "Transform the photo into South Park style.",
    "cyberpunk": "Create a Cyberpunk 2077 themed version of this photo with neon and futuristic atmosphere.",
    "vangogh": "Redraw the image in the painting style of Vincent van Gogh."
}

# Основная функция генерации изображения
async def stylize_image(image_path: str, style: str, size: str) -> str:
    promt = STYLE_PROMTS.get(style, "Transform the photo into an artistic version.")

    try:
        response = await openai.Image.acreate_edit(
            image=open(image_path, "rb"),
            mask=None,
            prompt=prompt,
            n=1,
            size=size # формат выбираем динамически (1:1, 16:9, и т.д.)
        )
        return response["data"][0]["url"]
    except Exception as e:
        print("OpenAI error:", e)
        return None
