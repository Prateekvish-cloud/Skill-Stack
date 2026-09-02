import urllib.request
import json

def fetch_lc_matched_user(username):
    url = 'https://leetcode.com/graphql'
    query = '''
    query userProblemsSolved($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
      recentAcSubmissionList(username: $username, limit: 50) {
        title
        titleSlug
        timestamp
      }
    }
    '''
    payload = json.dumps({'query': query, 'variables': {'username': username}}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('data', {})
    except Exception as e:
        print(f"LC Error: {e}")
        return {}

if __name__ == '__main__':
    data = fetch_lc_matched_user("Prateek_vish")
    print(json.dumps(data, indent=2))
