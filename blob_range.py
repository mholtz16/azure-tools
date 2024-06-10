import requests
import time
chunk_size = 2097152;

urls = ['','']

for url in urls:
    start_time = time.time()
    start=0
    headers = {'Range': f'bytes={start}-{start+chunk_size-1}','Accept-Encoding': 'gzip'}

    print(headers)
    response=requests.get(url,headers=headers)
    while (response.status_code == 206):
        start += chunk_size
        headers = {'Range': f'bytes={start}-{start+chunk_size-1}','Accept-Encoding': 'gzip'}

        response=requests.get(url,headers=headers)
        print(response.headers)
    end_time = time.time()
    print(f'duration for {url}:\n{end_time - start_time}')
