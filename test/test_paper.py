def test_create_paper(client):
    ''' 
    Test the creation of a new paper 
    API: POST /papers/
    '''
    payload = {
        "title": "Attention is All You Need",
        "authors": "Vaswani et al.",
        "abstract": "The dominant sequence transduction models...",
        "year": 2017,
        "venue": "NeurIPS",
        "pdf_path": "/path/to/pdf"
    }
    response = client.post("/papers/", json=payload)
    
    assert response.status_code == 201  # created
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data
    
def test_get_all_paper(client, sample_paper):
    '''
    Test retrieving all papers
    API: GET /papers/
    '''
    response = client.get("/papers/")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == sample_paper.title
    
def test_get_paper_by_id(client, sample_paper):
    '''
    Test retrieving a paper by id
    API: GET /papers/{id}
    '''
    response = client.get(f"/papers/{sample_paper.id}")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert data["title"] == sample_paper.title 
    assert data["id"] == sample_paper.id 
    
def test_get_paper_by_invalid_id(client, sample_paper):
    '''
    Test retrieving a paper by invalid id
    API: GET /papers/{id}
    '''
    response = client.get("/papers/0")  
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Paper not found"}
    
def test_update_paper(client, sample_paper):
    '''
    Test updating a paper by id
    API: PUT /papers/{id}
    '''
    payload = {
        "title": "Updated Paper",
        "authors": "Updated Author",
        "abstract": "Updated abstract",
        "year": 2024,
        "venue": "Updated Venue",
        "pdf_path": "/updated/path/to/pdf"
    }
    response = client.put(f"/papers/{sample_paper.id}", json=payload)
    
    assert response.status_code == 204  # no content
    
    # Verify the update
    response = client.get(f"/papers/{sample_paper.id}")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert data["id"] == sample_paper.id 
    assert data[0]["title"] == payload["title"]
    assert data[0]["year"] == payload["year"]
    
def test_update_paper_by_invalid_id(client, sample_paper):
    '''
    Test updating a paper by invalid id
    API: PUT /papers/{id}
    '''
    payload = {
        "title": "Updated Paper",
        "authors": "Updated Author",
        "abstract": "Updated abstract",
        "year": 2024,
        "venue": "Updated Venue",
        "pdf_path": "/updated/path/to/pdf"
    }
    response = client.put(f"/papers/0", json=payload)
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Paper not found"}
    
def test_delete_paper(client, sample_paper):
    '''
    Test deleting a paper by id
    API: DELETE /papers/{id}
    '''
    response = client.delete(f"/papers/{sample_paper.id}")
    
    assert response.status_code == 204  # no content
    
    # test if the paper is deleted
    response = client.get(f"/papers/{sample_paper.id}")
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Paper not found"}
    
def test_delete_paper_by_invalid_id(client, sample_paper):
    '''
    Test deleting a paper by invalid id
    API: DELETE /papers/{id}
    '''
    response = client.delete(f"/papers/0")
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Paper not found"}