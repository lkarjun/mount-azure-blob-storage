import setuptools

setuptools.setup(
    name = "mount_azure_blob",
    version = "0.0.1",
    author = "Lalkrishna",
    url = "arju66938@gmail.com",
    description = "Mount Azure blob storage in google colab.",
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    py_modules=['mount_azure_blob'],
    install_requires = "ipywidgets",
    python_requires = ">=3.7",
    zip_safe = False,
)
