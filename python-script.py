from os import environ, getenv
# import requests

minIssueComment = getenv('INPUT_MIN_ISSUE_COMMENT', 20)
print(minIssueComment)
# Input parameter passed to jobs.<job_id>.steps[*].width are available
# as environment variable

#ISSUE_URL = env['ISSUE_URL']
#API_URL = env['GITHUB_API_URL']
print(environ)