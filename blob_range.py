import requests
import time
chunk_size = 2097152;

urls = ['https://cdn.screencast.tsc-dev.co/uploads/g0003020UFwgduTTBuQYt71YXlRR2/luma.mp4?sp=r&st=2024-05-21T14:08:24Z&se=2024-05-21T22:08:24Z&spr=https&sv=2022-11-02&sr=b&sig=A7skVnnhaaFlx5jir%2BIwU5QN2UOOoHvhI3OmM5%2BqNTg%3D','https://tscscreencastdeveast.blob.core.windows.net/uploads/g0003020UFwgduTTBuQYt71YXlRR2/luma.mp4?sp=r&st=2024-05-21T14:08:24Z&se=2024-05-21T22:08:24Z&spr=https&sv=2022-11-02&sr=b&sig=A7skVnnhaaFlx5jir%2BIwU5QN2UOOoHvhI3OmM5%2BqNTg%3D']

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
