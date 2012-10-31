#!/usr/bin/python

import sys
from jiraauth import jclient as jira

'''
Synopsis: Get possible values for a specific field
Example: getfieldvalues.py EUCA Bug Hypervisor
'''

proj = sys.argv[1]
issuetype = sys.argv[2]
field = sys.argv[3]

issuetypes = dict([ (x.name, x.id) for x in jira.issue_types() ])
meta = jira.createmeta(projectIds=[ jira.project(proj).id ], 
                       issuetypeIds=[issuetypes[issuetype]], 
                       expand='projects.issuetypes.fields')
fields = meta['projects'][0]['issuetypes'][0]['fields']
target = [ fields[x] for x in fields.keys() 
           if fields[x]['name'] == field ][0]

print "\n".join([ x.get('name', x.get('value', '')) for x in target['allowedValues'] ])
