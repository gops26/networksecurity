import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import yaml

def read_yaml_file(filepath):
    try:
        with open(filepath, 'rb') as yaml_content:
            return yaml.safe_load(yaml_content)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(savepath:str, content:object, replace:bool=False)-> None:
    try:
        if replace:
            if os.path.exists(savepath): os.remove(savepath)
        os.makedirs(os.path.dirname(savepath), exist_ok=True)
        with open(savepath, "wb") as file:
            yaml.safe_dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
