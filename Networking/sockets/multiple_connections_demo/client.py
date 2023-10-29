import time
import requests as r

with r.Session() as sess:
    while True:
        response = sess.get('http://leon-tux:8000')
        print(time.time(), response.status_code, response.text)
        time.sleep(2)
