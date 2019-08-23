# Splash Page Extender
This script can be run to extend the splash page life on wireless devices on a Cisco Meraki network. If run continuously, it achieves the same behavior as having a setting to show the splash page only once.

## Installation
Edit the file variables.yaml with the contents below
```yaml
API_KEY: get-your-api-key-with-meraki
ORG_NAME: name-of-your-organization
NETWORK_NAME: name-of-the-targeted-network
SSID_NAME: name-of-the-ssid
```

## Usage

Trigger the script

```
python3 main.py
```

## Deploying on Google Cloud Platform
This will require a GCP account and the Cloud SDK command-line tool (gcloud) installed in your computer
- How to create a (free) GCP account: https://cloud.google.com/free/
- How to install gcloud: https://cloud.google.com/deployment-manager/docs/step-by-step-guide/installation-and-setup

```shell script
bash gcp-command.sh
```

You can run the file gcp-commands.sh if you want to deploy this script on a server-less infrastructure.
It consists of three steps:
1) It deploys a chron job that will be triggered every day at 00:05. This job will send a message to a PubSub topic.*
2) The second part is deploying the script as a Google Cloud Function, which will be triggered every time a new message is posted on the topic
3) Just a test to see if everything went well.

*This will only run successfully once, as you cannot have multiple chron jobs with the same name. If you want to change something, delete the chron job and rename it with a different name as you cannot reuse chron job names on the same GCP project.
```shell script
gcloud beta scheduler jobs delete update-splash-page-JOB
```
## License
[MIT](https://choosealicense.com/licenses/mit/)