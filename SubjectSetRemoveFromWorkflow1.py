import os
from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow

"""
This is a script that removes subject sets from a workflow
"""

# Set workflow here each time you use it
workflow_id=1432
# Set subject sets to add to workflow
subject_sets=(11343, 11372, 11373, 11375, 11376, 11379, 11381, 11382, 11383, 11384, 11385, 11388, 11391, 11393, 11394, 11395, 11397, 11406, 11407, 11408, 11409, 11411, 11413, 11414, 11416, 11417, 11418, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11433, 11434, 11435, 11436, 11437, 11438, 11439, 11440, 11441, 11442, 11444, 11445, 11446, 11448, 11450)

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
