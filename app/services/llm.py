import anthropic
from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

def stream_response(chunks: list[str], question: str):
    context = "\n\n---\n\n".join(chunks)
    with client.messages.stream(
        model=settings.llm_model,
        max_tokens=1024,
        system=(
            "Eres el asistente de KallpAI. "
            "Responde ÚNICAMENTE basándote en el contexto proporcionado. "
            "Si la información no está en el contexto, dilo claramente. "
            "Responde en el mismo idioma que la pregunta."
        ),
        messages=[{
            "role": "user",
            "content": f"Contexto:\n{context}\n\nPregunta: {question}"
        }],
    ) as stream:
        for token in stream.text_stream:
            yield token