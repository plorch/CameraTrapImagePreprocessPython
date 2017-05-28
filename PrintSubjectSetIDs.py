from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow
"""
This is a script to print subject sets IDs 
given a list of subject_set.display_names

Only really necessary from when panoptes_upload_data2.py 
listed subject_set.display_name rather than subject_set.id as it does now.
"""

# Set subject sets to get IDs from. This
subject_set_display_names=('C7_HI1146a','C7_HI1149a','C7_HI1162a','C7_HI1165afalseremoved','C7_HI1181a','C7_HI1194a','C7_HI1197a','C7_MS1003a','C7_MS1007a','C7_MS1014a','C7_MS1019a','C7_MS1035a_3','C7_MS1039a','C7_MS1051a','C7_MS1062a','C7_MS1067a','C7_MS1071a','C7_MS1083a','C7_MS1087a','C7_MS1099a','C7_MS1103a','C7_MS1115a','C7_MS1126a','C7_MS1131a','C7_MS1135a','C7_MS1147a','C7_MS1151a','C7_MS1163a','C7_MS1167a','C7_MS1179a','C7_MS1190a','C7_MS1199a')

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
# To test, use this instead of the one after
#    s3=(x.display_name for x in project.links.subject_sets if x.display_name in subject_set_display_names)#
    s3=(x.id for x in project.links.subject_sets if x.display_name in subject_set_display_names)#

    for dn in s3:
        print("%s, " % (dn)),
#    for subject_set in project.links.subject_sets:
#        print("%s," % (subject_set.display_name)),
else:
    print("No subject sets in project %s or %s " % (project,project.display_name))