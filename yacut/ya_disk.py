import urllib
import urllib.parse
from http import HTTPStatus

import aiohttp

from . import app
from .constants import DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL, Messages
from .exceptions import DiskUploadError

AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}


async def upload_to_disk(file, session):
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params=dict(
            path=f'app:/{file.filename}',
            overwrite='True'
        )
    ) as resp:
        if resp.status != HTTPStatus.OK:
            raise DiskUploadError(
                Messages.UPLOAD_URL_ERROR.format(
                    resp.status
                ),
                status_code=resp.status,
                url=resp.url
            )
        upload_data = await resp.json()
    async with session.put(
        upload_data['href'],
        data=file.read()
    ) as upload_resp:
        if resp.status != HTTPStatus.OK:
            raise DiskUploadError(
                Messages.UPLOAD_ERROR.format(
                    str(upload_resp.url), upload_resp.status
                ),
                status_code=upload_resp.status,
                url=upload_resp.url
            )
        location = upload_resp.headers['Location']
    location = urllib.parse.unquote(location)
    location = location.replace('/disk', '')
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': location}
    ) as download_resp:
        if download_resp.status != HTTPStatus.OK:
            raise DiskUploadError(
                Messages.DOWNLOAD_URL_ERROR.format(download_resp.status),
                status_code=download_resp.status,
                url=str(download_resp.url)
            )
        download_data = await download_resp.json()
    download_url = download_data['href']
    return download_url


async def upload_files_to_disk(files):
    async with aiohttp.ClientSession() as session:
        return {
            (file.filename, await upload_to_disk(file, session))
            for file in files
        }
