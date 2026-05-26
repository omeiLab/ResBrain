import os
import re
import pytest
import httpx
from unittest.mock import patch
from app.models.paper import PaperCreate
# Assuming your service is placed in app/services/zotero_service.py
from app.services.zotero_service import ZoteroClient

@pytest.fixture
def mock_zotero_credentials():
    """Fixture to provide dummy credentials for ZoteroClient."""
    return {
        "user_id": "12345678",
        "api_key": "mock_api_key_xyz"
    }

@pytest.fixture
def sample_zotero_response_json():
    """
    Fixture providing the actual sample JSON layout retrieved from Zotero API.
    This simulates a valid 'preprint' item payload like Toolformer.
    """
    return [
      {
        "key": "6ZQ26P5K",
        "version": 1031,
        "library": {
          "type": "user",
          "id": 18914350,
          "name": "omei_ogami"
        },
        "links": {
          "attachment": {
            "href": "https://api.zotero.org/users/18914350/items/FAM56MT3",
            "type": "application/json",
            "attachmentType": "application/pdf",
            "attachmentSize": 657966
          }
        },
        "meta": {
          "creatorSummary": "Schick et al.",
          "parsedDate": "2023-02-09",
          "numChildren": 2
        },
        "data": {
          "key": "6ZQ26P5K",
          "version": 1031,
          "itemType": "preprint",
          "title": "Toolformer: Language Models Can Teach Themselves to Use Tools",
          "creators": [
            {"creatorType": "author", "firstName": "Timo", "lastName": "Schick"}
          ],
          "abstractNote": "Language models (LMs) exhibit remarkable abilities...",
          "repository": "arXiv",
          "date": "2023-02-09",
          "url": "http://arxiv.org/abs/2302.04761"
        }
      }
    ]

def test_client_initialization_with_args(mock_zotero_credentials):
    """Test if the client correctly initializes when credentials are passed directly."""
    client = ZoteroClient(
        user_id=mock_zotero_credentials["user_id"], 
        api_key=mock_zotero_credentials["api_key"]
    )
    assert client.user_id == mock_zotero_credentials["user_id"]
    assert client.api_key == mock_zotero_credentials["api_key"]
    assert client.headers["Zotero-API-Key"] == mock_zotero_credentials["api_key"]
    assert mock_zotero_credentials["user_id"] in client.base_url

@patch("app.services.zotero_service.os.getenv")
@patch("app.services.zotero_service.load_dotenv")
def test_client_initialization_from_env(mock_load_dotenv, mock_getenv):
    """Test if the client falls back to environment variables when no args are provided."""
    mock_getenv.side_effect = lambda key: "env_user_id" if key == "ZOTERO_USER_ID" else "env_api_key"
    
    client = ZoteroClient()
    
    mock_load_dotenv.assert_called_once()
    assert client.user_id == "env_user_id"
    assert client.api_key == "env_api_key"

@pytest.mark.asyncio
async def test_fetch_papers_success(mock_zotero_credentials, sample_zotero_response_json, httpx_mock):
    """
    Test fetch_papers sends a valid GET request to Zotero API with required headers.
    Uses pytest-httpx to mock the network layer.
    """
    client = ZoteroClient(
        user_id=mock_zotero_credentials["user_id"], 
        api_key=mock_zotero_credentials["api_key"]
    )
    
    # Mocking the endpoint target
    httpx_mock.add_response(
        method="GET",
        url=re.compile(rf"^{client.base_url}.*"),
        status_code=200,
        json=sample_zotero_response_json
    )
    
    response = await client.fetch_papers()
    
    assert response.status_code == 200
    assert response.json() == sample_zotero_response_json

def test_extract_venue_fallbacks(mock_zotero_credentials):
    """Test the priority logic inside extract_venue method."""
    client = ZoteroClient(user_id="1", api_key="1")
    
    # Priority 1: publicationTitle
    data_journal = {"publicationTitle": "Journal of NLP", "repository": "arXiv"}
    assert client.extract_venue(data_journal) == "Journal of NLP"
    
    # Priority 2: conferenceName
    data_conf = {"conferenceName": "ACL 2026", "repository": "arXiv"}
    assert client.extract_venue(data_conf) == "ACL 2026"
    
    # Priority 4: repository
    data_preprint = {"repository": "arXiv"}
    assert client.extract_venue(data_preprint) == "arXiv"
    
    # Priority 5: default保底
    assert client.extract_venue({}) == "Unknown Venue"

