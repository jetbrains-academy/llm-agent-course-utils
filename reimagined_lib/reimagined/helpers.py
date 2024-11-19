from omegaconf import OmegaConf
import os


DEFAULT_CONF_PATH = os.path.join(os.path.dirname(__file__), "../conf.yaml")
def get_config(path: str = DEFAULT_CONF_PATH) -> OmegaConf:
    """Get the configuration from the YAML file."""
    conf_raw = OmegaConf.load(path)
    conf = OmegaConf.create(OmegaConf.to_yaml(conf_raw, resolve=True))
    return conf