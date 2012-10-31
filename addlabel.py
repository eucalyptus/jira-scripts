#!/usr/bin/python

import time
import sys

from jiraauth import jclient as jira

'''
Synopsis: Add label(s) to issue(s)
Example: addlabel.py EUCA-1234,EUCA-2345 Support,AWS

issues = sys.argv[1].split(',')
labels = sys.argv[2].split(',')

for x in issues:
  issue = jira.issue(x)
  issue.fields.labels.extend(labels)
  issue.update(labels=issue.fields.labels)
