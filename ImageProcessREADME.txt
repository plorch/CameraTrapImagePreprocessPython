ImageProcessREADME.txt

* Move camera folders from check folder into subfolder
  * Move rougly 1/5th of folders from each reservation
* Open each folder and remove any camera check images, 
  * Check any paper time cards shown against camera date/time
  * Delete image sets of 3 that have camera checkers or are moving, as well as images of paper cards
  * These will usually be the first and last 3-9 images
  * Make sure that there are multiples of 3 images left 
    * Sometimes there is an extra image or two at start of end of a set taken during camera changes
  * This took 2.5 hours for roughly 1/6th of folders
* Run image_file_crunch_Parallel4.py on this folder 10:42-12:30, 2 hours
* Upload images in sets named for check and camera (e.g., C8_BE1011b)
  * Command line upload (much slower than client or cli and you cannot link to workflow without using client or cli)
    * In Subject Sets tab click New Subject set
    * Enter name like C8_BE1011b (cutting and pasting from folder name is best to avoid typos)
    * Drag all files from to upload folder to drop box in subject set field (cntrl A, click-drag, Alt-tab to subjects sets browser window, drop)
    * Once done uploading
      * Cut and past name of subject set into file to keep track of sets
      * Change name of toupload folder to uploaded
    * Move up to next folder and Repeat
  * Client code approach
    * Copy and paste path to upload folder from Explorer window into panoptes_upload_data3.py
    * Run panoptes_upload_data3.py
    * When it beeps
      * Change name of toupload folder to uploaded
    * Move up to next folder and Repeat
  * CLI approach
    * In Canopy, open command prompt with Tools -> Canopy command prompt
    * Change to directory to be uploaded (E:. cd UNPROCESSED\8th check August 2016\8thCheckAugust2016_2readytoupload\BR1013b\toupload)
    * Run add Subject set command
      * start by running panoptes configure (https://github.com/zooniverse/panoptes-cli)
      * panoptes subject_set create --project-id 1793 --display-name "C8_BE1011b"
		* output will be : 4667 C8_BE1011b, where 4667 is subject set ID
    * Run add images to set command
      * panoptes subject_set upload_subjects -m image/jpeg 4667 manifest.csv
    * Cut and past name of subject set into file to keep track of sets
    * Change name of toupload folder to upload
    * Move up to next folder and Repeat
* Unlink old sets (scripts are in C:\Users\pdl\Documents\GitHub\CameraTrapImagePreprocessPython)
  * Get list
    * Run PrintLinkedSubjecSets.py 
  * Unlink these, if you think they are done based on the Subjects report
    * Cut and paste the above list into SubjectSetRemoveFromWorkflow1.py
    * Run it
  * Get list of newly uploaded subject sets from E:\UNPROCESSED\8th check August 2016\8thCheckAugust2016_3\subject_sets_saved.txt
  * Link these
    * Cut and paste the above list into SubjectSetLinkToWorkflow1.py
