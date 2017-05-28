import csv, os, signal, winsound
from panoptes_client import SubjectSet, Subject, Project, Panoptes
from panoptes_client.panoptes import PanoptesAPIException
# debugger with breakpoints set by pdb.set_trace()
#import pdb
"""
This is the version I have modified to work with my PC

Now that the cli is mature, there is a command line equivalent (that does not
write subject sets to the text file.
"""
# get a ref to the project we're uploading to -> change this for the correct project
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

# Debug check the workflows on the project
# for workflow in project.links.workflows:
#     print workflow.display_name


# SETUP variables for the script
# ------------------------------
saved_subjects = []
uploaded_subjects_count = 0
# csv_input_file = 'data/input_file_manifest.csv'
# project_id = 1
project_slug = 'pat-lorch/focus-on-wildlife-cleveland-metroparks'
# set_name = 'subject_set_name'

# get an API connection with our user creds
# TODO: put your username and password in here or use ENV vars
Panoptes.connect(username='Pat_Lorch', password='FlivBo@9')

## *** Change these every time you run it. ***
uploaddir=r'E:\UNPROCESSED\8th check August 2016\8thCheckAugust2016_2readytoupload\BC1024b_6\toupload'
print uploaddir
savedsubjs=os.path.join(os.path.split(os.path.split(uploaddir)[0])[0],'subject_sets_saved.txt')
print savedsubjs
set_name = 'C8_'+os.path.split(os.path.split(uploaddir)[0])[1]
#subject_set.display_name = 'C7_BK1152a_'+os.path.split(uploaddir)[1]
csv_input_file=os.path.join(uploaddir,'manifest.csv')

# number of csv rows to process in a batch
# NOTE: if any api failure occurs, this will be the max number of
# subjects rolled backed before stopping / reporting after the error.
CSV_BATCH_SIZE = 100

# Define functions for re-use
# ---------------------------
# create a new subject and set the metadata
# and the remote URL for the externally hosted images
# e.g. not via zooniverse s3
def create_external_subject(project, row):
    subject = Subject()
    subject.links.project = project
#   subject.locations.append({'image/jpeg': row['url']})
    # TODO: change the image MIME type to match your data, png, etc
    ##print os.path.join(uploaddir,row['#Image 1'])
    subject.add_location(os.path.join(uploaddir,row['#Image 1']))
    subject.add_location(os.path.join(uploaddir,row['#Image 2']))
    subject.add_location(os.path.join(uploaddir,row['#Image 3']))

   # NOTE: modify this to set whatever metadata you want
#    subject.metadata['origin'] = row['origin']
#    subject.metadata['subject_id'] = row['subject_id']
#    subject.metadata['image_name'] = row['image_name']
#    subject.metadata['licence'] = row['licence']

# TODO: You can set whatever metadata you want, or none at all
    ## I have #Image 1	#Image 2	#Image 3	ID, with # to stop ID from showing up when info button is clicked
    subject.metadata['#Image 1'] = row['#Image 1']
    subject.metadata['#Image 2'] = row['#Image 2']
    subject.metadata['#Image 3'] = row['#Image 3']
    subject.metadata['ID'] = row['ID']

    subject.save()
    return subject

def handle_batch_failure(saved_subjects):
    print('\nRolling back, attempting to clean up the the current batch of uploaded subjects.')
    for subject in saved_subjects :
        print('Removing the subject with id: {}'.format(subject.id))
        # this method may change in the future
        # https://github.com/zooniverse/panoptes-python-client/issues/39
        Subject.delete(subject.id, headers={'If-Match': subject.etag})

def add_batch_to_subject_set(subject_set, subjects):
    print('Linking {} subjects to the set with id: {}'.format(len(subjects), subject_set.id))
    subject_set.add(subjects)

# handle (Ctrl+C) keyboard interrupt
def signal_handler(*args):
    print('You pressed Ctrl+C! - attempting to clean up gracefully')
    handle_batch_failure(saved_subjects)
    raise SystemExit
#register the handler for interrupt signal
signal.signal(signal.SIGINT, signal_handler)

project = Project.find(slug=project_slug)
# e.g. https://www.zooniverse.org/projects/pat-lorch/cmp-wildlife-camera-traps
# project = Project.find(slug='pat-lorch/focus-on-wildlife-cleveland-metroparks')
# OR Just use the project id from the lab if you know it
# project = Project.find(PROJECT_ID_HERE)
## should be <Project 1793>

# Debug check the workflows on the project
# for workflow in project.links.workflows:
#     print workflow.display_name

# find / create the subject set to upload to
try:
    subject_set = SubjectSet.where(project_id=project.id, display_name=set_name).next()
    print("Using the existing subject set with id: {}.".format(subject_set.id))
except StopIteration:
    # create a new subject set for the new data and link it to the project above
    subject_set = SubjectSet()
    subject_set.links.project = project
    subject_set.display_name = set_name
    subject_set.save()
    print("Created a new subject set with id: {}.".format(subject_set.id))

# read the manifest and create externally linked subjects
with open(csv_input_file, 'rb') as csvfile:
    subjects_to_upload = csv.DictReader(csvfile)
    print("\nRead the csv maninfest, now building subjects for project id: {}".format(project.id))

    for count, row in enumerate(subjects_to_upload):
        # expected header format: image_name, origin, licence, link
        # print(row['image_name'], row['origin'], row['licence'], row['url'])

        # try and handle api failures, intermittent network, etc.
        try:
            subject = create_external_subject(project, row)
        except PanoptesAPIException as e:
            print('\nError occurred on row: {} of the csv file'.format(count+1))
            print('Details of error: {}'.format(e))
            handle_batch_failure(saved_subjects)
            raise SystemExit

        # save the list of subjects to add to the subject set above
        saved_subjects.append(subject)

        # for each batch of new subjects
        if (count + 1) % CSV_BATCH_SIZE == 0:
            add_batch_to_subject_set(subject_set, saved_subjects)
            # reset the saved_subjects for the next batch
            saved_subjects = []
            uploaded_subjects_count += CSV_BATCH_SIZE

# catch any left over batches in the file
if len(saved_subjects) > 0:
    add_batch_to_subject_set(subject_set, saved_subjects)
    uploaded_subjects_count += len(saved_subjects)

# This should write subject set names out to a file for use in running SubjectSetLinToWorkflow1.py
#  This file must be moved, deleted or renamed before the next set is uploaded
with open(savedsubjs, "a+") as subject_sets_saved:
    subject_sets_saved.write(",%s" % subject_set.id)
print("Finished uploading {} subjects".format(uploaded_subjects_count))
winsound.Beep(300,2000)