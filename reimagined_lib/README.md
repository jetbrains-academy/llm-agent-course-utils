# Auto Generation

> Reimagined is a mini-project designed AI-based automatization.
> It can be used for various tasks, including typings and docstrings generation, test generation, and more.

## Getting started

Note: In near future, reimagined will support Grazie API

Install the dependencies:
```bash
pip install -r requirements.txt
```

Choose configuration file in `conf/` folder and change it appropriately. \
On top of that, change `CONF_NAME` in `pipeline.py` to the name of your configuration file. \
*Note:* Without understanding the structure of the configuration, it is impossible to use the tool.

Launch the pipeline:
```bash
python pipeline.py
```

## Configuration

```yaml
root: /your/root/folder # root folder of the project (used to resolve relative paths)

template: ${root}/reimagined/templates/TEMPLATE_NAME.md # path to the template file

api:
  # API configuration
  type: openai
  key: ${oc.env:OPENAI_API_KEY}
  model: gpt-3.5-turbo

  extractor:  # Extractor configuration
    name: PythonCodeExtractor
    take_only: 0

repo: ${root}/data
inp:
  - file: ${repo}/main.py
    name: code
    extractor:
      name: ClassExtractor
      take_only: 0

out:
  file: ${repo}/test.py
```

Now, let's break down the configuration file.

### API

Currently, reimagined supports OpenAI API. \
You need to provide your API key and the model you want to use. \
Refer to the OpenAI API documentation for more information.

### Extractor

Extractor is a class that extracts the necessary information from the file or the API response (that is from some text).

Extractor usages:
- In API configuration: to extract the code (or whatever) from API response, and then write it to the output file.
- In input configuration: to extract the relevant information from the file (e.g. code, description), and then pass it to the template.

*Note 1:* Extractor always returns a list of strings. For this reason, one should use `take_only` parameter to take only the ith element. \
Yes, it's a bit inconvenient. \
*Note 2:* Extractor can be ommited. In this case, the whole content of file/response will be passed to the next step.

Extractor classes:
- `ClassExtractor`: extracts classes from python code.
Input:
```python
# some comment
import os

class A:
    pass

class B:
    pass
```
Extracted:
```python
[
    "class A:\n    pass",
    "class B:\n    pass"
]
```

- `DescriptionExtractor`: extracts descriptions from text (start token: `START_DESC`, end token: `END_DESC`).
Input:
```
some text
START_DESC
description
END_DESC
another text
```
Extracted:
```
[
    "description"
]
```
- `PythonCodeExtractor`: extracts python code from text (start token: ```python, end token: ``\`).

*Note:* You can create your own extractor by inheriting from `BaseExtractor` class.

### Template

Template is a markdown file with placeholders. For example:
```markdown
YOUR PROMT HERE

Description: {desc}
`` `python
{code}
`` `
```
Here, `code` and `desc` are placeholders to be filled in.

*Note 1:* You can create your own template in `reimagined/templates/` folder. \
*Note 2:* Beware of using `{` and `}` in the template. Sometimes, you want to escape them. In this case, use `{{` and `}}`.

### Input

You can think of input as a list of parameters to be passed to the template. \
Each parameter is an element of the `inp` list. \
It has to have the next attributes: `file` (path to the file), `name` (name of the parameter in the template), and `extractor` (contains the name of the extractor and `take_only` parameter). \
*Note:* If you want to omit the extractor, set `name` and `take_only` to `null`.

Example:
```yaml
inp:
    - file: ${repo}/main.py
        name: code
        extractor:
        name: ClassExtractor
        take_only: 1
    - file: ${repo}/description.txt
        name: desc
        extractor:
        name: DescriptionExtractor
        take_only: 0
```
This will produce the parameters like:
```python
{
    "code": "class B:\n    pass",
    "desc": "description"
}
```

*Note:* Use `VERBOSE=True` in `pipeline.py` to see the extracted information.

### Output

Output is a file where the result will be written. (simple as that)

## Additional information

* You can look in the `notebook.ipynb` to see an example how to use the tool over multiple files.

## Future plans

- Make `README.md` more informative.
- Add `Grazie` API support.

