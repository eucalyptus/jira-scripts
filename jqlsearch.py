#!/usr/bin/python

import sys
from jiraauth import jclient as jira

'''
Synopsis:  This script runs an arbitrary JQL search
Example: jqlsearch.py 'project="SUP" and reporter="nbeard"'
'''

issues = jira.search_issues(sys.argv[1])

for x in issues:
    print x.key + " | " + x.fields.summary 
