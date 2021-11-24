import os

#minIssueComment = os.environ['INPUT_MIN_ISSUE_COMMENT'] or 20
# Input parameter passed to jobs.<job_id>.steps[*].width are available
# as environment variable

min = os.getenv('INPUT_MIN_ISSUE_COMMENT', 20)
print(min)