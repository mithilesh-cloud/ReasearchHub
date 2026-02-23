
def build_research_prompt(question: str, paper_summaries: list[str]) -> str:
    joined = "\n".join(f"- {summary}" for summary in paper_summaries)
    return (
        "You are a research assistant. Use the supplied paper summaries to answer the question.\n"
        f"Question: {question}\n"
        f"Paper Summaries:\n{joined if joined else '- None provided'}"
    )
