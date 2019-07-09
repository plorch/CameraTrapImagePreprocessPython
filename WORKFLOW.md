# AI commnands
## Commands in image processing workflow running AI trained previously

### To set up transfer after configuring AWS instance based on notes in Joplin
From mac terminal (not logged into AWS instance)

* `scp -i ~/.ssh/AWShomeKey3.pem ~/Desktop/transferArchive/train_1000_2nd_4_best_weights_kfold_0.tar.gz ubuntu@ec2-18-220-206-163.us-east-2.compute.amazonaws.com:/home/ubuntu/`

### ssh to AWS machine, install aws cli, run aws configure, and import model

* `ssh -i /Users/plorch/.ssh/AWShomeKey3.pem ubuntu@ec2-18-220-206-163.us-east-2.compute.amazonaws.com`

*** If you are starting from a new instance: ***

* `pip3 install awscli --upgrade --user`
* `aws configure`
    * Enter access key, secret key, and region based on Amazon eWallet record
* `transfer --import train_1000_2nd_4_best_weights_kfold_0.tar.gz`
    * Destination: C24images_out
* Copy in this file from s3 to main directory with something like
    * `aws s3 cp s3://"cleveland-metroparks-trail-cam-image-trainset1/24thCheckMarch2018/WORKFLOW.md . --region us-east-2`
    * Now these commands may be modified in vim, saved and then cut and pasted into aws cli

### to start a background tmux session

* `tmux new -s model` to start a tmux session called model
* `tmux attach -t model` to re-enter a session after a connection timeout

### Rename last output file, move it to AWS S3, and rm old tar file 
To modify between batches in vim type : then something like 33,35s/OE_WA_WC/MS/g
Check to see that directory names are correct.

* `mv C22images_out/train_1000_2nd_4_server_weights_predictions.csv C24images_out/train_1000_2nd_4_server_weights_predictionsC24_MS.csv`
* `aws s3 cp C24images_out/train_1000_2nd_4_server_weights_predictionsC24_MS.csv s3://"cleveland-metroparks-trail-cam-image-trainset1/24thCheckMarch2018/train_1000_2nd_4_server_weights_predictionsC24_MS.csv" --region us-east-2`
* `rm 24_MS.tar.gz` 

### Remove old images and directories

* `rm -r C24images/MS*`

### Copy in new tar with images and unpack
To modify between batches in vim type : then something like 44,46s/MS/NC/g

* `aws s3 cp s3://cleveland-metroparks-trail-cam-image-trainset1/24thCheckMarch2018/24_NC.tar.gz C24images/ --region us-east-2`
* `tar -xzf C24images/24_NC.tar.gz -C C24images/`
* `mv C24images/24_NC.tar.gz .`

### Check for bad files

* `find C24images/ -name "*JPG" -exec jpeginfo -c {} \; | grep -E "WARNING|ERROR"`
* `transfer --predict C24images --project train_1000_2nd_4` 
