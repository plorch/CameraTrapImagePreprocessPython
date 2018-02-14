import os
from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow

"""
This is a script that removes subject sets from a workflow
"""

# Set workflow here each time you use it
workflow_id=1432
# Set subject sets to add to workflow
subject_sets=(17481, 17492, 17493, 17494, 17495, 17496, 17497, 17498, 17499, 17500, 17501, 17502, 17503, 17504, 17505, 17506, 17507, 17508, 17509, 17510, 17511, 17512, 17513, 17514, 17515)
# Last set 16065, 16112, 16113, 16114, 16115, 16125, 16129, 16130, 16131, 16132, 16133, 16135, 16136, 16137, 16139, 16143, 16146, 16148, 16152, 16153, 16155, 16156, 16157, 16159, 16160, 16164, 16165, 16166, 16167, 16168, 16169, 16170, 16171, 16172, 16173, 16174

# TODO: put your username and password in here or use ENV vars
Panoptes.connect(username='Pat_Lorch', password=os.environ['ZOONPASS'])

# get a ref to the project we're uploading to -> change this for the correct project
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

# Debug check the workflows on the project
#i=0
#print "Workflows:"
#for workflow in project.links.workflows:
#    i=i+1
#    print("%i %s or %s " % (i,workflow,workflow.display_name))


workflow=Workflow.find(workflow_id)
print("\nChosen workflow: %s " % workflow.display_name)

workflow.remove_subject_sets(subject_sets)
print("\nSubject sets removed:")
print(subject_sets)
