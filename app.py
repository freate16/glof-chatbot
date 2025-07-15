import streamlit as st
from retriever import get_top_chunks
from llm_response import get_response

st.set_page_config(page_title="GLOF RAG Chatbot", layout="centered")

st.title("💬 GLOF Ontology Chatbot")
st.markdown("Hi! I'm your GLOF (Glacial Lake Outburst Flood) Assistant — here to help you understand risks, get early warnings, and explore safety measures related to glacial lake floods.")

query = st.text_input("Ask a question:")

if query:
    with st.spinner("🔍 Retrieving ontology chunks..."):
        chunks = get_top_chunks(query)
        context = "\n".join(chunks)

    with st.spinner("🧠 Generating LLM response..."):
        response = get_response(query, context)

    st.success("✅ Answer:")
    st.write(response)

    # st.info("📄 Retrieved Chunks:")
    # for i, chunk in enumerate(chunks, 1):
    #     st.markdown(f"**Chunk {i}:**\n```\n{chunk}\n```")
