# Validation of the tutorial done by Team-1

## Deploying Federated Learning on Instances/Docker Across Multiple Servers in AWS


### Reproduction of the tutorial

Generally, the code executed with no major issues.

> [!WARNING]
> ```python /client.py --partition-id 0 --server-address 127.0.0.1:8080```
> The following code did not execute on my machine properly because of the auxulary `/` in the command line (`/client.py`). This is not a critical mistake, probably just a typo, which can be easlity and quickly fixed.

> [!NOTE]
> We did not need to create the `run_random_clients.sh` since it was already created by the authors