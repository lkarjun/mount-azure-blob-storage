import setuptools

setuptools.setup(
    name = "mount_azure_blob",
    version = "0.0.5",
    author = "Lalkrishna",
    url = "https://github.com/lkarjun/mount-azure-blob-storage/",
    description = "Mount Azure blob storage in google colab.",
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    py_modules=['mount_azure_blob'],
    install_requires = ["ipywidgets", "python-dotenv"],
    python_requires = ">=3.7",
    zip_safe = False,
)
