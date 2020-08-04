# Rave-DL
Rips video and audio (with metadata) from music mixing website [RaveDJ](https://rave.dj/). Support the creators of the website on [Patreon](https://www.patreon.com/RaveDJ/). <br>

Install with `python3 -m pip install rave-dl` or `poetry add rave-dl`.

## Example Usage
### Application Programming Interface
```python
from rave_dl import RaveDJ

rave = RaveDJ('https://rave.dj/sZJr6b9MG6vpPA')
rave.scraper(filetype="mp3+mp4", metadata=True, output="hello_world")
```
### Command Line Interface
```bash
python3 -m rave-dl "https://rave.dj/sZJr6b9MG6vpPA" -m -f mp3+mp4 -o hello_world
```
## API
### class RaveDJ
Attributes:
* datastore (list): Contains information on multiple videos

Args:
* url (str): URL of RaveDJ video
### def scraper(filetype="mp4", metadata=False, output="output", bar=False)
Download music videos from RaveDJ.

Args:
* filetype (str, optional): Choose to download MP3s (mp3), MP4s (mp4), or both (mp3+mp4). Defaults to "mp4".
* metadata (bool, optional): Adds metadata (title, artist, album art) to MP3s. Defaults to False.
* output (str, optional): Folder files are downloaded to. Defaults to "output".
* bar (bool, optional): Shows download progress in the form of a bar. Defaults to False.
## CLI
Invoke it with `python3 -m rave-dl` or `python3 rave-dl.py`.
```bash
usage: rave-dl [-h] [-m] [-f FILETYPE] [-o OUTPUT] [-nb] [-v] URL

Rips video and audio (with metadata) from music mixing website RaveDJ. (v1.0)

positional arguments:
  URL                   link to RaveDJ video

optional arguments:
  -h, --help            show this help message and exit
  -m, --metadata        Adds metadata (title, artist, album art) to MP3s.
  -f FILETYPE, --filetype FILETYPE
                        Choose to download MP3s [mp3], MP4s [mp4], or both
                        [mp3+mp4].
  -o OUTPUT, --output OUTPUT
                        Folder to download files to.
  -nb, --nobar          Do not display bar when downloading.
  -v, --version         Show version number and exit.
```
