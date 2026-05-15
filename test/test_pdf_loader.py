import io

def test_upload_pdf(client, sample_paper):
    """
    Test upload pdf
    API: POST /papers/{id}/upload/
    """
    file_content = b"%PDF-1.4 test content"
    file_name = "attention.pdf"
    response = client.post(
        f"/papers/{sample_paper.id}/upload/",
        files={"file": (file_name, io.BytesIO(file_content), "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "pdfs/" in data["pdf_path"]
    assert data["pdf_path"].endswith(".pdf")

def test_upload_pdf_invalid_paper(client):
    """
    Test upload pdf for not-existed paper
    API: POST /papers/{id}/upload/
    """
    response = client.post(
        "/papers/0/upload/",
        files={"file": ("test.pdf", b"content", "application/pdf")}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Paper not found"}