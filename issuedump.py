import time
import sys

from jiraauth import jclient as jira

issues = sys.argv[1:]

def dump_issue(issue):
  print "Key: " + issue.key
  print "Summary: " + issue.fields.summary
  print "Description: " + (issue.fields.description or "")
  print "Status: " + issue.fields.status.name
  print "Type: " + issue.fields.issuetype.name
  print "Reporter: " + issue.fields.reporter.name
  print "Assignee: " + getattr(issue.fields.assignee, "name", "")
  print "Components: " + ",".join([ x.name for x in issue.fields.components ])
  if (issue.fields.issuetype.name == "Sub-task"):
    print "Parent: " + issue.fields.parent.key
  for link in issue.fields.issuelinks:
    if hasattr(link, 'outwardIssue'):
      print "Link: " + issue.key + " " + link.type.outward + " " + link.outwardIssue.key
    else:
      print "Link: " + issue.key + " " + link.type.inward + " " + link.inwardIssue.key
  comments = jira.comments(issue.key)
  for comment in comments:
    print "Comment by %s: %s" % (comment.author.name, comment.body)
   
for x in issues:
  dump_issue(jira.issue(x))
  print "---------------------------"
