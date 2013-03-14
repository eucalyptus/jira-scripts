from jiraauth import jclient
import debugmode

"""
This script was used to copy target versions (customfield_10304)
into the fix version field.  It's a decent example of how to
iterate over search results and update issues in the result set
"""

i = 0
maxResults=50
num = 50
while i < num:
    num, results = jclient.search_issues_with_total('"Target Version/s" is not EMPTY and status not in (Resolved, Closed)', startAt=i)
    for issue in results:
        print "checking " + issue.key
        newFixVersions = None
        for target_version in issue.fields.customfield_10304:
            if not len([ x for x in issue.fields.fixVersions if x.id == target_version.id ]):
                if not newFixVersions:
                    newFixVersions = [ x for x in issue.fields.fixVersions ]
                newFixVersions.append(target_version)
        if newFixVersions:
            print "Updating " + issue.key + " was " + \
                  ",".join(sorted([x.name for x in issue.fields.fixVersions ])) + \
                  " now " + ",".join(sorted([x.name for x in newFixVersions ]))
            issue.update(fixVersions=[ { 'name': x.name } for x in newFixVersions ])
    i += maxResults
    print i
     
