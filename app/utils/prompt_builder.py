def build_research_prompt(question: str, paper_contexts: list[str]) -> str:
    context_block = "\n\n".join(f"Paper {i+1}:\n{ctx}" for i, ctx in enumerate(paper_contexts))
    return (
        "You are ResearchHub AI, an expert research assistant.\n"
        "Use only the provided paper context where possible.\n"
        "If context is limited, clearly say assumptions and provide cautious synthesis.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer in concise bullet points with practical research insights."
    )
