import requests, json, msgpack, os
from tqdm import tqdm

def list_get():
    response = requests.get("https://api.matsurihi.me/mltd/v1/version/latest").content.decode("utf-8")
    l_version = json.loads(response)
    list = []
    version = l_version['res']['version']
    indexName = l_version['res']['indexName']
    list.append(version)
    list.append(indexName)
    return list
    
def filename_get(list):
    response = requests.get(f"https://td-assets.bn765.com/{list[0]}/production/2018/Android/{list[1]}").content
    a = msgpack.unpackb(response)
    progress = tqdm(total=len(a[0]),colour='green')
    for key,value in a[0].items():
        get_files = requests.get(f"https://td-assets.bn765.com/{list[0]}/production/2018/Android/{value[1]}")
        folder_path = f'./files/'
        file_name = folder_path + value[1]
        os.makedirs(folder_path, exist_ok=True)
        with open(file_name, 'wb') as f:
            f.write(get_files.content)
        progress.set_description(f"Download {key}")
        progress.update(1)
            