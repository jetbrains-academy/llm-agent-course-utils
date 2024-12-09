# Scripts

> Collection of scripts to automate tasks.


### Autoflake

Remove unused imports from a python file.
```bash
autoflake --ignore-pass-after-docstring --in-place --remove-all-unused-imports --ignore-init-module-imports -r folder/
```
Additional option: `--remove-unused-variables` \
Note: autoflake removes `pass` statements that don't follow a docstings (use git diff to check changes)

### Smart Freeze