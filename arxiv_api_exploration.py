import feedparser
import urllib.parse

def fetch_arxiv_papers(query, max_results=5):
    query = urllib.parse.quote(query)

    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{query}&start=0&max_results={max_results}"
    )

    feed = feedparser.parse(url)

    papers = []

    for entry in feed.entries:
        paper = {
            "id": entry.id.split("/abs/")[-1],
            "title": entry.title.strip(),
            "abstract": entry.summary.strip(),
            "published": entry.published,
            "authors": [author.name for author in entry.authors],
            "pdf_url": next(
                (link.href for link in entry.links if link.type == "application/pdf"),
                None
            ),
            "categories": [tag.term for tag in entry.tags]
        }
        papers.append(paper)

    return papers
