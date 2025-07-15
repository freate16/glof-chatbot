from dotenv import load_dotenv
import os
from openai import OpenAI
 
load_dotenv() 
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_response(query, context):
    system_prompt = (
        "You are a glacier lake outburst flood (GLOF) risk assessment expert. "
        "Based on the provided ontology knowledge, answer the user's query accurately, "
        "clearly, and concisely. Provide explanations where helpful, and use domain-relevant terminology."
        "\n\nOntology Context:\n" + context
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content
