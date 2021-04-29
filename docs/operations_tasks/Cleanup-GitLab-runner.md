---
layout: default
title: Clean up GitLab Runner
parent: Operations tasks
---

# Clean up GitLab runner for Integration tests

If the integration tests are failing due to the following error:

```
ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device
```

Try doing the following to solve the issue:

1. Get the secrets from AWS secrets and SSH into the Gitlab runner EC2 instance.
    ```
    $ ssh -i "ingest-gitlab.pem" ubuntu@ec2-3-83-134-192.compute-1.amazonaws.com
    ```

2. Remove untagged docker images
    ```
    $ sudo docker rmi $(sudo docker images | grep none | awk '{print $3}')
    ```

3. Remove unused packages
    ```
    $ sudo apt-get autoremove
    ```

# References:
* https://stackoverflow.com/questions/60248189/linux-headers-are-consuming-a-lot-of-disk-space-on-the-ec2-machine-is-it-safe-t
* https://techoverflow.net/2019/08/16/how-to-identify-large-directories-for-no-space-left-on-device-on-linux/#:~:text=Long%20answer,space%20left%20to%20write%20on.&text=Check%20the%20Use%20%25%20column%20%E2%80%93%20you,system%20is%20mounted)%20is%20full
* https://jimhoskins.com/2013/07/27/remove-untagged-docker-images.html