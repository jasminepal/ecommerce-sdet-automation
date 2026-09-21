import yaml

class DataReader:
    
    def __init__(self, file_path):
        self.file_path = file_path
        
    def read_data(self):
        with open(self.file_path, "r") as file:
            return yaml.safe_load(file)
        
        
        