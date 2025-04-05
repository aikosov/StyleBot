from dotenv import load_dotenv
import os


# Загружаем данные из файла .env
load_dotenv()

#Забираем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_AOI_KEY")
