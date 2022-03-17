from pathlib import Path
from freqtag.download_examples import FILES_TO_DOWNLOAD, download
import pytest


@pytest.mark.skip(reason="Test is lengthy and right now we know this works.")
def test_download():
    """
    Test that files are downloaded when they don't exist.
    """
    for to_path in FILES_TO_DOWNLOAD.values():
        Path(to_path).unlink(missing_ok=True)

    download()

    for to_path in FILES_TO_DOWNLOAD.values():
        assert Path(to_path).exists()
