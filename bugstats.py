#!/usr/bin/python

import sys
from jiraauth import jclient as jira
from collections import namedtuple

'''
Synopsis:  This script runs an arbitrary JQL search
Example: jqlsearch.py 'project="SUP" and reporter="nbeard"'
'''



QueryData = namedtuple('QueryData', ['issuetype', 'status', 'reporter', 'assignee', 'SLA', 'level', 'flagged'])
querygroups = [ [ QueryData('in (Bug, Improvement)', '= "Release Pending"', None, None, None, None, None), ],
                [ QueryData('in (Bug, Improvement)', '= "Reopened"', None, None, None, None, None), ],
                [ QueryData('in (Bug, Improvement)', 'in ("Needs Clarification", "Waiting for Reporter")', None, None, None, None, None), ],
                [ QueryData('in (Bug, Improvement)', 'in ("In Progress", "In Review", "In QA")', None, 'is EMPTY', None, None, None), 
                  QueryData('in (Bug, Improvement)', 'in ("In Progress", "In Review", "In QA")', None, 'is not EMPTY', None, None, None), ],
                [ QueryData('in (Bug, Improvement)', '= Confirmed', None, 'is EMPTY', None, None, None),
                  QueryData('in (Bug, Improvement)', '= Confirmed', None, 'in membersOf("engineering")', None, None, None),
                  QueryData('in (Bug, Improvement)', '= Confirmed', None, 'not in membersOf("engineering")', None, None, None), ],
                [ QueryData('in (Bug, Improvement)', 'in (Unconfirmed, Investigating)', 'in membersOf("engineering")', 
                            'not in membersOf("engineering")', None, None, None), 
                  QueryData('in (Bug, Improvement)', 'in (Unconfirmed, Investigating)', 'in membersOf("engineering")', 
                            'is EMPTY', None, None, None), 
                  QueryData('in (Bug, Improvement)', 'in (Unconfirmed, Investigating)', 'in membersOf("engineering")', 
                            'in membersOf("engineering")', None, None, None), ],
                [ QueryData('= Improvement', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'in membersOf("engineering")', None, None, None), 
                  QueryData('= Improvement', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'not in membersOf("engineering"); is EMPTY', None, None, None), ],
                [ QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'is EMPTY', 'in ("Standard", "Premium")', None, None), 
                  QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'in membersOf("engineering")', 'in ("Standard", "Premium")', None, None), 
                  QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'in membersOf("tier-2-support"); in membersOf("tier-3-support")', 'in ("Standard", "Premium")', None, "is EMPTY"), 
                  QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'not in membersOf("tier-2-support"); not in membersOf("engineering"); not in membersOf("tier-3-support")', 'in ("Standard", "Premium")', None, "is EMPTY"), 
                  QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'not in membersOf("engineering")', 'in ("Standard", "Premium")', None, "is not EMPTY"), ],
                [ QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'is EMPTY', 'is EMPTY; = "Not Applicable"', 'is EMPTY; = "Public"', None), 
                  QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'is EMPTY', 'is EMPTY; = "Not Applicable"', 'in ("Eucalyptus Employees", "Eucalyptus and Reporter")', None), 
                  QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'in membersOf("engineering")', 'is EMPTY; = "Not Applicable"', None, None), 
                  QueryData('= Bug', 'in (Unconfirmed, Investigating)', 'not in membersOf("engineering")', 
                            'not in membersOf("engineering")', 'is EMPTY; = "Not Applicable"', None, None), ],
           ]

basequery = '''project in (Euca2ools, Broker, "SAN Storage", Eucalyptus) AND 
               issuetype in (Bug, Improvement) AND 
               status not in (Closed, Resolved)'''

print "issuetype|status|reporter|assignee|SLA|level|flagged|count|subtotal"
sumTotal = 0
for qgroup in querygroups:
  subTotal = 0
  data = []
  for query in qgroup:
    fullquery = basequery
    for attr in ['issuetype', 'status', 'reporter', 'assignee', 'SLA', 'level', 'flagged']:
        criteria = getattr(query, attr)
        if criteria:
            fullquery += " AND (%s) " % " OR ".join([ "%s %s" % (attr, x) for x in criteria.split(";") ])
    total, issues = jira.search_issues_with_total(fullquery)
    data.append("%s|%d" % ("|".join([repr(x) for x in query]), total))
    subTotal += total
  print "\n".join(data) + "|" + str(subTotal)
  sumTotal += subTotal

total, issues = jira.search_issues(basequery)
print "GRAND TOTAL: %d" % total
print "SUM TOTAL: %d" % sumTotal

