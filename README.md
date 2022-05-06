rasa x issue: https://forum.rasa.com/t/cannot-install-rasa-x-with-rei-neither-locally-nor-on-my-server/51648

# gcloud example (tested and worked with gck computing engine)
https://www.youtube.com/watch?v=R8gs-xJuhGs

# rasax version needs to be updated after deployment
https://forum.rasa.com/t/rasa-x-1-0-1-compatibility-issue-with-rasa-2-8-2-2-8-17-models/50220

# useful commands

**I might need to run with root user**

### If Rasa X does not start
it might be helpful to delete the Find Kube Context
`bash rei.bash -u` (uninstall)
Then reinstall `bash rei.bash -y`
Finally, re-deploy rasa x `rasactl start --project --values-file values.yml`

### upgrade through values.yml
`rasactl upgrade agitated-tu --values-file values.yml`

### connect with a rasa open source
`rasactl connect rasa`
This might be needed when we cannot upload the model to rasa x

### How to get custom server runing with rasactil connect
Follow this: https://github.com/RasaHQ/rasactl/issues/35#issuecomment-1115301599

`ps -ef | grep "rasa.*\-p 5005"`

The generated endpoint file was named as .endpoint.yaml under the PROJECY_DIRECTORY. Not under tmp anymore.