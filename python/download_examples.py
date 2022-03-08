"""
Downloads the example data used for the freqtag pipeline.
"""
import urllib.request
from pathlib import Path

FILES_TO_DOWNLOAD = {
    "https://osf.io/pmge9/download": "raw/exampledata_1.mat",
    "https://osf.io/hb7sd/download": "raw/exampledata_2.mat",
}


def download():
    """
    Downloads data listed in FILES_TO_DOWNLOAD if they aren't already downloaded.
    """
    for from_url, to_path in FILES_TO_DOWNLOAD.items():
        to_path = Path(to_path)
        if not to_path.exists():
            print(f"Downloading {to_path} from {from_url}")
            to_path.parent.mkdir(exist_ok=True, parents=True)
            urllib.request.urlretrieve(from_url, to_path)


if __name__ == "__main__":
    download()
