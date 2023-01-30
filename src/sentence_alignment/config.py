import os
import nltk


class LoadConfig:
    def __init__(self):
        self.nltk_download("punkt")
        self.set_laser_environment("/LASER")
        self.install_external_tools()
        self.install_models()

    def nltk_download(self, tokenizer_type):
        print(f"Downloading {tokenizer_type}...")
        nltk.download(tokenizer_type)

    def install_external_tools(self):
        if os.path.exists("./LASER/tools-external"):
            print("External Tools already exists, skipping installation...")
        else:
            print("Installing External Tools...")
            os.system("bash ./LASER/install_external_tools.sh")

    def install_models(self):
        print("Installing the Models...")
        os.system("bash ./LASER/install_models.sh")

    def set_laser_environment(self, laser_env):
        LASER_ENVIRON = os.getcwd() + laser_env
        print(f"Setting LASER environment to {LASER_ENVIRON}")
        os.environ["LASER"] = LASER_ENVIRON

    def download_models(self, language_mappings):
        models = ""
        for code in language_mappings:
            models += language_mappings[code] + " "

        print(f"Downloading(s) {models}...")
        os.system(f"bash ./LASER/nllb/download_models.sh {models}")
