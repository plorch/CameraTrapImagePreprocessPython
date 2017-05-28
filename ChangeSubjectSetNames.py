from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow
"""
This is a script to change subject names 
given a list of subject_sets

Only really necessary if you screw up subject_set_names when doing uploads with
panoptes_upload_data2.py.

*** This never worked.  Probably not possible.
"""

# Set subject sets to change names
subject_set_IDs=('9436','9440','9443','9445','9447','9449','9450','9451','9452','9453','9454','9455','9482','9485','9488','9489','9491','9492','9493','9499','9500','9503','9509')

# TODO: put your username and password in here or use ENV vars
Panoptes.connect(username='Pat_Lorch', password='timzpw14')

# get a ref to the project we're uploading to -> change this for the correct project
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

print("\nChosen project: %s " % project.display_name)

if hasattr(project.links,'subject_sets'):
    s3=(x.display_name for x in project.links.subject_sets if x.id in subject_set_IDs) #
    print("Starting names of subject sets:")
    for dn in s3:
#        print("%s to %s, " % (dn,(dn[:1]+'8'+dn[2:]))),
        print("%s, " % (dn)),
#    s4=(x.id for x in project.links.subject_sets if x.id in subject_set_IDs)
    for x in project.links.subject_sets:
        if x.id in subject_set_IDs:
            x=(x[:1]+'8'+x[2:])
    print("\nNew names of subject sets:")
    for dn in s3:
        print("%s, " % (dn)),
else:
    print("No subject sets in project %s or %s " % (project,project.display_name))