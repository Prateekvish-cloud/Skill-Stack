import urllib.request
import json

def fetch_lc_contest_history(username="Prateek_vish"):
    url = 'https://leetcode.com/graphql'
    query = '''
    query userContestRankingInfo($username: String!) {
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
      }
      userContestRankingHistory(username: $username) {
        attended
        trendDirection
        problemsSolved
        totalProblems
        finishTimeInSeconds
        rating
        ranking
        contest {
          title
          startTime
        }
      }
    }
    '''
    payload = json.dumps({'query': query, 'variables': {'username': username}}).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('data', {})
    except Exception as e:
        print("Error fetching LC contest history:", e)
        return {}

if __name__ == '__main__':
    data = fetch_lc_contest_history("Prateek_vish")
    print("Contest Ranking Info:", json.dumps(data.get("userContestRanking"), indent=2))
    history = data.get("userContestRankingHistory", [])
    attended = [h for h in history if h.get("attended")]
    print(f"Attended contests count: {len(attended)}")
    for a in attended[:10]:
        print(" ", a["contest"]["title"], "-> Rating:", a["rating"], "Rank:", a["ranking"])
