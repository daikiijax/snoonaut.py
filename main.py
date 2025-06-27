import requests
import random


USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
]

def random_ua():
    return random.choice(USER_AGENTS)

def generate_proof_url():
    usernames = ['altcoinbear1', 'cryptofan', 'snootlover', 'airdropking', 'blockchainbro']
    status_id = random.randint(10**18, 10**19 - 1)
    return f"https://x.com/{random.choice(usernames)}/status/{status_id}"

def create_session(cookie):
    session = requests.Session()
    session.headers.update({
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'max-age=120',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'referer': 'https://earn.snoonaut.xyz/home',
        'cookie': cookie,
        'user-agent': random_ua(),
    })
    return session

def fetch_user_info(session):
    try:
        r = session.get('https://earn.snoonaut.xyz/api/user/stats', timeout=10)
        data = r.json()
        user = data.get('user', {})
        print(f"Username: {user.get('username')}, Snoot Balance: {user.get('snootBalance')}")
        return True
    except:
        print("Gagal ambil data user")
        return False

def fetch_tasks(session, tipe):
    try:
        r = session.get(f'https://earn.snoonaut.xyz/api/tasks?type={tipe}', timeout=10)
        return r.json().get('tasks', [])
    except:
        print(f"Gagal ambil task tipe {tipe}")
        return []

def complete_task(session, task):
    payload = {
        'taskId': task['id'],
        'action': 'complete',
    }

    if task['title'] in ['Spread the Snoot!', 'Like, Retweet and Comment']:
        payload['proofUrl'] = generate_proof_url()

    try:
        r = session.post('https://earn.snoonaut.xyz/api/tasks/complete', json=payload, timeout=10)
        data = r.json()
        if data.get('success'):
            print(f"Sukses: {task['title']} - Reward: {data.get('reward')}")
        else:
            print(f"Gagal selesaikan task: {task['title']}")
    except:
        print(f"Error saat kirim task: {task['title']}")

def run(cookie):
    print(f"\n== Proses akun dengan cookie: {cookie[:40]}...")
    s = create_session(cookie)

    if not fetch_user_info(s):
        return

    tugas1 = fetch_tasks(s, 'engagement')
    tugas2 = fetch_tasks(s, 'referral')
    semua = tugas1 + tugas2

    pending = [t for t in semua if t.get('status') == 'pending']
    for t in pending:
        complete_task(s, t)

    print("Semua task selesai!\n")

# ======= MASUKKAN COOKIENYA DI SINI =======
cookies = [
    "sessionid=xxx; other=xxx",
    # Tambahkan lebih banyak cookie kalau mau
]

for c in cookies:
    run(c)
