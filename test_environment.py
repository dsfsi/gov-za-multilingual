import sys

REQUIRED_PYTHON = "python3"
REQUIRED_VERSION = (3, 8)  # Python 3.8 required for fairseq compatibility


def main():
    system_major = sys.version_info.major
    system_version = sys.version_info[:2]

    if REQUIRED_PYTHON == "python":
        required_major = 2
    elif REQUIRED_PYTHON == "python3":
        required_major = 3
    else:
        raise ValueError("Unrecognized python interpreter: {}".format(
            REQUIRED_PYTHON))

    if system_major != required_major:
        raise TypeError(
            "This project requires Python {}. Found: Python {}".format(
                required_major, sys.version))

    # Check for specific version (3.8) required by sentence alignment
    if system_version != REQUIRED_VERSION:
        print(">>> WARNING: Python {}.{} detected".format(*system_version))
        print(">>> Sentence alignment requires Python {}.{} (fairseq compatibility)".format(*REQUIRED_VERSION))
        print(">>> Scraping will work, but sentence alignment may fail")
        print(">>> Consider using pyenv to install Python {}.{}".format(*REQUIRED_VERSION))
    else:
        print(">>> Python {}.{} detected - Perfect!".format(*system_version))
        print(">>> Development environment passes all tests!")


if __name__ == '__main__':
    main()
