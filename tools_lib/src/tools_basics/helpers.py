import numpy as np
import os
from omegaconf import OmegaConf
from typing import Iterable

def get_config(path: str) -> OmegaConf:
    """Get the configuration from the YAML file.
    Set `root_dir` to the directory of the config file.
    
    Note: The function expects the conf.yaml file to be in the root of the project."""
    conf_raw = OmegaConf.load(path)
    root_dir = os.path.dirname(path)
    conf_raw.root_dir = os.path.abspath(root_dir)
    conf = OmegaConf.create(OmegaConf.to_yaml(conf_raw, resolve=True))
    return conf

def save_as_numpy(data: Iterable, path: str) -> None:
    """Save the data as a NumPy file."""
    np.save(path, np.array(data))