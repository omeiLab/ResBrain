def test_create_note(client, sample_paper):
    '''
    Test the creation of a new note
    API: POST /papers/{paper_id}/notes/
    '''
    payload = {'content': 'Test Note'}
    response = client.post("/papers/1/notes/", json=payload)

    assert response.status_code == 201  # created
    data = response.json()
    assert data['content'] == payload['content']

def test_create_note_by_invalid_id(client, sample_paper):
    '''
    Test the creation of a new note with not-exist paper
    API: POST /papers/{paper_id}/notes/
    '''
    payload = {'content': 'Test Note'}
    response = client.post("/papers/0/notes/", json=payload)

    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Paper not found"}

def test_get_note(client, sample_paper, sample_note):
    '''
    Test retrieving all notes from a paper
    API: GET /papers/{paper_id}/notes/
    '''
    response = client.get("/papers/1/notes/")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert len(data) >= 1
    assert data[0]['paper_id'] == sample_paper.id
    assert data[0]['paper_id'] == sample_note.paper_id
    assert data[0]['content'] == sample_note.content

def test_get_note_by_invalid_paper_id(client, sample_paper, sample_note):
    '''
    Test retrieving all notes from a not-exist paper
    API: GET /papers/{paper_id}/notes/
    '''
    response = client.get("/papers/0/notes/")
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Paper not found"}

def test_get_note_by_id(client, sample_paper, sample_note):
    '''
    Test retrieving all notes from a paper
    API: GET /notes/{note_id}/
    '''
    response = client.get("/notes/1/")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert data['paper_id'] == sample_paper.id
    assert data['paper_id'] == sample_note.paper_id
    assert data['content'] == sample_note.content

def test_get_note_by_invalid_note_id(client, sample_paper, sample_note):
    '''
    Test retrieving all notes from a not-exist paper
    API: GET /notes/{note_id}
    '''
    response = client.get("/notes/0/")
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Note not found"}

def test_update_note(client, sample_paper, sample_note):
    '''
    Test updating a note by id
    API: PATCH /notes/{note_id}
    '''
    payload = {'content': 'Updated note'}
    response = client.patch("/notes/1/", json=payload)

    assert response.status_code == 204  # no content
    
    # Verify the update
    response = client.get(f"/notes/1/")
    
    assert response.status_code == 200  # ok
    data = response.json()
    assert data['paper_id'] == sample_paper.id
    assert data['paper_id'] == sample_note.paper_id
    assert data['content'] == payload['content']

def test_update_note_by_invalid_note_id(client, sample_paper, sample_note):
    '''
    Test updating a note by invalid id
    API: PATCH /notes/{note_id}
    '''
    payload = {'content': 'Updated note'}
    response = client.patch("/notes/0/", json=payload)
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Note not found"}

def test_delete_note(client, sample_paper, sample_note):
    '''
    Test deleting a note by id
    API: DELETE /notes/{note_id}
    '''
    response = client.delete(f"/notes/1/")
    
    assert response.status_code == 204  # no content
    
    # test if the note is deleted
    response = client.get(f"/notes/1/")

    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Note not found"}

    # check the paper
    response = client.get(f"/papers/1/")
    data = response.json()

    assert len(data['notes']) == 0
    
def test_delete_note_by_invalid_id(client, sample_paper, sample_note):
    '''
    Test deleting a note by invalid id
    API: DELETE /notes/{note_id}
    '''
    response = client.delete(f"/notes/0/")
    
    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Note not found"}

def test_delete_paper_cascade(client, sample_paper, sample_note):
    '''
    Test deleting a paper should also delete the notes under it
    API: DELETE /papers/{paper_id}
    '''
    _ = client.delete("/papers/1/")
    response = client.get("/notes/1/")

    assert response.status_code == 404  # not found
    assert response.json() == {"detail": "Note not found"}