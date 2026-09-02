import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.geeksforgeeks.org/'
}

def test_endpoints(handle="vishpratdzsq"):
    urls = [
        f"https://www.geeksforgeeks.org/api/vr/user/{handle}",
        f"https://www.geeksforgeeks.org/api/v1/user/{handle}",
        f"https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/{handle}/",
        f"https://practiceapi.geeksforgeeks.org/api/vr/problems/user/{handle}/solved/",
        f"https://gfg-stats-api.herokuapp.com/user/{handle}",
        f"https://codechef-api.vercel.app/handle/{handle}",
        f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=20"
    ]
    
    for url in urls:
        print(f"\nTesting: {url}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                print("Status:", resp.status)
                body = resp.read().decode('utf-8')
                print("Length:", len(body))
                print("Sample:", body[:300])
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    test_endpoints("vishpratdzsq")
