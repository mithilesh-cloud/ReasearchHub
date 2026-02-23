from xml.etree import ElementTree

import httpx

from app.schemas.paper import PaperResult

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}


async def search_papers(query: str, max_results: int = 10) -> list[PaperResult]:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max(1, min(max_results, 25)),
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(ARXIV_API, params=params)
        resp.raise_for_status()

    root = ElementTree.fromstring(resp.text)
    papers: list[PaperResult] = []

    for entry in root.findall("atom:entry", NS):
        authors = [author.findtext("atom:name", default="", namespaces=NS) for author in entry.findall("atom:author", NS)]
        papers.append(
            PaperResult(
                external_id=entry.findtext("atom:id", default="", namespaces=NS),
                title=(entry.findtext("atom:title", default="", namespaces=NS) or "").strip(),
                authors=[a for a in authors if a],
                published_date=entry.findtext("atom:published", default="", namespaces=NS),
                abstract=(entry.findtext("atom:summary", default="", namespaces=NS) or "").strip(),
                source="arxiv",
            )
        )

    return papers
