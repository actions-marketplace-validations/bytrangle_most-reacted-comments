from os import environ, getenv
import re
import requests
import json

def getMostReactedComments(comments, maxComments):
  mostReactedList = []
  for comment in comments:
    reactionCount = comment["reactions"]["total_count"]
    if (reactionCount > 0):
      extract = comment["body"][:50] + "..."
      reactedComment = { "url": comment["html_url"], "body": extract, "reactionCount": reactionCount}
      mostReactedList.append(reactedComment)
  if (len(mostReactedList) > 0):
    mostReactedList = sorted(mostReactedList, key = lambda i: i["reactionCount"], reverse=True)
  if (len(mostReactedList) > maxComments):
    mostReactedList = mostReactedList[:maxComments]
  return mostReactedList

def constructNewIssueContent(comments, url):
  issueResp = requests.get(url)
  issueJson = issueResp.json()
  issueBody = issueJson['body']
  commentBody = '\r\n<details><summary><strong>Potentially helpful comments</strong></summary>'
  for x in comments:
    commentBody += f'\r\n[{x["body"]}]({x["url"]})'
  commentBody += '\r\n</details>'
  issueBody += commentBody
  return issueBody

def updateIssue(token, content):
  head = dict(authorization='Bearer ' + token, accept='application/vnd.github.v3+json')
  payload = {"body": content}
  updateIssueReq = requests.patch(ISSUE_API, json.dumps(payload), headers=head)
  print(updateIssueReq.json())

def processCommentsAndIssue():
  print('Updating issue')

# print(ISSUE_API)
# print(issueUrl)
  MIN_TOTAL_COMMENT = int(getenv('INPUT_MIN_ISSUE_COMMENT', 10))
  MAX_REACTED_COMMENTS = int(getenv('INPUT_MAXIMUM_REACTED_COMMENTS', 5))
  # Input parameter passed to jobs.<job_id>.steps[*].with are available
  # as environment variables with prefix INPUT
  REPO = environ['GITHUB_REPOSITORY']
  ISSUE_COMMENT_API = ISSUE_API + '/comments'
  commentResp = requests.get(ISSUE_COMMENT_API)
  commentJson = commentResp.json()
  updatedIssueContent = ''
  if (len(commentJson) > MIN_TOTAL_COMMENT):
    mostReactedComment = getMostReactedComments(commentJson, MAX_REACTED_COMMENTS)
    # print(mostReactedComment)
    updatedIssueContent = constructNewIssueContent(mostReactedComment, ISSUE_API)
  return updatedIssueContent
  # payload = {"body": "This is just a fake issue to test a Github action."}
  # r = requests.patch(ISSUE_API, json.dumps(payload), headers=head)
  # print(r)
  # rJson = r.json()
  # print(rJson)

#   API_URL = getenv('GITHUB_API_URL', 'https://api.github.com')
#   # print(API_URL)
#   # print(minIssueComment)

#   ISSUE_ID = re.search("issues\/(.+)", issueUrl).group(1)
# # print(ISSUE_ID)
# # print(type(ISSUE_ID))
#   commentApiUrl = API_URL + "/repos/" + REPO + "/issues/" + ISSUE_ID + "/comments"
# # print(commentApiUrl)

#     print('Fetching most reacted comments')
#       
#     # print(issueBody)
#     issueBody += commentBody
#     print(issueBody)
#   else:
#     print('exit')

token = getenv('GITHUB_TOKEN')
if token is not None:
  issueUrl = environ['ISSUE_URL']
  ISSUE_API = re.sub("github.com", "api.github.com/repos", issueUrl)
  newIssueContent = processCommentsAndIssue()
  print(newIssueContent)
  # if (len(newIssueContent) > 0):
  #   updateIssue(content=newIssueContent)
else:
  print('No Github token is found')