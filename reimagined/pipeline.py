from typing import Any, Dict
from reimagined.helpers import get_config
from reimagined.prompting.content_extractor import get_extractor_by_name
from reimagined.prompting.prompter import Prompter
from reimagined.api import get_api_class_by_name, APIBase
from omegaconf import OmegaConf
from pprint import pprint

VERBOSE = True
CONF_NAME = "conf_tmp.yaml"

def load_config() -> OmegaConf:
    """Load and return configuration."""
    conf = get_config() if CONF_NAME is None else get_config(CONF_NAME)
    if VERBOSE:
        pprint(dict(conf))
    return conf

def read_file(path: str) -> str:
    """Read and return file content."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    """Write content to file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_param(file_info: OmegaConf) -> str:
    """Extract parameter from file based on configuration."""
    data = read_file(file_info.file)
    if file_info.get("extractor", None) is None or file_info.extractor.get("name", None) is None:
        return data
    extractor = get_extractor_by_name(file_info.extractor.name)
    return extractor.extract(data)[file_info.extractor.take_only]

def collect_params(inp_info: OmegaConf) -> Dict[str, str]:
    """Collect parameters from multiple input configurations."""
    return {info.name: extract_param(info) for info in inp_info}

def create_prompter(conf: OmegaConf) -> Prompter:
    """Initialize and return a Prompter with template."""
    template = read_file(conf.template)
    return Prompter(template)

def initialize_api(api_conf: OmegaConf) -> APIBase:
    """Initialize and return the API client."""
    api_cls = get_api_class_by_name(api_conf.type)
    return api_cls(model=api_conf.model, token=api_conf.key)

def process_response(response: str, api_conf: OmegaConf) -> str:
    """Process and extract relevant data from API response."""
    extractor = get_extractor_by_name(api_conf.extractor.name)
    return extractor.extract(response)[api_conf.extractor.take_only]

def main() -> None:
    """Main function to execute the pipeline."""
    conf = load_config()
    params = collect_params(conf.inp)
    if VERBOSE:
        print("Collected parameters:")
        pprint(params)
    
    prompter = create_prompter(conf)
    prompt = prompter.prompt(**params)
    
    api = initialize_api(conf.api)
    response = api.query(prompt)
    response_processed = process_response(response, conf.api)
    
    if VERBOSE:
        print("Response (after processing):")
        print(response_processed)
    
    write_file(conf.out.file, response_processed)

if __name__ == "__main__":
    main()
