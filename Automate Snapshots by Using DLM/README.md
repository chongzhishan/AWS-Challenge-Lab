## Add Tag to EBS Volume

1. **Sign in to the AWS Management Console:**
   - Go to [AWS Management Console](https://aws.amazon.com/console/) and sign in to your AWS account.

2. **Navigate to EC2 Dashboard:**
   - Click on the "Services" dropdown menu and select "EC2" under "Compute".

3. **Locate the EBS Volume:**
   - In the EC2 Dashboard, navigate to "Volumes" from the left-hand side menu.

4. **Select the EBS Volume:**
   - Identify and click on the EBS volume associated with WebServer1-38223953 or WebServer2-38223953.

5. **Add Tag:**
   - Once you've selected the correct volume, find the "Tags" tab in the details pane.

6. **Create Tag:**
   - Click on the "Add/Edit tags" button.
   - Add a tag with the following details:
     - **Key:** Name
     - **Value:** WebVol-38223953

7. **Save Changes:**
   - After entering the tag details, click on "Save" or "Save changes" to apply the tag to the EBS volume.

8. **Verification:**
   - Verify that the tag has been successfully added by checking the tags associated with the EBS volume.

9. **Repeat for the Other Volume:**
   - Repeat steps 4 to 8 for the EBS volume associated with the other server (WebServer1-38223953 or WebServer2-38223953).

## Create DLM Lifecycle Policy

10. **Navigate to Data Lifecycle Manager (DLM):**
    - In the navigation pane, go to Elastic Block Store and select Lifecycle Manager.

11. **Start Policy Creation:**
    - Click on "Create new lifecycle policy".

12. **Set Policy Type and Target Resources:**
    - Ensure "EBS snapshot policy" is selected for Policy type.
    - Choose "Volume" for Target resources.

13. **Define Target Resource Tags:**
    - Enter "Name" for Target resource tags key and "WebVol-38223953" for Target resource tags value.

14. **Provide Policy Description and IAM Role:**
    - Enter "Hourly Backup of Web Server Volumes" for Policy description.
    - Select "Choose another role" for IAM role and choose "AWSDataLifecycleManagerDefaultRole".

15. **Add Policy Tags:**
    - Click on "Add tag" under Tags.
    - Enter "Name" for Key and "Hourly-38223953" for Value.

16. **Set Schedule Details:**
    - Enter "Hourly" for Schedule name.
    - Choose "Daily" for Frequency.
    - Set "Every" to "1 hour".
    - Set "Starting at" to the time 5 minutes from now in UTC.

17. **Configure Retention:**
    - Choose "Age" for Retention type.
    - Set "Expire" to "1 days".

18. **Advanced Settings - Tagging:**
    - Expand Tagging in Advanced settings.
    - Check the "Copy tags from source" checkbox.

19. **Review and Create Policy:**
    - Click on "Review policy".
    - Review the configuration.
    - Click on "Create policy" to finalize and create the policy.

20. **Verification:**
    - Wait for approximately 20 minutes for the snapshots to be created.
    - Refresh the DLM dashboard and verify that two snapshots were created as per the policy.

## Replace Root Volume Using Snapshot

21. **Replace Root Volume:**
    - In the navigation pane, select "Instances", and then select the checkbox next to "WebServer1-38223953".
    - In the details pane, navigate to the "Storage" tab and copy the Volume ID: vol-0af529eb84348df5b.
    - Select "Replace root volume" in the "Recent root volume replacement tasks" section.

22. **Select Snapshot:**
    - In the "Replace root volume" dialog, choose "Snapshot" in the "Restore" dropdown menu.
    - Select the first snapshot in the list of snapshots provided.

23. **Create Replacement Task:**
    - Click on "Create replacement task".

24. **Wait for Replacement Task Completion:**
    - In the "Recent root volume replacement tasks" section, monitor the "Task state" value. Wait for it to change to "Successful".
    - It will take approximately 3-5 minutes for the replacement task to complete.

25. **Record Current Volume ID:**
    - Once the replacement task is successful, record the new EBS volume ID for WebServer1-38223953 in the "Current Volume ID" text box.

26. **Verify Replacement:**
    - Wait several minutes for the new Volume ID to appear.
    - Compare the volume IDs between the original and current in the provided table.

