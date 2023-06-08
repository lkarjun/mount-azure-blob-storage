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
    try:
        output = subprocess.check_output(dependencies_install_command, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        print("\nFailed to Install Dependencies...\n")
        print(str(e))

    print("Dependencies Installed...")


def create_config_file(
    account_name, account_key, container_name, config_export_path
):
    with open(config_export_path, "w") as f:
        content = f"""accountName {account_name}\naccountKey {account_key}\ncontainerName {container_name}"""
        f.write(content)
    print(f"Config created file={config_export_path}...")


def _mount_storage_helper(
    mount_path, account_name=None, account_key=None, container_name=None, config_file=None
):
    print("\nMounting azure blob storage (blobfuse v1)...")
    rm_config = False
    if config_file is None:
        rm_config = True
        config_file = "fuse_connection.cfg"
        with open(config_file, "w") as f:
            content = f"""accountName {account_name}\naccountKey {account_key}\ncontainerName {container_name}"""
            f.write(content)
    print("Installing Dependencies...")
    install_dependenices()

    command = f"""
        chmod 600 fuse_connection.cfg
        mkdir {mount_path}
        sudo blobfuse {mount_path} --tmp-path=/mnt/resource/blobfusetmp  --config-file={config_file} -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120
      """
    
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        print("\nFailed to Mount Blob Storage...\n")
        print(str(e))

    if rm_config:
        os.remove(config_file)

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
    if config_file:
        _mount_storage_helper(mount_path=mount_path, config_file=config_file)
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
        
