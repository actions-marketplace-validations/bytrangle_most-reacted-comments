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

def getOriginalIssueBody():
  issueResp = requests.get(ISSUE_API)
  issueJson = issueResp.json()
  issueBody = issueJson['body']
  return issueBody

def constructNewIssueContent(original, commentList):
  newContent = '\r\n<details><summary><strong>Potentially helpful comments</strong></summary>'
  for x in commentList:
    newContent += f'\r\n<p><a href="{x["url"]}" rel="nofollow">{x["body"]}</p>'
  newContent += '\r\n</details>'
  updatedContent = original + newContent
  return updatedContent

# def updateIssue(content):
#   head = dict(authorization='Bearer ' + token, accept='application/vnd.github.v3+json')
#   payload = {"body": content}
#   updateIssueReq = requests.patch(ISSUE_API, json.dumps(payload), headers=head)
#   print(updateIssueReq.json())

# This function checks if the total comments in the given issue
# is equal or greater than the input paremeter min_total_comments
# returns TRUE or FALSE accordingly
def issueMeetsRequirement():
  print('Updating issue')
  MIN_TOTAL_COMMENTS = int(getenv('INPUT_MIN_TOTAL_COMMENTS', 10))
#   # Input parameter passed to jobs.<job_id>.steps[*].with are available
#   # as environment variables with prefix INPUT
  ISSUE_COMMENT_API = ISSUE_API + '/comments'
  commentResp = requests.get(ISSUE_COMMENT_API)
  commentJson = commentResp.json()
#   updatedIssueContent = ''
  if (len(commentJson) >= MIN_TOTAL_COMMENTS):
    return commentJson
  return None
#     mostReactedComment = getMostReactedComments(commentJson, MAX_REACTED_COMMENTS)
#     # print(mostReactedComment)
#     originalIssueContent = getOriginalIssueBody()
#     updatedIssueContent = constructNewIssueContent(original=originalIssueContent, commentList=mostReactedComment)
#   print(updatedIssueContent)
#   return updatedIssueContent

token = getenv('INPUT_REPO_TOKEN')
if token is not None:
  MAX_REACTED_COMMENTS = int(getenv('INPUT_MAX_REACTED_COMMENT_COUNT', 5))
  filePath = getenv('GITHUB_EVENT_PATH', '/github/workflows/event.json')
  with open(filePath) as f:
    data = json.load(f)
  issueUrl = data["issue"]["html_url"]
#   issueUrl = environ['ISSUE_URL']
  ISSUE_API = re.sub("github.com", "api.github.com/repos", issueUrl)
  comments = issueMeetsRequirement()
  if comments is not None:
    reactedCommentList = getMostReactedComments(comments, MAX_REACTED_COMMENTS)
    print(reactedCommentList)
    if (len(reactedCommentList) > 0):
      originalIssueBody = getOriginalIssueBody()
      print(originalIssueBody)
      newIssueContent = originalIssueBody + constructNewIssueContent(originalIssueBody, reactedCommentList)
      print(newIssueContent)

#   newIssueContent = processCommentsAndIssue()
#   print(newIssueContent)
#   if (len(newIssueContent) > 0):
#     updateIssue(newIssueContent)
# else:
#   print('No Github token is found')