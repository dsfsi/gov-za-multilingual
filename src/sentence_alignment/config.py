import os
import subprocess
import sys

import nltk

LASER_PATH = os.path.join(os.getcwd(), 'LASER')  # path to LASER module


def validate_python_version():
    """
    ### Validates that Python 3.8 is being used (required for fairseq)
    """
    version_info = sys.version_info
    if version_info[:2] != (3, 8):
        raise RuntimeError(
            f"Python 3.8 is required for sentence alignment (fairseq compatibility).\n"
            f"Current version: {version_info.major}.{version_info.minor}\n"
            f"Please switch to Python 3.8 using pyenv or your version manager."
        )


def validate_laser_setup():
    """
    ### Validates that LASER has been properly set up
    """
    if not os.path.exists(LASER_PATH):
        raise RuntimeError(
            f"LASER directory not found at {LASER_PATH}\n"
            f"Please ensure you're running from src/sentence_alignment/ directory"
        )

    models_path = os.path.join(LASER_PATH, 'models')
    tools_path = os.path.join(LASER_PATH, 'tools-external')

    missing = []
    if not os.path.exists(models_path):
        missing.append("models/")
    if not os.path.exists(tools_path):
        missing.append("tools-external/")

    if missing:
        print(f"⚠️  WARNING: LASER setup incomplete. Missing: {', '.join(missing)}")
        print("   These will be downloaded during setup_laser()")


def set_environ_var():
    """
    ### Sets environment variables for use within the LASER module
    """
    validate_python_version()
    validate_laser_setup()

    os.environ['LASER'] = str(LASER_PATH)
    os.environ['LC_ALL'] = 'C.UTF-8'
    os.environ['LANG'] = 'C.UTF-8'


def setup_laser():
    """
    ### Downloads configs for LASER repo
    """
    print('Setting up LASER module...')

    models_path = os.path.join(LASER_PATH, 'models')
    tools_path = os.path.join(LASER_PATH, 'tools-external')

    if os.path.exists(models_path):
        print('✓ LASER/models directory found, skipping installation.')
    else:
        print('Downloading LASER models...')
        install_script = os.path.join(LASER_PATH, "install_models.sh")
        if not os.path.exists(install_script):
            raise FileNotFoundError(
                f"install_models.sh not found at {install_script}\n"
                f"Please ensure LASER submodule is properly initialized"
            )
        result = subprocess.run(f'bash {install_script}', shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to install LASER models:\n{result.stderr}")
        print('✓ LASER models installed')

    if os.path.exists(tools_path):
        print('✓ LASER/tools-external directory found, skipping installation.')
    else:
        print('Downloading LASER external tools...')
        tools_script = os.path.join(LASER_PATH, "install_external_tools.sh")
        if not os.path.exists(tools_script):
            raise FileNotFoundError(
                f"install_external_tools.sh not found at {tools_script}\n"
                f"Please ensure LASER submodule is properly initialized"
            )
        result = subprocess.run(f'bash {tools_script}', shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to install external tools:\n{result.stderr}")
        print('✓ LASER external tools installed')

    print('✓ LASER module configured.')


def download_laser_models(lang_mappings):
    """
    ### Downloads language models to perform sentence encoding
    #### Params:
        -   lang_mappings: a dictionary mapping langs to LASER models, eg. 'xho -> xho_Latn`. (dict)
    """
    print('Downloading LASER language-specific models...')
    download_script = os.path.join(LASER_PATH, "nllb", "download_models.sh")

    if not os.path.exists(download_script):
        raise FileNotFoundError(
            f"download_models.sh not found at {download_script}\n"
            f"Please ensure LASER is properly set up"
        )

    command = f'bash {download_script}'
    for _, val in lang_mappings.items():
        if val:  # Only add non-empty model names
            command = '{} {}'.format(command, val)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to download LASER models:\n{result.stderr}")

    print('✓ Language models downloaded.')


def download_tokeniser() -> None:
    print('Downloading NLTK tokeniser...')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    print('NLTK tokeniser downloaded')
