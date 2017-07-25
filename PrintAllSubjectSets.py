import os
from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow
"""
This is a script to print all subject sets linked to
a project
"""

# TODO: put your username and password in here or use ENV vars
Panoptes.connect(username='Pat_Lorch', password=os.environ['ZOONPASS'])

# get a ref to the project we're uploading to -> change this for the correct project
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

print "Subject sets:"
if hasattr(project.links,'subject_sets'):
    print("Project %s or %s:" % (project,project.display_name))

    for subject_set in project.links.subject_sets:
        print("%s or %s " % (subject_set,subject_set.display_name))
#    This gives you a comma separated list you can paste into 
#     SubjecSetRemoveFromWorkflow1.py *** Leave off the final , when you copy
    for subject_set in project.links.subject_sets:
        print("%s," % (subject_set.id)),

# This is ugly, but it works
#        print ",".join(map(str,workflow.links.subject_sets))
    print("\n")
else:
    print("No subject sets in project %s " % (project))
