# blog_ex.py
import yaml


def to_yaml(object):
    return yaml.dump(object)


def from_yaml(yaml_str):
    return yaml.load(yaml_str)


yaml_str = to_yaml({
    # Yes, this is some metadata about this blog ;)
    'layout': 'post',
    'title': 'Getting Started with Bandit',
    'date': '2017-01-16 10:00',
    'author': 'Ian Cordasco',
})
parsed_yaml = from_yaml(yaml_str)
#rishi
