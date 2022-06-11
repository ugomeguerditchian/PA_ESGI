import requests
session = requests.session()
session.proxies = {}

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

r = session.get("http://httpbin.org/ip")
print(r.text)

r = session.get('http://7znv2tbld7nb2xsljnb4h25fcakyezwlknsn3frwrhewcdrncvrbrxyd.onion/')
print(r.headers)
print(r.text)

#post to http://7znv2tbld7nb2xsljnb4h25fcakyezwlknsn3frwrhewcdrncvrbrxyd.onion/test/main2.php
#image to send : C:\Users\Wherxit\Desktop\PICS\bench_tmtc.png
#then submit
'''
Content-Disposition: form-data; name="fileToUpload"; filename="bench_tmtc.png"
Content-Type: image/png
Content-Disposition: form-data; name="submit"
'''
data= {'fileToUpload': open('C:\\Users\\Wherxit\\Desktop\\PICS\\bench_tmtc.png', 'rb'), 'submit': 'submit'}
r = session.post('http://7znv2tbld7nb2xsljnb4h25fcakyezwlknsn3frwrhewcdrncvrbrxyd.onion/test/drop2.php', files=data)
print(r.text)
#print error



