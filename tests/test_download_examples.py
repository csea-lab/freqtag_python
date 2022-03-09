from pathlib import Path
from python.download_examples import FILES_TO_DOWNLOAD, download


def test_download():
    """
    Test that files are downloaded when they don't exist.
    """
    for to_path in FILES_TO_DOWNLOAD.values():
        Path(to_path).unlink(missing_ok=True)

    download()

    for to_path in FILES_TO_DOWNLOAD.values():
        assert Path(to_path).exists()
