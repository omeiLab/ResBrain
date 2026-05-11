def test_get_tags(client, sample_tag):
    '''
    Test retrieving all tags
    API: GET /tags/
    '''
    response = client.get("/tags/")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert any(t["name"] == sample_tag.name for t in data)

def test_get_tags_after_creating_paper(client, sample_tag):
    '''
    Test retrieving all tags after creating a paper
    The non-existed tags should be created
    API: GET /tags/
    '''
    payload = {
        "title": "Attention is All You Need",
        "authors": "Vaswani",
        "year": 2017,
        "venue": "NeurIPS",
        "pdf_path": "/path",
        "abstract": "...",
        "tags": ["Transformer", "Attention"] 
    }
    _ = client.post("/papers/", json=payload)
    response = client.get("/tags/")

    assert response.status_code == 200  # ok
    data = response.json()
    tag_set = set(sample_tag)
    assert data == list(tag_set.union(data))

def test_delete_tag(client, sample_tag):
    '''
    Test deleting the tag by a valid id
    API: DELETE /tags/{id}/
    '''
    response = client.delete(f"/tags/1")

    assert response.status_code == 204  # no content
    
    # test if the tag is deleted
    response = client.get(f"/tags/")
    data = response.json()
    
    assert sample_tag not in data

def test_delete_tag_by_invalid_id(client):
    '''
    Test deleting a tag by invalid id
    API: DELETE /tags/{id}
    '''
    response = client.delete(f"/tags/0")
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Tag not found"}

def test_delete_tag_removes_link_but_not_paper(client, sample_tag):
    """
    Test after deleting a tag, the related paper should remain
    API: DELETE /tags/{id}
    """
    # create a new paper
    payload = {
        "title": "Attention is All You Need",
        "authors": "Vaswani",
        "year": 2017,
        "venue": "NeurIPS",
        "pdf_path": "/path",
        "abstract": "...",
        "tags": ["Transformer", "Attention"] 
    }
    _ = client.post("/papers/", json=payload)

    # delete tag 1 : Attention
    response = client.delete("/tags/1")
    assert response.status_code == 204  # no content
    
    # fetch paper
    response = client.get("/papers/1")
    assert response.status_code == 200  # ok
    data = response.json()
    assert "Transformer" in data["tags"]
    assert "Attention" not in data["tags"]

