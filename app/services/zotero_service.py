import httpx
import json
import os
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from app.models.paper import PaperCreate

class ZoteroClient:
    """
    ZoteroClient handles the API request to Zotero
    """
    def __init__(self, user_id: str = None, api_key: str = None):   # type: ignore
        if not user_id or not api_key:
            load_dotenv()
            
        self.user_id = user_id or os.getenv("ZOTERO_USER_ID")
        self.api_key = api_key or os.getenv("ZOTERO_API_KEY")
        
        # base_url and headers
        self.base_url = f"https://api.zotero.org/users/{self.user_id}/items"
        self.headers = {"Zotero-API-Key": self.api_key}

    async def fetch_papers(self) -> httpx.Response:
        """
        Fetch papers by requesting to Zotero
        Return the http response directly
        """
        params = {
            "format": "json",
            "itemType": "-attachment || annotation"
        } 
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, headers=self.headers, params=params) # type: ignore
        return response
    
    def transform_format(self, response: httpx.Response) -> List[PaperCreate]:
        papers = response.json()

        create_list = []

        for paper in papers:
            meta = paper["meta"]
            data = paper["data"]
            _, paper_url = self.extract_pdf_info(paper)

            # A dto for this paper
            dto = PaperCreate(
                title = data.get("title"),
                authors = meta.get("creatorSummary"),
                abstract = data.get("abstractNote"),
                year = datetime.strptime(meta.get("parsedDate"), "%Y-%m-%d").year,
                venue = self.extract_venue(data),
                pdf_path = paper_url or ""
            )

            create_list.append(dto)
        
        return create_list


    def extract_venue(self, data: dict) -> str:
        """
        Extract Zotero paper's venue
        Priority: publicationTitle -> conferenceName -> proceedingsTitle -> repository -> default
        """
        venue = (
            data.get("publicationTitle") or   
            data.get("conferenceName") or     
            data.get("proceedingsTitle") or    
            data.get("repository") or          
            "Unknown Venue"                   
        )
        return venue

    def extract_pdf_info(self, item: dict) -> tuple[str | None, str | None]:
        """
        Extract paper key and real download url from Zotero item
        """
        # Fetch attachment
        attachment_info = item.get("links", {}).get("attachment", {})
        
        # Make sure it's application/pdf
        if attachment_info.get("attachmentType") == "application/pdf":
            pdf_href = attachment_info.get("href", "")
            
            if pdf_href:
                # paper key
                pdf_key = pdf_href.split("/")[-1]
                
                # url
                download_url = f"{pdf_href}/file"
                
                return pdf_key, download_url

        # default if no pdf attached
        return None, None
    
    def download_pdf(self, download_url: str, save_path: str) -> bool:
        """
        Download the real binary PDF stream from Zotero and save it locally.
        Return True if successful, False otherwise.
        """
        try:
            # 發送請求（記得一樣帶上認證 Header）
            response = httpx.get(download_url, headers=self.headers)    # type: ignore
            
            if response.status_code == 200:
                # 確保父目錄存在 (例如 storage/pdfs/)
                from pathlib import Path
                Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                
                # 以二進位寫入模式 ("wb") 存入指定路徑
                with open(save_path, "wb") as f:
                    f.write(response.content)
                return True
                
            return False
        except httpx.RequestError:
            return False