def test_get_tags(client, sample_tag):
    '''
    Test retrieving all tags
    API: GET /tags/
    '''
    response = client.get("/tags/")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert any(t["name"] == sample_tag[0].name for t in data)
    assert any(t["name"] == sample_tag[1].name for t in data)

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

    client.post("/papers/", json=payload)
    response = client.get("/tags/")

    assert response.status_code == 200
    data = response.json()
    returned_tag_names = {tag["name"] for tag in data}
    expected_tag_names = {"Transformer", "Attention"}

    # if sample_tag fixture already creates tags:
    if isinstance(sample_tag, list):
        expected_tag_names.update(tag.name for tag in sample_tag)
    else:
        expected_tag_names.add(sample_tag.name)

    assert expected_tag_names.issubset(returned_tag_names)

def test_get_tag_by_id(client, sample_tag):
    '''
    Test retrieving a tag by id
    API: GET /tags/{id}
    '''
    response = client.get(f"/tags/1")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert data["name"] == sample_tag[0].name
    assert data["id"] == sample_tag[0].id 
    
def test_get_tag_by_invalid_id(client, sample_tag):
    '''
    Test retrieving a tag by invalid id
    API: GET /tags/{id}
    '''
    response = client.get("/tags/0")  
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Tag not found"}

def test_update_tag(client, sample_tag):
    '''
    Test updating an existed tag
    API: PUT /tags/{id}/
    '''
    payload = {"name": "Self-attention"}
    response = client.put(f"/tags/1/", json=payload)
    
    assert response.status_code == 204 
    
    response = client.get(f"/tags/1/")
    assert response.json()["name"] == "Self-attention"

def test_update_tag_by_invalid_id(client, sample_tag):
    '''
    Test updating an existed tag with invalid id
    API: PUT /tags/{id}/
    '''
    payload = {"name": "Self-attention"}
    response = client.put(f"/tags/0/", json=payload)
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Tag not found"}

def test_update_tag_conflict(client, sample_tag):
    '''
    Test the uniqueness of tag's name
    API: PUT /tags/{id}/
    '''
    response = client.put(f"/tags/1/", json={"name": "DL"})

    assert response.status_code == 400  # bad request
    assert response.json() == {"detail": "Tag name exists"}

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
    
    assert not any(t["id"] == sample_tag[0].id for t in data)

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
    tags = data['tags']
    assert data['title'] == payload["title"]
    assert any(t["name"] == "Transformer" for t in tags)
    assert not any(t["name"] == "Attention" for t in tags)

