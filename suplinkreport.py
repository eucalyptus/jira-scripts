#!/usr/bin/python

'''
Synopsis: This script generates an html report of Engineering issues linked
to SUP issues
'''

from jiraauth import jclient as jira

issues = jira.search_issues('''project = SUP''')

def l(k):
  return '<a href="https://eucalyptus.atlassian.net/browse/%s">%s</a>' % (k, k)

def dump_issue(issuekey, customers, sups):
  issue = jira.issue(issuekey)
  print "<tr><td>"
  print ("</td><td>".join([ l(issue.key), 
               issue.fields.summary, 
               issue.fields.status.name, 
               issue.fields.issuetype.name, 
               getattr(issue.fields.assignee, 'displayName', 'Unassigned'),
               ",".join([ l(k) for k in sups ]),
               "; ".join(customers) ]) + "</td></tr>").encode("utf-8")
   
bugList = dict()
supList = dict()
for x in issues:
  if len(x.fields.issuelinks):
    # Get affected customers
    customers = [ y.value for y in x.fields.customfield_10900 or [] ]
    for link in x.fields.issuelinks:
      bugKey = None
      if hasattr(link, 'outwardIssue'):
        bugKey = link.outwardIssue.key
      else:
        bugKey = link.inwardIssue.key
      if bugKey.startswith('SUP'):
        continue
      if not bugList.has_key(bugKey):
        bugList[bugKey] = set()
        supList[bugKey] = set()
      bugList[bugKey].update(set(customers))
      supList[bugKey].add(x.key)

print "<html><body><table border='1'>"
print "<tr><th>Key</th><th>Summary</th><th>Status</th><th>Issue Type</th><th>Assignee</th><th>SUP issues</th><th>Customers Affected</th></tr>"
for key in sorted(bugList.keys()):
    dump_issue(key, bugList[key], supList[key])
print "</table></body></html>"
