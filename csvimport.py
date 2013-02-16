from jiraauth import jclient as jira
from jira.exceptions import JIRAError
import json
from collections import namedtuple
from StringIO import StringIO
import csv
import time

idx=0
issue_data = []
issues = []

#### Change this line to match your csv format ####
IssueData = namedtuple('IssueData', ['project', 'issuetype', 'summary', 
                                     'reporter', 'dependencies', 'due_date'])

# Read the file into a list of named tuples
reader = csv.reader(open(sys.argv[1], "rb"), delimiter=',', quotechar='"')
for line in reader:
    issue_data.append(IssueData(*line))

# For imports into a single project, this was useful to deal with restarting
# after a failure.  You simply have to know that you have a contiguous
# block of issues.  It would be better to write a new csv mapping rows to
# issues...
"""
while idx < 114:
    issues.append(jira.issue('CFP-' + str(idx+150)))
    print "Fetching CFP-" + str(idx+150)
    idx += 1
"""

while idx < len(issue_data):
    i = issue_data[idx]

    #### Change this to utilize the fields you care about ####
    issues.append(jira.create_issue(fields={'project':{'key': i.project},
                                            'summary':i.summary,
                                            'description':'',
                                            'issuetype':{'name': i.issuetype},
                                           }, prefetch=True))
    current = issues[-1]
    current.update(reporter={'name':i.reporter})
    # current.update(duedate=time.strftime('%Y-%m-%d', time.strptime(i.due_date, "%m/%d/%y")))
    idx += 1

# Iterate through the list again to make links.
idx = 0
while idx < len(issues):
    if issue_data[idx].dependencies.replace(" ", "") != "":
        for link_idx in issue_data[idx].dependencies.replace(" ", "").split(","):
            # TODO: allow deps of the form link_type:row ?  For now all links are of the same type
            jira.create_issue_link('Blocks', issues[int(link_idx)-1].key, issues[idx].key)
    idx += 1

print "Issues have been created!\n" + "\n".join([ 'https://eucalyptus.atlassian.net/browse/%s' % x.key for x in issues ]))

