import requests

from homework07.vkapi.config import VK_CONFIG

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
user_id = 250240920
fields = 'sex'

query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
response = requests.get(query).json()
for i in response['response']['items']:
    print(i)
print(response)