def test_filter_by_year(client, sample_multiple_papers):
    """
    Test filter by year
    """
    response = client.get("/papers/?year=2017")
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Attention is All You Need"

def test_filter_by_tag(client, sample_multiple_papers):
    """
    Test filter by tags
    """
    response = client.get("/papers/?tag=Transformer")
    data = response.json()
    assert len(data) == 2
    titles = [p["title"] for p in data]
    assert "BERT: Pre-training of Deep Bidirectional Transformers" in titles

def test_search_by_keyword(client, sample_multiple_papers):
    """
    Test search keywords by title or abstract
    """
    response = client.get("/papers/?q=Reasoning")
    data = response.json()
    assert len(data) == 1
    assert "ReAct" in data[0]["title"]