# Mount Azure Blob Storage in Colab

## How to use 
### Approch 1
```
from mount_azure_blob import mount_storage
mount_storage(mount_path="blob-storage", config_file=None)
```
output: 
![image](https://user-images.githubusercontent.com/58617251/222134815-9404dd84-8fb4-46c5-8919-e1c77748abfe.png)
Enter the credentials and click ```Mount Storage``` button

### Approch 2
```
from mount_azure_blob import mount_storage
mount_storage(mount_path="blob-storage", config_file="path-to-.env-file")
```
#### sample ```config_file``` / ```.env```
```
account_name="..."
account_key="..."
container_name="..."
```
output: 

![image](https://user-images.githubusercontent.com/58617251/222144492-88eebbfa-4e91-48c6-acec-950f2bf7b799.png)

### After mount
![image](https://user-images.githubusercontent.com/58617251/222145707-28b625a6-a1f0-479c-9748-e7ad69a18fa3.png)


## Reference

[Blobfusev1 official document](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-how-to-mount-container-linux)
