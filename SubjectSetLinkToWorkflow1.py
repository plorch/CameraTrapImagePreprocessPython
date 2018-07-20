import os
import sys
sys.path.append('C:\Users\pdl\Documents\GitHub\panoptes-python-client\panoptes_client')
from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow

"""
This is a script that links subject sets to a workflow

The cli command for this is 
panoptes workflow add_subject_sets 1432 9436 9440 9443 9445 9447 9449 9450 9451 9452 9453 9454 9455 9482 9485 9488 9489 9491 9492 9493 9499 9500 9503 9509
"""

# Set workflow here each time you use it
workflow_id=1432
# Set subject sets to add to workflow
subject_sets=(20592,20594,20595,20598,20600,20605,20631,20632,20634,20636,20639,20640,20641,20642,20691,20692,20694,20695,20697,20698,20699,20700,20701,20702,20703,20704,20705,20706,20707,20708,20709,20710,20711)
#subject_sets=([9436,9440,9443,9445,9447,9449,9450,9451,9452,9453,9454,9455,9482,9485,9488,9489,9491,9492,9493,9499,9500,9503,9509])

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

#workflow.add_subject_sets([subject_sets])
workflow.add_subject_sets(subject_sets)
print("\nSubject sets added:")
print(subject_sets)
