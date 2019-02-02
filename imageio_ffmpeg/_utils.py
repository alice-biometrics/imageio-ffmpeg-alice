import os
import sys
import subprocess
import logging

from ._definitions import get_platform, SUFFIX_PER_PLATFORM

LIB_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger("imageio_ffmpeg")


def get_ffmpeg_exe():
    """ Get the ffmpeg executable file.
    """
    # Try ffmpeg exe in order of priority.

    # 1. Try environment variable.
    exe = os.getenv("IMAGEIO_FFMPEG_EXE", None)
    if exe:
        return exe

    plat = get_platform()

    # 2. Try from here
    exe = os.path.join(
        LIB_DIR, "binaries", "ffmpeg-" + SUFFIX_PER_PLATFORM.get(plat, "")
    )
    if exe and os.path.isfile(exe):
        return exe

    # 3. Try binary from conda package
    # (installed e.g. via `conda install ffmpeg -c conda-forge`)
    if plat.startswith("win"):
        exe = os.path.join(sys.prefix, "Library", "bin", "ffmpeg.exe")
    else:
        exe = os.path.join(sys.prefix, "bin", "ffmpeg")
    if exe and os.path.isfile(exe):
        try:
            with open(os.devnull, "w") as null:
                subprocess.check_call(
                    [exe, "-version"], stdout=null, stderr=subprocess.STDOUT
                )
                return exe
        except (OSError, ValueError, subprocess.CalledProcessError):
            pass

    # 4. Try system ffmpeg command
    exe = "ffmpeg"
    try:
        with open(os.devnull, "w") as null:
            subprocess.check_call(
                [exe, "-version"], stdout=null, stderr=subprocess.STDOUT
            )
            return exe
    except (OSError, ValueError, subprocess.CalledProcessError):
        pass

    # Nothing was found
    raise RuntimeError(
        "ffmpeg exe not found. Install ffmpeg and/or set IMAGEIO_FFMPEG_EXE."
    )


def get_ffmpeg_version():
    """ Get the version of the used ffmpeg executable (as a string).
    """
    exe = get_ffmpeg_exe()
    line = subprocess.check_output([exe, "-version"]).split(b"\n", 1)[0]
    line = line.decode(errors='ignore').strip()
    version = line.split("version", 1)[-1].lstrip().split(" ", 1)[0].strip()
    return version