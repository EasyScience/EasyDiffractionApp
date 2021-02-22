import os, sys
import toml


def config():
    project_fname = 'pyproject.toml'
    current_path = os.path.dirname(__file__)
    project_fpath = os.path.join(current_path, project_fname)
    return toml.load(project_fpath)

def keyPath():
    if len(sys.argv) < 2:
        return ''
    return sys.argv[1]

def getValue(d, element):
    keys = element.split('.')
    keys[-1] = keys[-1].split('-')[0] # macos-latest -> macos, etc.
    rv = d
    for key in keys:
        rv = rv[key]
    return rv

if __name__ == "__main__":
    config = config()
    key_path = keyPath()
    value = getValue(config, key_path)
    print(value)
