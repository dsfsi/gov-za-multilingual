import os
import nltk


class LoadConfig:
    def __init__(self):
        self.nltk_download("punkt")
        self.set_laser_environment(os.getcwd())
        self.install_external_tools()
        self.install_models()

    def nltk_download(self, tokenizer_type):
        print(f"Downloading {tokenizer_type}...")
        nltk.download(tokenizer_type)

    def install_external_tools(self):
        if os.path.exists("./tools-external"):
            print("External Tools already exists, skipping installation...")
        else:
            print("Installing External Tools...")
            os.system("bash ./install_external_tools.sh")

    def install_models(self):
        print("Installing the Models...")
        os.system("bash ./install_models.sh")

    def set_laser_environment(self, laser_env):
        print(f"Setting LASER environment to {laser_env}")
        os.environ["LASER"] = laser_env

    def download_models(self, language_mappings):
        models = ""
        for code in language_mappings:
            models += language_mappings[code] + " "

        print(f"Downloading(s) {models}...")
        os.system(f"bash ./nllb/download_models.sh {models}")
