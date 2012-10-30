#!/usr/bin/python

from jiraauth import jclient as jira

'''
Synopsis:  This script finds all issues with a "Customer:" snippet in a comment
'''

issues = jira.search_issues('''comment ~ "Customer"''')

import re
for x in issues:
  comments = jira.comments(x.key)
  for comment in comments:
    for line in comment.body.split('\n'):
      if re.match('.*Customer:.*', line):
        print x.key + " : " + comment.author.displayName + " -- " + line
        break
