import os

KNOWLEDGE_BASE_DIR = "knowledge_base"

def load_docs():
    """Load all .md files from the knowledge base into a list of dicts."""
    docs = []
    for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
        for fname in files:
            if fname.endswith(".md"):
                path = os.path.join(root, fname)
                with open(path, "r") as f:
                    content = f.read()
                docs.append({
                    "filename": fname.replace(".md", ""),
                    "path": path,
                    "content": content
                })
    return docs

def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Find the top_k most relevant docs for a given query using
    simple keyword matching. Returns list of matching doc dicts.
    """
    docs = load_docs()
    query_words = set(query.lower().split())

    scored = []
    for doc in docs:
        doc_words = set(doc["content"].lower().split())
        # score = number of query words that appear in the doc
        score = len(query_words & doc_words)
        if score > 0:
            scored.append((score, doc))

    # sort by score descending, return top_k
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]

def format_context(docs: list[dict]) -> str:
    """Format retrieved docs into a single context string for the prompt."""
    if not docs:
        return "No relevant documentation found."
    parts = []
    for doc in docs:
        parts.append(f"### {doc['filename']}\n{doc['content']}")
    return "\n\n".join(parts)