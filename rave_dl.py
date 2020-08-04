import re
import sys
import requests as r
import json
import os
from argparse import ArgumentParser
import sys

__version__ = "1.0"


def download(url: str, filename: str, bar: bool = False) -> str:
    """Download a file from the internet.

    Args:
        url (str): URL of file
        filename (str): Desired name of file.
        bar (bool, optional): Show download bar. Defaults to False.
    """
    with open(filename, "wb") as f:
        response = r.get(url, stream=True)
        total_length = response.headers.get("content-length")
        if total_length and bar:
            dl = 0
            total_length = int(total_length)
            print(f"Downloading {filename}...")
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write(
                    f"\r {round((dl / total_length)*100)}% [{'='*done}{' '*(50-done)}]"
                )
                sys.stdout.flush()
            sys.stdout.write("\n")
        else:
            f.write(response.content)
    return filename


class RaveDJ:
    """rave-dl
    =====
    Rips video and audio (with metadata) from music mixing website RaveDJ [https://rave.dj/].
    Support the creators of the website on Patreon [https://www.patreon.com/RaveDJ/].

    Attributes:
        datastore (list): Contains information on multiple videos
    """

    def __init__(self, url: str):
        """Extract Env.datastore object from given webpage.

        Args:
            url (str): URL of RaveDJ video
        """
        # Verifies given URL
        if re.search(r".*\.*rave\.dj/.*", url) == None:
            sys.exit(f"'{url}' is an invalid link! Try again...")

        page = r.get(url)

        # Select the <script> with the 'Env' variables
        scripts = re.findall(r"<script>([^<]*)</script>", page.text, re.MULTILINE)
        env = scripts[1]

        dataStore = env.splitlines()[16]  # Capture the Env.dataStore variable
        dataStoreClean = dataStore.replace("   Env.dataStore = ", "").replace(
            " // Raw JSON", ""
        )  # Remove extraneous text from JSON
        self.datastore = json.loads(dataStoreClean)

    def scraper(
        self,
        filetype: str = "mp4",
        metadata: bool = False,
        output: str = "output",
        bar: bool = False,
    ) -> None:
        """Download music videos from RaveDJ.

        Args:
            filetype (str, optional): Choose to download MP3s (mp3), MP4s (mp4), or both (mp3+mp4). Defaults to "mp4".
            metadata (bool, optional): Adds metadata (title, artist, album art) to MP3s. Requires eyeD3 (pip install rave-dl[metadata]). Defaults to False.
            output (str, optional): Folder files are downloaded to. Defaults to "output".
            bar (bool, optional): Shows download progress in the form of a bar. Defaults to False.
        """
        data = self.datastore["content"][
            0
        ]  # Grabs the dictionary necessary for downloading the desired video

        # Creates folder(s) for file(s) to go in
        path = os.path.join(output)
        if not os.path.exists(path):
            os.makedirs(path)

        # Looking through the dataStore for necessary variables
        video = data["urls"]["default"]
        audio = data["urls"]["audio"]
        thumbnail = data["thumbnails"]["default"]
        artist = data["artist"]
        dj = data["dj"]["displayName"]
        title = data["title"]

        # Create an 'author' variable
        if not dj == "":
            author = f"DJ {dj} [{artist}]"
        else:
            author = artist

        # Download files and apply metadata
        def mp3(thumbnail=thumbnail):
            audio_download = download(
                audio, os.path.join(path, f"{author} - {title}.mp3"), bar=bar
            )
            if metadata == True:
                try:
                    import eyed3
                except ModuleNotFoundError:
                    sys.exit(
                        "To apply metadata, install eyeD3 with pip install rave-dl[metadata]."
                    )
                mp3 = eyed3.load(audio_download)
                if mp3.tag == None:
                    mp3.initTag()
                mp3.tag.title = title
                mp3.tag.artist = author
                thumbnail = download(
                    thumbnail, os.path.join(path, "album.jpg"), bar=bar
                )
                mp3.tag.images.set(3, open(thumbnail, "rb").read(), "image/jpeg")
                mp3.tag.save()

        def mp4():
            download(video, os.path.join(path, f"{author} - {title}.mp4"), bar=bar)

        if filetype == "mp3":
            mp3()
        elif filetype == "mp4":
            mp4()
        elif filetype == "mp3+mp4":
            # Have the 'mp3+mp4' files go into their own folder
            path = os.path.join(path, f"{author} - {title}")
            if not os.path.exists(path):
                os.makedirs(path)
            mp3()
            mp4()


# Command line application
if __name__ == "__main__":
    parser = ArgumentParser(
        prog="rave-dl",
        description=f"Rips video and audio (with metadata) from music mixing website RaveDJ. (v{__version__})",
    )
    parser.add_argument("URL", help="link to RaveDJ video")
    parser.add_argument(
        "-m",
        "--metadata",
        help="Adds metadata (title, artist, album art) to MP3s.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--filetype",
        help="Choose to download MP3s [mp3], MP4s [mp4], or both [mp3+mp4].",
        default="mp4",
    )
    parser.add_argument(
        "-o", "--output", help="Folder to download files to.", default="output"
    )
    parser.add_argument(
        "-nb",
        "--nobar",
        help="Do not display bar when downloading.",
        action="store_false",
        default="True",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s version " + __version__,
        help="Show version number and exit.",
    )
    args = parser.parse_args()
    RaveDJ(args.URL).scraper(
        filetype=args.filetype,
        metadata=args.metadata,
        output=args.output,
        bar=args.nobar,
    )
