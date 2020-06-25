import os
import shutil
import sys
from urllib.request import urlopen
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def download_ffmpeg_binary():
    """ Download/copy ffmpeg binary for local development.
    """
    # Get ffmpeg fname
    sys.path.insert(0, os.path.join(ROOT_DIR, "imageio_ffmpeg"))
    try:
        from _definitions import FNAME_PER_PLATFORM, get_platform
    finally:
        sys.path.pop(0)
    fname = FNAME_PER_PLATFORM[get_platform()]

    # Clear
    clear_binaries_dir(os.path.join(ROOT_DIR, "imageio_ffmpeg", "binaries"))
    # Download from Github
    base_url = "https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/"
    filename = os.path.join(ROOT_DIR, "imageio_ffmpeg", "binaries", fname)
    print("Downloading", fname, "...", end="")
    with urlopen(base_url + fname, timeout=5) as f1:
        with open(filename, "wb") as f2:
            shutil.copyfileobj(f1, f2)
    # Mark executable
    os.chmod(filename, os.stat(filename).st_mode | 64)
    print("done")


def clear_binaries_dir(target_dir):
    assert os.path.isdir(target_dir)
    for fname in os.listdir(target_dir):
        if fname != "README.md":
            print("Removing", fname, "...", end="")
            os.remove(os.path.join(target_dir, fname))
            print("done")
