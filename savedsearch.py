#!/usr/bin/python

import sys
from jiraauth import jclient as jira

'''
Synopsis: ./savedsearch.py <filtername>
Example: ./savedsearch.py "Unowned, unconfirmed engineering issues"
Example 2: ./savedsearch.py 10506
'''

filterid = None
try:
  filterid = str(int(sys.argv[1]))
except ValueError:
  favs = jira.favourite_filters()
  tgt = [ x.id for x in favs if x.name == sys.argv[1] ]
  if len(tgt):
    filterid = tgt[0]

if filterid:
  filt = jira.filter(id=filterid)
  issues = jira.search_issues(filt.jql)
  for x in issues:
    print x.key + " | " + x.fields.summary
