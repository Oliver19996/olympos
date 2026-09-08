import uuid
from dataclasses import dataclass
from .config import PORTRAIT_API_KEY, PORTRAIT_API_URL, PORTRAIT_PROVIDER

@dataclass
class PortraitOutput:
    provider: str
    asset_ref: str
    status: str

class PortraitProvider:
    async def generate(self, source_reference: str, attempt: int) -> PortraitOutput:
        raise NotImplementedError
    async def delete_source(self, source_reference: str) -> None:
        raise NotImplementedError

class MockPortraitProvider(PortraitProvider):
    async def generate(self, source_reference: str, attempt: int) -> PortraitOutput:
        # 実画像は送信・保存せず、UI検証用の参照だけ返す。
        return PortraitOutput('mock', f'mock://realistic-portrait/{attempt}/{uuid.uuid4()}', 'ready')
    async def delete_source(self, source_reference: str) -> None:
        return None

class HttpPortraitProvider(PortraitProvider):
    """本番候補APIへの接続口。保存・学習禁止契約の確認後だけ有効化する。"""
    def __init__(self):
        if not PORTRAIT_API_URL or not PORTRAIT_API_KEY:
            raise RuntimeError('PORTRAIT_API_URL と PORTRAIT_API_KEY を backend/.env に設定してください')
        self.url=PORTRAIT_API_URL
        self.key=PORTRAIT_API_KEY
    async def generate(self, source_reference: str, attempt: int) -> PortraitOutput:
        import httpx
        payload={'source_reference':source_reference,'style':'realistic_illustration','attempt':attempt,'retention':'none','training':False}
        async with httpx.AsyncClient(timeout=30) as client:
            r=await client.post(f'{self.url}/portraits',json=payload,headers={'Authorization':f'Bearer {self.key}'})
            r.raise_for_status(); data=r.json()
        return PortraitOutput('http', data['asset_ref'], data.get('status','ready'))
    async def delete_source(self, source_reference: str) -> None:
        import httpx
        async with httpx.AsyncClient(timeout=20) as client:
            r=await client.delete(f'{self.url}/sources/{source_reference}',headers={'Authorization':f'Bearer {self.key}'})
            r.raise_for_status()

def provider():
    return HttpPortraitProvider() if PORTRAIT_PROVIDER=='http' else MockPortraitProvider()
