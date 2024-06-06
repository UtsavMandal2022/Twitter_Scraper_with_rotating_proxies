import queue
import requests
import threading

q=queue.Queue()

valid_proxies = []

with open('free_proxy_list.txt') as f:
    for line in f:
        q.put(line.strip())

        # print(line.strip())
def check_proxy():
    global q
    c=0
    while not q.empty():
        proxy = q.get()
        # print(c,'Checking proxy:', proxy)
        c+=1
        proxies = {
            'http': proxy,
            'https': proxy
        }
        try:
            r = requests.get('https://x.com/home', proxies=proxies)
        except:
            continue
        if r.status_code == 200:
                valid_proxies.append(proxy)
                print(proxy)
                if(len(valid_proxies) >= 50):
                    return
                # print(r.json())


for _ in range(10):
    threading.Thread(target=check_proxy).start()

open('valid_proxies.txt', 'w').write('\n'.join(valid_proxies))

# proxy='36.37.86.26:9812'
# proxies = {
#     'http': proxy,
#     'https': proxy
# }
# try:
#     r = requests.get('http://ipinfo.io/json', proxies=proxies)
#     if r.status_code == 200:
#         print(r.json())
# except:
#     print('Error')
#     pass