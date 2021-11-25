from os import environ, getenv
import re
import requests

minIssueComment = int(getenv('INPUT_MIN_ISSUE_COMMENT', 10))
print(minIssueComment)
API_URL = getenv('GITHUB_API_URL', 'https://api.github.com')
# print(API_URL)
# Input parameter passed to jobs.<job_id>.steps[*].width are available
# as environment variable

#print(environ)

REPO = environ['GITHUB_REPOSITORY']
issueUrl = environ['ISSUE_URL']
# print(issueUrl)
ISSUE_ID = re.search("issues\/(.+)", issueUrl).group(1)
# print(ISSUE_ID)
# print(type(ISSUE_ID))
commentApiUrl = API_URL + "/repos/" + REPO + "/issues/" + ISSUE_ID + "/comments"
print(commentApiUrl)

response = requests.get(commentApiUrl)
json = response.json()
print(json)
if (len(json) > minIssueComment):
  print('Fetching most reacted comments')
else:
  print('exit')