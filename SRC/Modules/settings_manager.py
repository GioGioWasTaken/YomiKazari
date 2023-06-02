# This module will handle reading and saving user settings for YomiKazari.
import json
class SettingsManager:
    def __init__(self,setting_file):
        self.setting_file=setting_file
        self.settings={}
    def load_settings(self):
        # This method will be responsible for loading the settings from a file
        # and storing them in the settings attribute.
        try:
            with open(self.settings_file, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {}
    def save_settings(self):
        # This method will save the current settings to a file.
        with open(self.setting_file,'w') as file:
            json.dump(self.settings, file)

    def get_setting(self, setting_name):
        # This method will retrieve the value of a specific setting.
        return self.settings.get(setting_name)
    def set_setting(self, setting_name, setting_value):
        # This method will update the value of a specific setting.
        self.settings[self.setting_name]=self.setting_value
    def reset_settings(self):
        # this method resets the settings
        self.settings={}