import urllib
import urllib.parse
from typing import Optional

import aiohttp

from . import app

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'

AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}

payload = {
    'path': 'app:/filename.txt',
    'overwrite': 'True'
}


async def upload_to_disk(file) -> Optional[str]:

    async with aiohttp.ClientSession() as session:
        payload = {
            'path': f'app:/{file.filename}',
            'overwrite': 'True'
        }

        try:

            async with session.get(
                REQUEST_UPLOAD_URL,
                headers=AUTH_HEADERS,
                params=payload
            ) as resp:

                if resp.status != 200:
                    return None

                upload_data = await resp.json()
                upload_url = upload_data['href']
                async with session.put(
                    upload_url,
                    data=file.read()
                ) as upload_resp:

                    if upload_resp.status == 201:
                        location = upload_resp.headers['Location']
                        location = urllib.parse.unquote(location)
                        location = location.replace('/disk', '')
                    else:
                        return None
                    download_payload = {
                        'path': location,
                    }

                    async with session.get(
                        DOWNLOAD_LINK_URL,
                        headers=AUTH_HEADERS,
                        params=download_payload
                    ) as download_resp:
                        if download_resp.status != 200:
                            return None

                        download_data = await download_resp.json()
                        download_url = download_data['href']
                        return download_url
        except Exception as e:
            print(e)
            return None
