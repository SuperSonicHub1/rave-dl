# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rave_dl']
install_requires = \
['regex>=2020.7.14,<2021.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'rave-dl',
    'version': '1.0',
    'description': 'Rips video and audio (with metadata) from music mixing website RaveDJ.',
    'long_description': '# Rave-DL\nRips video and audio (with metadata) from music mixing website [RaveDJ](https://rave.dj/). Support the creators of the website on [Patreon](https://www.patreon.com/RaveDJ/). <br>\n\nInstall with `python3 -m pip install rave-dl` or `poetry add rave-dl`.\n\n## Example Usage\n### Application Programming Interface\n```python\nfrom rave-dl import RaveDJ\n\nrave = RaveDJ(\'https://rave.dj/sZJr6b9MG6vpPA\')\nrave.scraper(filetype="mp3+mp4", metadata=True, output="hello_world")\n```\n### Command Line Interface\n```bash\npython3 -m rave-dl "https://rave.dj/sZJr6b9MG6vpPA" -m -f mp3+mp4 -o hello_world\n```\n## API\n### class RaveDJ\nAttributes:\n* datastore (list): Contains information on multiple videos\n\nArgs:\n* url (str): URL of RaveDJ video\n### def scraper(filetype="mp4", metadata=False, output="output")\nDownload music videos from RaveDJ.\n\nArgs:\n* filetype (str, optional): Choose to download MP3s (mp3), MP4s (mp4), or both (mp3+mp4). Defaults to "mp4".\n* metadata (bool, optional): Adds metadata (title, artist, album art) to MP3s. Defaults to False.\n* output (str, optional): Folder files are downloaded to. Defaults to "output".\n## CLI\nInvoke it with `python3 -m rave-dl` or `python3 rave-dl.py`.\n```bash\nusage: rave-dl [-h] [-m] [-f FILETYPE] [-o OUTPUT] [-nb] [-v] URL\n\nRips video and audio (with metadata) from music mixing website RaveDJ. (v1.0)\n\npositional arguments:\n  URL                   link to RaveDJ video\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -m, --metadata        Adds metadata (title, artist, album art) to MP3s.\n  -f FILETYPE, --filetype FILETYPE\n                        Choose to download MP3s [mp3], MP4s [mp4], or both\n                        [mp3+mp4].\n  -o OUTPUT, --output OUTPUT\n                        Folder to download files to.\n  -nb, --nobar          Do not display bar when downloading.\n  -v, --version         Show version number and exit.\n```',
    'author': 'Kyle Williams',
    'author_email': 'kyle.anthony.williams2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SuperSonicHub1/rave-dl',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
