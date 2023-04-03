from IPython.display import display
import ipywidgets as widgets
import subprocess
from functools import partial
from dotenv import load_dotenv
import os


def install_dependenices():
    dependencies_install_command = """
        wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
        sudo dpkg -i packages-microsoft-prod.deb
        sudo apt-get update
        sudo apt-get install blobfuse
        rm packages-microsoft-prod.deb
    """
    output = subprocess.check_output(dependencies_install_command, shell=True)
    print("Dependencies Installed...")


def _mount_storage_helper(account_name, account_key, container_name, mount_path):
    print("\nMounting azure blob storage...")
    with open("fuse_connection.cfg", "w") as f:
        content = f"""accountName {account_name}\naccountKey {account_key}\ncontainerName {container_name}"""
        f.write(content)

    install_dependenices()

    command = f"""
        chmod 600 fuse_connection.cfg
        mkdir {mount_path}
        sudo blobfuse {mount_path} --tmp-path=/mnt/resource/blobfusetmp  --config-file=fuse_connection.cfg -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120
        rm fuse_connection.cfg
      """
    output = subprocess.check_output(command, shell=True)
    print("Successfully Mounted...")


def _mount_storage__widget_helper(
    btn: widgets.Button,
    accountName: widgets.Text, 
    accountKey: widgets.Text, 
    containerName: widgets.Text, 
    mountPath: widgets.Text
):
    _mount_storage_helper(
        account_name=accountName.value,
        account_key=accountKey.value,
        container_name=containerName.value,
        mount_path=mountPath.value
    )


def mount_storage(mount_path = "blob-storage", config_file=None):
    if config_file and load_dotenv(dotenv_path=config_file):
        _mount_storage_helper(
            account_name=os.getenv("account_name"),
            account_key=os.getenv("account_key"),
            container_name=os.getenv("container_name"),
            mount_path=os.getenv("mount_path", default=mount_path)
        )
        os.environ.pop('container_name')
        os.environ.pop('account_key')
        os.environ.pop('account_name')
    else:
        accountName = widgets.Text(description='accountName')
        accountKey = widgets.Text(description='accountKey')
        containerName = widgets.Text(description='containerName')
        mountPath = widgets.Text(value=mount_path, description='mountPath')
        btn = widgets.Button(
            button_style='success', icon='check', description='Mount Storage'
        )
        btn.on_click(
            partial(
                _mount_storage__widget_helper, 
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
        
