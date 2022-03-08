"""
Downloads the example data used for the freqtag pipeline.
"""
import urllib.request


def download_data():
    urllib.request.urlretrieve("https://osf.io/pmge9/download", "raw/exampledata_1.mat")
    urllib.request.urlretrieve("https://osf.io/hb7sd/download", "raw/exampledata_2.mat")


if __name__ == "__main__":
    download_data()
