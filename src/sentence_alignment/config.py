import os, subprocess, nltk
from pathlib import Path


LASER_PATH = Path(Path(os.path.abspath(__file__)).parent / 'LASER') # path to LASER module

def set_environ_var():
    """
    ### Sets enviroment variables for use within the LASER module
    """
    os.environ['LASER'] = str(LASER_PATH)
    os.environ['LC_ALL']='C.UTF-8'
    os.environ['LANG']='C.UTF-8'

def setup_laser():
    """
    ### Downloads configs for LASER repo
    """
    print('Setting Up LASER module...')
    if (os.path.exists(f'{LASER_PATH}/models')):
        print('LASER/models dir found, skipping installation, delete folders for and run script again for fresh installation')
    else: 
        command = f'bash {LASER_PATH}/install_models.sh'
        subprocess.run(command, shell=True)
        
    if (os.path.exists(f'{LASER_PATH}/tools-external')):
        print('LASER/tools-external dir found, skipping installation, delete folders for and run script again for fresh installation')
    else: 
        command = f'bash {LASER_PATH}/install_external_tools.sh'
        subprocess.run(command, shell=True)
    print('LASER module configured.')


def download_laser_models(lang_mappings):
    """
    ### Downloads language models to perform sentence encoding
    #### Params:
        -   lang_mappings: a dictionary mapping langs to LASER models, eg. 'xho -> xho_Latn`. (dict)
    """
    print('Downloading LASER models...')
    command = f'bash {LASER_PATH}/nllb/download_models.sh'
    for _,val in lang_mappings.items():
        command = "{} {}".format(command, val)
    subprocess.run(command, shell=True)
    print('Models downloaded.')


def download_tokeniser() -> None:
    print('Downloading NLTK tokeniser...')
    nltk.download('punkt')
    print('NLTK tokeniser downloaded')