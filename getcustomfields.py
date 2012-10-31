#!/usr/bin/python

import sys
from jiraauth import jclient as jira

'''
Synopsis: Get all visible custom field ids and names,
along with applicable projects and issue types
'''

projectIds = [ x.id for x in jira.projects() ]
issuetypeIds = [ x.id for x in jira.issue_types() ]

meta = jira.createmeta(projectIds=projectIds, 
                       issuetypeIds=issuetypeIds, 
                       expand='projects.issuetypes.fields')
fields = dict()
for p in meta['projects']:
  for i in p['issuetypes']:
    for f in i['fields'].keys():
      if not fields.has_key(f):
        fields[f] = (i['fields'][f]['name'], set([ p['key'] ]), set([ i['name'] ]))
      else:
        fields[f][1].add(p['key'])
        fields[f][2].add(i['name'])

print "\n".join([ "%s: %s (%s | %s)" % (x, fields[x][0], 
                                        ','.join(fields[x][1]),
                                        ','.join(fields[x][2])) for x in fields.keys() ])
