import os
import csv
import winsound
from panoptes_client import SubjectSet, Subject, Project, Panoptes
from panoptes_client.panoptes import PanoptesAPIException

"""
This is the version I have modified to work with my PC

Now that the cli is mature, there is a command line equivalent (that does not
write subject sets to the text file.
"""
# TODO: put your username and password in here or use ENV vars
Panoptes.connect(username='Pat_Lorch', password=os.environ['ZOONPASS'])

# get a ref to the project we're uploading to -> change this for the correct project
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

# Debug check the workflows on the project
# for workflow in project.links.workflows:
#     print workflow.display_name

# EITHER create a new subject set linked to the project form above
subject_set = SubjectSet()
subject_set.links.project = project
## *** Change these every time you run it. ***
uploaddir=r'E:\UNPROCESSED\8th check August 2016\8thCheckAugust2016_3\WC1376c\toupload'
print uploaddir
savedsubjs=os.path.join(os.path.split(os.path.split(uploaddir)[0])[0],'subject_sets_saved.txt')
print savedsubjs
subject_set.display_name = 'C8_'+os.path.split(os.path.split(uploaddir)[0])[1]
#subject_set.display_name = 'C7_BK1152a_'+os.path.split(uploaddir)[1]
manifest=os.path.join(uploaddir,'manifest.csv')
## If you get an error here, it is likely because you already created a set with that name.  Delete it or add a _2 or something
subject_set.save()

# OR find an existing subject set to add subject to
## subject_set = SubjectSet.find(SUBJECT_SET_ID_HERE)

# empty list to add the saved subjects to the subject set
saved_subjects = []

# read the manifest and create externally linked subjects
# NOTE: TRY and to this in batches of 500 - 1000K images to avoid a failure
# not saving subject and linking to a subject set
with open(manifest, 'rb') as csvfile:
    subjects_to_upload = csv.DictReader(csvfile)
    for row in subjects_to_upload :
        # expected header format: image_name, origin, licence, link
        # print(row['image_name'], row['origin'], row['licence'], row['link'])

        # creat a new subject and set the metadata and the remote URL for the externally hosted images (not via zooniverse s3)
        subject = Subject()
        subject.links.project = project
        # TODO: change the image MIME type to match your data, png, etc
        ##print os.path.join(uploaddir,row['#Image 1'])
        subject.add_location(os.path.join(uploaddir,row['#Image 1']))
        subject.add_location(os.path.join(uploaddir,row['#Image 2']))
        subject.add_location(os.path.join(uploaddir,row['#Image 3']))
# TODO: You can set whatever metadata you want, or none at all
        ## I have #Image 1	#Image 2	#Image 3	ID, with # to stop ID from showing up when info button is clicked
        subject.metadata['#Image 1'] = row['#Image 1']
        subject.metadata['#Image 2'] = row['#Image 2']
        subject.metadata['#Image 3'] = row['#Image 3']
        subject.metadata['ID'] = row['ID']
        # handle api failures (network, etc)
        try:
            subject.save()
        except PanoptesAPIException:
            print('Error occurred, rolling back and cleaning up the created subjects.')
            for subject in saved_subjects :
                print('removing the subject with id: {}'.format(subject.id))
                # this method may change in the future, https://github.com/zooniverse/panoptes-python-client/issues/39
                Subject.delete(subject.id, headers={'If-Match': subject.etag})
            raise SystemExit

        # save in the list of subjects to add to the subject set above
        saved_subjects.append(subject)
        # add the subject to the subjet set 1 at a time.
        # but there is a more efficient way of adding this all at once (see below)
        # subject_set.add(subject)

# link the saved subjects to the subject set
# NOTE: this will only run after the whole file is processed and all subjects saved successfully
# try and keep the manifest set of data small enough to not have problems
# perhaps process large manifests in batches instead of all at once like i have it here
# happy to help out with this rather than have busted uploads to cleanup
subject_set.add(saved_subjects)

# This should write subject set names out to a file for use in running SubjectSetLinToWorkflow1.py
#  This file must be moved, deleted or renamed before the next set is uploaded
with open(savedsubjs, "a+") as subject_sets_saved:
    subject_sets_saved.write(",%s" % subject_set.id)
winsound.Beep(300,2000)