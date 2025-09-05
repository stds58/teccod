from fastapi import APIRouter, Query, Depends
from typing import Optional
from .opensearch_client import client

router = APIRouter()

@router.get("/search")
def search(
    q: str = Query(..., min_length=1),
    content_type: Optional[str] = None,
    opensearch = Depends(get_opensearch)
):
    query = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": q,
                    "fields": ["title", "content"]
                }
            },
            "filter": []
        }
    }
    if content_type:
        query["bool"]["filter"].append({"term": {"content_type": content_type}})

    result = opensearch.search(index="documents", body={"query": query})
    hits = []
    for hit in result["hits"]["hits"]:
        source = hit["_source"]
        snippet = (source["content"][:50] + "...") if len(source["content"]) > 50 else source["content"]
        hits.append({
            "title": source["title"],
            "snippet": snippet
        })

    return {"results": hits}
