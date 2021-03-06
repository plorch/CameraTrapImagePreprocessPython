import os
import os
from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow
"""
This is a script to print subject sets linked to
a workflow to be used in SubjectSetLinkToWorkflow1.py
or SubjectSetRemoveFromWorkflow1.py

The cli command for this is 
panoptes subject_set ls --project-id 1793 --workflow-id 1432
but it does not give a nice list.
"""

# TODO: put your username and password in here or use ENV vars
Panoptes.connect(username='Pat_Lorch', password=os.environ['ZOONPASS'])

# get a ref to the project we're uploading to -> change this for the correct project
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

# Assumes you have at least one workflow or it fails badly

print "Workflows and linked subject sets:"
for i,workflow in enumerate(project.links.workflows):
#    see if workflow.links.subject_sets exists
    if hasattr(workflow.links,'subject_sets'):
        print("%i %s or %s " % (i,workflow,workflow.display_name))
# You can comment out one of the following
#    This one gives you a readable list with id and name
        for subject_set in workflow.links.subject_sets:
            print("%s or %s " % (subject_set,subject_set.display_name))
#    This one gives you a comma separated list you can paste into 
#     SubjecSetRemoveFromWorkflow1.py *** Leave off the final , when you copy
        for subject_set in workflow.links.subject_sets:
            print("%s," % (subject_set.id)),

# This is ugly, but it works
#        print ",".join(map(str,workflow.links.subject_sets))
        print("\n")
    else:
        print("No linked subjects in workflow %i %s or %s " % (i,workflow,workflow.display_name))
