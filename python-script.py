from os import environ, getenv
import re
import requests

def updateIssue(token):
  print('Updating issue')
  head = { "authorization": "Bearer " + token, "accept": "application/vnd.github.v3+json"}
  issueUrl = environ['ISSUE_URL']
  ISSUE_API = re.sub("github.com", "api.github.com/repos", issueUrl)
# print(ISSUE_API)
# print(issueUrl)
  payload = {"body": "## Describe the issue\r\nThis is just a fake issue to test a Github action."}
  r = requests.patch(ISSUE_API, payload, headers=head)
  json = r.json()
  print(json)

#   API_URL = getenv('GITHUB_API_URL', 'https://api.github.com')
#   # print(API_URL)
#   minIssueComment = int(getenv('INPUT_MIN_ISSUE_COMMENT', 10))
#   # print(minIssueComment)
#   MAX_REACTED_COMMENTS = int(getenv('INPUT_MAXIMUM_REACTED_COMMENTS', 5))
#   # Input parameter passed to jobs.<job_id>.steps[*].width are available
#   # as environment variable
#   REPO = environ['GITHUB_REPOSITORY']
#   ISSUE_ID = re.search("issues\/(.+)", issueUrl).group(1)
# # print(ISSUE_ID)
# # print(type(ISSUE_ID))
#   commentApiUrl = API_URL + "/repos/" + REPO + "/issues/" + ISSUE_ID + "/comments"
# # print(commentApiUrl)

#   commentResp = requests.get(commentApiUrl)
#   commentJson = commentResp.json()
#   if (len(commentJson) > minIssueComment):
#     print('Fetching most reacted comments')
#     commentList = []
#     for comment in commentJson:
#       reactionCount = comment["reactions"]["total_count"]
#       if (reactionCount > 0):
#         extract = comment["body"][:50] + "..."
#         reactedComment = { "url": comment["html_url"], "body": extract, "reactionCount": reactionCount}
#         commentList.append(reactedComment)
#     commentList = sorted(commentList, key = lambda i: i["reactionCount"], reverse=True)
#     if (len(commentList) > MAX_REACTED_COMMENTS):
#       commentList = commentList[:MAX_REACTED_COMMENTS]
#     issueResp = requests.get(ISSUE_API)
#     issueJson = issueResp.json()
#     issueBody = issueJson['body']
#     # print(issueBody)
#     commentBody = '<details><summary><strong>Potentially helpful comments</strong></summary>'
#     for x in commentList:
#       commentBody += f'\r\n[{x["body"]}]({x["url"]})'
#     commentBody += '</details>'
#     issueBody += commentBody
#     print(issueBody)
#   else:
#     print('exit')

token = getenv('GITHUB_TOKEN')
if token is not None:
  updateIssue(token)
else:
  print('No Github token is found')