def test_extract_pdf_info_valid(mock_zotero_credentials, sample_zotero_response_json):
    """Test parsing an item containing a valid PDF attachment link."""
    client = ZoteroClient(user_id="1", api_key="1")
    item = sample_zotero_response_json[0]
    
    pdf_key, download_url = client.extract_pdf_info(item)
    
    assert pdf_key == "FAM56MT3"
    assert download_url == "https://api.zotero.org/users/18914350/items/FAM56MT3/file"

def test_extract_pdf_info_missing_or_invalid(mock_zotero_credentials):
    """Test extract_pdf_info returns (None, None) gracefully if attachment types don't match."""
    client = ZoteroClient(user_id="1", api_key="1")
    
    # Scenario A: Non-pdf attachment
    item_txt = {"links": {"attachment": {"href": "...", "attachmentType": "text/plain"}}}
    assert client.extract_pdf_info(item_txt) == (None, None)
    
    # Scenario B: Missing links key completely
    assert client.extract_pdf_info({}) == (None, None)

def test_transform_format_creates_valid_paper_dto(mock_zotero_credentials, sample_zotero_response_json):
    """
    Test mapping logic converts raw Zotero items into a List of PaperCreate schemas.
    Validates field correctness based on target specifications.
    """
    client = ZoteroClient(user_id="1", api_key="1")
    
    # Mocking a mock response object
    mock_response = httpx.Response(status_code=200, json=sample_zotero_response_json)
    
    result = client.transform_format(mock_response)
    
    assert len(result) == 1
    dto = result[0]
    
    assert isinstance(dto, PaperCreate)
    assert dto.title == "Toolformer: Language Models Can Teach Themselves to Use Tools"
    assert dto.authors == "Schick et al."
    assert dto.year == 2023
    assert dto.venue == "arXiv"
    assert dto.pdf_path == "https://api.zotero.org/users/18914350/items/FAM56MT3/file"

@pytest.mark.asyncio
async def test_fetch_papers_error_handling_placeholder(mock_zotero_credentials, httpx_mock):
    """
    A placeholder test demonstrating future unexpected status code verifications.
    ZoteroClient currently directly passes the response object, so we verify status tracking.
    """
    client = ZoteroClient(user_id="1", api_key="1")
    httpx_mock.add_response(
        method="GET", 
        url=re.compile(rf"^{client.base_url}.*"), 
        status_code=401
    )
    
    response = await client.fetch_papers()
    assert response.status_code == 401

def test_download_pdf_success(mock_zotero_credentials, httpx_mock, tmp_path):
    """
    Test if download_pdf successfully retrieves binary content 
    and writes it to the designated local file path.
    """
    client = ZoteroClient(
        user_id=mock_zotero_credentials["user_id"], 
        api_key=mock_zotero_credentials["api_key"]
    )
    
    # 模擬要下載的目標金鑰與測試寫入路徑
    target_pdf_key = "FAM56MT3"
    dummy_save_path = tmp_path / "storage" / "pdfs" / f"1_{target_pdf_key}.pdf"
    
    # 構造 Zotero 真實檔案下載網址
    expected_download_url = f"https://api.zotero.org/users/{client.user_id}/items/{target_pdf_key}/file"
    fake_pdf_content = b"%PDF-1.5 test binary stream data"
    
    # 註冊 Mock 檔案流回應
    httpx_mock.add_response(
        method="GET",
        url=expected_download_url,
        status_code=200,
        content=fake_pdf_content  # 模擬真實二進位 bytes
    )
    
    # 執行下載
    success = client.download_pdf(download_url=expected_download_url, save_path=str(dummy_save_path))
    
    # 驗證 A: 函數必須回傳 True
    assert success is True
    # 驗證 B: 實體檔案必須真的被建立在硬碟上
    assert dummy_save_path.exists()
    # 驗證 C: 寫入的內文必須與 API 吐回的完全一致
    assert dummy_save_path.read_bytes() == fake_pdf_content

def test_download_pdf_not_found(mock_zotero_credentials, httpx_mock, tmp_path):
    """
    Test if download_pdf returns False gracefully when Zotero API 
    returns a non-200 status code (e.g., file missing or permission denied).
    """
    client = ZoteroClient(user_id="1", api_key="1")
    target_pdf_key = "MISSING_KEY"
    dummy_save_path = tmp_path / "failed_download.pdf"
    
    expected_download_url = f"https://api.zotero.org/users/1/items/{target_pdf_key}/file"
    
    # 模擬檔案遺失 (404)
    httpx_mock.add_response(
        method="GET",
        url=expected_download_url,
        status_code=404
    )
    
    success = client.download_pdf(download_url=expected_download_url, save_path=str(dummy_save_path))
    
    # 驗證: 函數回傳 False，且不應該有任何垃圾檔案被建立出來
    assert success is False
    assert not dummy_save_path.exists()