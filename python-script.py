from os import environ, getenv
# import requests

minIssueComment = getenv('INPUT_MIN_ISSUE_COMMENT', 20)
print(minIssueComment)
API_URL = getenv('GITHUB_API_URL', 'https://api.github.com')
print(API_URL)
# Input parameter passed to jobs.<job_id>.steps[*].width are available
# as environment variable

#ISSUE_URL = env['ISSUE_URL']
print(environ)