import os
from fastapi import FastAPI, UploadFile, File, Form
from backend.services.loader import load_document
from backend.services.chunker import chunk_documents
from backend.services.vectorstore import create_or_update_vectorstore, load_vectorstore
from backend.services.retriever import get_mmr_retriever
from backend.services.llm import get_llm

app = FastAPI()


@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    workspace_id: str = Form(...)
):
    content = await file.read()
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(content)

    docs = load_document(temp_path, file.filename)
    chunks = chunk_documents(docs)

    create_or_update_vectorstore(chunks, workspace_id)

    os.remove(temp_path)

    return {"status": "indexed"}


@app.post("/query/")
async def query(
    workspace_id: str = Form(...),
    question: str = Form(...)
):
    try:
        vectorstore = load_vectorstore(workspace_id)

        if not vectorstore:
            return {"answer": "No documents indexed yet."}

        retriever = get_mmr_retriever(vectorstore)
        llm = get_llm()

        docs = retriever.invoke(question)
        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}
"""

        result = llm.invoke(prompt)

        return {"answer": result.content}

    except Exception as e:
        print("ERROR IN QUERY:", str(e))
        return {"answer": f"Backend error: {str(e)}"}