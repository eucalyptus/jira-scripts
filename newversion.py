#!/usr/bin/python


import sys
from jiraauth import jclient as jira

'''
Usage example -- to create version 3.2.2 after 3.2.1 in all relevant projects: 
newversion.py EUCA,DOC,VNX,SAN,BROKER,INST 3.2.2 3.2.1
'''
 
projects = sys.argv[1].split(',')
new_version = sys.argv[2]
after_version = None
if len(sys.argv) > 2:
  after_version = sys.argv[3]

for proj in projects:
  prev_ver_id = None
  this_ver_id = None
  proj_ver = jira.project_versions(proj)
  for v in proj_ver:
    if after_version and v.name == after_version:
      prev_ver_id = v.id
    elif v.name == new_version:
      this_ver_id = v.id
  if not this_ver_id:
    # version does not exist yet; create it
     this_ver_id = jira.create_version(name=new_version, project=proj).id
  if prev_ver_id:
    jira.move_version(this_ver_id, after=prev_ver_id)
