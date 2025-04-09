import os
from openai import OpenAI
from dotenv import load_dotenv
from app.db.database import db

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def obtener_recomendacion_chatgpt(presupuesto: float, objetivo: str):
    pcs = []
    async for pc in db.pcs.find():
        pcs.append({
            "nombre": pc["nombre"],
            "precio": pc["precio"],
            "categoria": pc["categoria"],
            "componentes": pc["componentes"]
        })

    mensaje_usuario = f"""Tengo un presupuesto de {presupuesto} y quiero un PC para {objetivo}.
    Aquí está la base de datos disponible: {pcs}
    ¿Cuál me recomiendas y por qué?
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": mensaje_usuario}]
    )

    return response.choices[0].message.content
