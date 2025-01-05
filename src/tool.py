import aiohttp
import asyncio
import json
import msgpack
import os
import requests

from tqdm import tqdm
from typing import Dict


class AssetDownload(object):
    def __init__(self):
        self.folder_path = "./files/"
        self.max_connections = 50
        self.progress = None

    async def main(self):
        mltd_information = self.information_get()
        data_amount, filename_list = self.filename_get(mltd_information)

        self.progress = tqdm(total=data_amount, colour='green')

        os.makedirs(self.folder_path, exist_ok=True)

        connector = aiohttp.TCPConnector(
            limit=self.max_connections)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.download_data(session, url) for url in filename_list]
            _ = await asyncio.gather(*tasks)

    def information_get(self) -> Dict[str, str]:
        response = requests.get(
            "https://api.matsurihi.me/api/mltd/v2/version/latest").content.decode("utf-8")
        data = json.loads(response)
        mltd_information = {
            "version": data['asset']['version'],
            "indexName": data['asset']['indexName']
        }
        print("get information complete")
        return mltd_information

    def filename_get(self, mltd_information):
        response = requests.get(
            f"https://td-assets.bn765.com/{mltd_information['version']}/production/2018/Android/{mltd_information['indexName']}").content
        res_unpack = msgpack.unpackb(response)
        print("get file data complete")
        return len(res_unpack[0]), [f"https://td-assets.bn765.com/{mltd_information['version']}/production/2018/Android/{value[1]}" for _, value in res_unpack[0].items()]

    async def download_data(self, session: aiohttp.ClientSession, url: str):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    file_name = self.folder_path + url.split("/")[-1]
                    os.makedirs(self.folder_path, exist_ok=True)
                    with open(file_name, 'wb') as f:
                        f.write(data)
                    self.progress.set_description(
                        f"Download {url.split('/')[-1]}")
                    self.progress.update(1)
                else:
                    print(f"download {url.split('/')[-1]} failed")
        except Exception as e:
            print(f"download {url.split('/')[-1]} has occurred an error: {e}")
