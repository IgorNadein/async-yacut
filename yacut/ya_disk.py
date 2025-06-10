import urllib
import urllib.parse
from http import HTTPStatus

import aiohttp

from . import app
from .constants import DOWNLOAD_LINK_URL, MESSAGES, REQUEST_UPLOAD_URL
from .exceptions import DiskUploadError

AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}


async def upload_to_disk(file):

    async with aiohttp.ClientSession() as session:
        payload = dict(
            path=f'app:/{file.filename}',
            overwrite='True'
        )
        async with session.get(
            REQUEST_UPLOAD_URL,
            headers=AUTH_HEADERS,
            params=payload
        ) as resp:

            if resp.status != HTTPStatus.OK:
                raise DiskUploadError(
                    MESSAGES['upload_url_error'].format(
                        resp.status
                    ),
                    status_code=resp.status,
                    url=str(resp.url)
                )

            upload_data = await resp.json()
            upload_url = upload_data['href']

            async with session.put(
                upload_url,
                data=file.read()
            ) as upload_resp:

                if resp.status != HTTPStatus.OK:
                    raise DiskUploadError(
                        MESSAGES['upload_error'].format(
                            str(upload_resp.url), upload_resp.status
                        ),
                        status_code=upload_resp.status,
                        url=str(upload_resp.url)
                    )
                location = upload_resp.headers['Location']
                location = urllib.parse.unquote(location)
                location = location.replace('/disk', '')
                download_payload = {
                    'path': location,
                }

                async with session.get(
                    DOWNLOAD_LINK_URL,
                    headers=AUTH_HEADERS,
                    params=download_payload
                ) as d_resp:
                    if d_resp.status != HTTPStatus.OK:
                        raise DiskUploadError(
                            MESSAGES[
                                'download_url_error'
                            ].format(d_resp.status),
                            status_code=d_resp.status,
                            url=str(d_resp.url)
                        )

                    download_data = await d_resp.json()
                    download_url = download_data['href']
                    return download_url


async def upload_files_to_disk(files):
    download_urls = []
    for file in files:
        download_url = await upload_to_disk(file)
        download_urls.append((file.filename, download_url))
    return download_urls
