import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://www.geeksforgeeks.org',
    'Referer': 'https://www.geeksforgeeks.org/'
}

def test_gfg_post(handle="vishpratdzsq"):
    endpoints = [
        "https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/",
        "https://practiceapi.geeksforgeeks.org/api/vr/problems/user/solved/",
        "https://practiceapi.geeksforgeeks.org/api/v1/user/profile/"
    ]
    for ep in endpoints:
        print(f"\nPOST testing: {ep}")
        try:
            payload = json.dumps({"handle": handle, "user_handle": handle, "username": handle}).encode('utf-8')
            req = urllib.request.Request(ep, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=5) as resp:
                print("Status:", resp.status)
                body = resp.read().decode('utf-8')
                print("Length:", len(body))
                print("Sample:", body[:300])
        except Exception as e:
            print("Error:", e)

def test_gfg_get_with_params(handle="vishpratdzsq"):
    endpoints = [
        f"https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/?handle={handle}",
        f"https://practiceapi.geeksforgeeks.org/api/v1/user/profile/{handle}/",
        f"https://practiceapi.geeksforgeeks.org/api/vr/user/profile/{handle}/"
    ]
    for ep in endpoints:
        print(f"\nGET testing: {ep}")
        try:
            req = urllib.request.Request(ep, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                print("Status:", resp.status)
                body = resp.read().decode('utf-8')
                print("Length:", len(body))
                print("Sample:", body[:300])
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    test_gfg_post("vishpratdzsq")
    test_gfg_get_with_params("vishpratdzsq")
