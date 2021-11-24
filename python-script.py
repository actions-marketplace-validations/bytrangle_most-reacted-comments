import os

minIssueComment = os.getenv('INPUT_MIN_ISSUE_COMMENT', 20)
# Input parameter passed to jobs.<job_id>.steps[*].width are available
# as environment variable

print(minIssueComment)