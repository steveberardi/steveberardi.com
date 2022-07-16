import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_PATH_ROOT = "src/templates"

"""
    Looks at source path for two directories:
        static
        templates
    
    1. Walks the templates directory and renders all index.html

        Examples:
            src/index.html -> build/index.html
            src/about/index.html -> build/about/index.html
            src/base.html -> No build file

    2. Copies all files in static
    
        Examples:
            src/static/bundle.js -> build/bundle.js
            src/static/css/style.css -> build/css/style.css

"""

env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH_ROOT),
    autoescape=select_autoescape()
)

def walk_templates(path=TEMPLATE_PATH_ROOT, index_filename='index.html'):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith(index_filename):
                p = Path(os.path.join(dirpath, filename))
                yield p.relative_to(path).parent

# Render Templates
for template_path in walk_templates():
    template = env.get_template(str(template_path / "index.html"))

    build_path = Path(f"build/{template_path}")
    build_path.mkdir(parents=True, exist_ok=True)
    
    build_filename = build_path / "index.html"

    with open(build_filename, "w") as build_file:
        build_file.write(template.render())
    
    print(f"Built page: {template_path}")


# Copy Static Files
shutil.copytree("src/static", "build", dirs_exist_ok=True)
