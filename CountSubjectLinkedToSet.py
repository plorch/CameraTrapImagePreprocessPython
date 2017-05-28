from panoptes_client import SubjectSet, Subject, Project, Panoptes, Workflow
"""
This is a script to count all subjects in a set
"""

# TODO: put your username and password in here or use ENV vars
Panoptes.connect(username='Pat_Lorch', password='timzpw14')

# get a ref to the project we're uploading to -> change this for the correct project
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

# *** Change subject set to get list
# This currently fails to find the subjects attribute of a subject_set.links
subject_set=SubjectSet.find(7459)

print "Subjects:"
if hasattr(subject_set,'subjects'):
    print("Project %s or %s:" % (subject_set,subject_set.display_name))

    i=0
    for subject in subject_set.subjects():
#        print("%s " % (subject))
        i += 1
    print("\nSubjectSetID, SubjectName, SubjectsUploaded, FilesInUploadFolder\n") 
    print("%s,%s,%i,%i,0,\n" % (subject_set.id,subject_set.display_name,i,(i*3+1))) 

    print("\n")
else:
    print("No subjects in project %s or %s" % (subject_set,subject_set.display_name))
