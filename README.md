# SSH-key-migrator
Create multiple users in a instance with sudo privileges and migrate their SSH keys to the home directories.

There may be situations where you need to create multiple users in any EC2 instance but the instance may not be under any stack in opsworks.
Creating the users one by one and adding the keys will take a lot of time if the number of users are more.
This script will help you to perform the task within a minute. All you need is provide the user names to be added and the rest will be taken care by the script.
Make sure that you upload the ssh-keys in the s3 bucket.
