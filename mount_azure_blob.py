from IPython.display import display
import ipywidgets as widgets
import subprocess
from functools import partial

def _mount_azure_blob_storage(btn, accountName, accountKey, containerName, mountPath):
    print("\nMounting azure blob storage...")
    account_name = accountName.value
    account_key = accountKey.value
    container_name = containerName.value
    mount_path = mountPath.value
    with open("fuse_connection.cfg", "w") as f:
        content = f"""accountName {account_name}\naccountKey {account_key}\ncontainerName {container_name}"""
        f.write(content)

    dependencies_install_command = """
        wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
        sudo dpkg -i packages-microsoft-prod.deb
        sudo apt-get update
        sudo apt-get install blobfuse
    """
    output = subprocess.check_output(dependencies_install_command, shell=True)
    print("Dependencies Installed...")

    command = f"""
        chmod 600 fuse_connection.cfg
        mkdir {mount_path}
        sudo blobfuse {mount_path} --tmp-path=/mnt/resource/blobfusetmp  --config-file=fuse_connection.cfg -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120
        rm fuse_connection.cfg
        rm packages-microsoft-prod.deb
      """
    output = subprocess.check_output(command, shell=True)
    print("Successfully Mounted...")


def mount_storage():
    accountName = widgets.Text(description='accountName')
    accountKey = widgets.Text(description='accountKey')
    containerName = widgets.Text(description='containerName')
    mountPath = widgets.Text(value="blob-storage", description='mountPath')
    btn = widgets.Button(
        button_style='success', icon='check',
        description='Mount Azure Blob Storage'
    )
    btn.on_click(
        partial(
            _mount_azure_blob_storage, 
            accountName=accountName, 
            accountKey=accountKey, 
            containerName=containerName, 
            mountPath=mountPath
        )
    )
    box = widgets.VBox(
        [
            widgets.HBox([accountName, accountKey, containerName]), 
            mountPath,
            btn,
        ]
    )
    return box
