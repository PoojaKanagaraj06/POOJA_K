import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None


def generate_answer(question: str, context: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer the user's question only using the provided document context. "
                            "If the answer is not present in the context, say that the information "
                            "could not be found in the uploaded documents. Do not invent information."
                        ),
                    },
                    {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"},
                ],
                temperature=0,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "OpenAI request failed. Please try again or check the API configuration."

    context_lines = [line.strip() for line in context.splitlines() if line.strip()]
    if not context_lines:
        return "I could not find relevant information in the uploaded documents."

    first_lines = " ".join(context_lines[:3])
    return f"Based on the uploaded documents, the relevant information is: {first_lines}"
