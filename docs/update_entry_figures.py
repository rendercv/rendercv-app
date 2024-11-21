"""This script generates the example entry figures and creates an environment for
documentation templates using `mkdocs-macros-plugin`. For example, the content of the
example entries found in
"[Structure of the YAML Input File](https://docs.rendercv.com/user_guide/structure_of_the_yaml_input_file/)"
are coming from this script.
"""

import io
import pathlib

import pydantic
import ruamel.yaml

import rendercv.data as data
import rendercv.renderer as renderer

repository_root = pathlib.Path(__file__).parent.parent
rendercv_path = repository_root / "rendercv"
image_assets_directory = pathlib.Path(__file__).parent / "assets" / "images"


class SampleEntries(pydantic.BaseModel):
    education_entry: data.EducationEntry
    experience_entry: data.ExperienceEntry
    normal_entry: data.NormalEntry
    publication_entry: data.PublicationEntry
    one_line_entry: data.OneLineEntry
    bullet_entry: data.BulletEntry
    text_entry: str


def dictionary_to_yaml(dictionary: dict):
    """Converts a dictionary to a YAML string.

    Args:
        dictionary: The dictionary to be converted to YAML.
    Returns:
        The YAML string.
    """
    yaml_object = ruamel.yaml.YAML()
    yaml_object.width = 60
    yaml_object.indent(mapping=2, sequence=4, offset=2)
    with io.StringIO() as string_stream:
        yaml_object.dump(dictionary, string_stream)
        yaml_string = string_stream.getvalue()
    return yaml_string


def define_env(env):
    # See https://mkdocs-macros-plugin.readthedocs.io/en/latest/macros/
    sample_entries = data.read_a_yaml_file(
        repository_root / "docs" / "sample_entries.yaml"
    )
    # validate the parsed dictionary by creating an instance of SampleEntries:
    SampleEntries(**sample_entries)

    entries_showcase = dict()
    for entry_name, entry in sample_entries.items():
        proper_entry_name = entry_name.replace("_", " ").title().replace(" ", "")
        entries_showcase[proper_entry_name] = {
            "yaml": dictionary_to_yaml(entry),
            "figures": [
                {
                    "path": f"../assets/images/{theme}/{entry_name}.png",
                    "alt_text": f"{proper_entry_name} in {theme}",
                    "theme": theme,
                }
                for theme in data.available_themes
            ],
        }

    env.variables["showcase_entries"] = entries_showcase

    # Available themes strings (put available themes between ``)
    themes = [f"`{theme}`" for theme in data.available_themes]
    env.variables["available_themes"] = ", ".join(themes)

    # Available social networks strings (put available social networks between ``)
    social_networks = [
        f"`{social_network}`" for social_network in data.available_social_networks
    ]
    env.variables["available_social_networks"] = ", ".join(social_networks)
