from os import environ, getenv
import re
import requests

API_URL = getenv('GITHUB_API_URL', 'https://api.github.com')
# print(API_URL)
minIssueComment = int(getenv('INPUT_MIN_ISSUE_COMMENT', 10))
print(minIssueComment)
MAX_REACTED_COMMENTS = int(getenv('INPUT_MAXIMUM_REACTED_COMMENTS', 5))
# Input parameter passed to jobs.<job_id>.steps[*].width are available
# as environment variable

#print(environ)

REPO = environ['GITHUB_REPOSITORY']
issueUrl = environ['ISSUE_URL']
ISSUE_API = re.sub("github.com", "api.github.com/repos", issueUrl)
print(ISSUE_API)
# print(issueUrl)
ISSUE_ID = re.search("issues\/(.+)", issueUrl).group(1)
# print(ISSUE_ID)
# print(type(ISSUE_ID))
commentApiUrl = API_URL + "/repos/" + REPO + "/issues/" + ISSUE_ID + "/comments"
print(commentApiUrl)

response = requests.get(commentApiUrl)
json = response.json()
issueResp = requests.get(ISSUE_API)
print(issueResp.json()['comments'])
if (len(json) > minIssueComment):
  print('Fetching most reacted comments')
  commentList = []
  for comment in json:
    reactionCount = comment["reactions"]["total_count"]
    if (reactionCount > 0):
      extract = comment["body"][:50] + "..."
      reactedComment = { "url": comment["html_url"], "body": extract, "reactionCount": reactionCount}
      commentList.append(reactedComment)
  commentList = sorted(commentList, key = lambda i: i["reactionCount"], reverse=True)
  if (len(commentList) > MAX_REACTED_COMMENTS):
    commentList = commentList[:MAX_REACTED_COMMENTS]
  
  issueBody = issueResp.json()['body']
  print(issueBody)
  newIssueBody = issueBody + '\r\n## Potentially helpful comments'
  # print(commentList)
else:
  print('exit')