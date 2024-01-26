# mkdocs-macros-adr-summary
![Static Badge](https://img.shields.io/badge/Python-3.8_%7C_3.9_%7C_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)
[![Stable Version](https://img.shields.io/pypi/v/mkdocs-macros-adr-summary?color=blue)](https://pypi.org/project/mkdocs-macros-adr-summary/)
[![stability-beta](https://img.shields.io/badge/stability-beta-33bbff.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#beta)

[![Python tests](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-tests.yml)
[![Bandit checks](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-bandit.yml/badge.svg?branch=main)](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-bandit.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/5631f62f6dcd3a34d7ae/maintainability)](https://codeclimate.com/github/febus982/mkdocs-macros-adr-summary/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5631f62f6dcd3a34d7ae/test_coverage)](https://codeclimate.com/github/febus982/mkdocs-macros-adr-summary/test_coverage)

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

This is a macro plugin to generates summaries from a list of a ADR documents in a directory.

Examples and documentation can be found [here](https://febus982.github.io/mkdocs-macros-adr-summary)

The package should be stable enough for daily use. I'll release 1.0.0, and switch to semantic version,
as soon as support for MADR version 2 has been implemented. Until that breaking changes can be introduced
and will be documented in the GitHub release description.

## Quick start

Enable the plugin in `mkdocs.yml`

```yaml
plugins:
  - macros:
        module_name: mkdocs_macros_adr_summary
```

Create a markdown page in your mkdocs website and use the `adr_summary` macro providing
the path containing your ADR files relative to the `mkdocs.yml` file.

```markdown
{{ adr_summary(adr_path="docs/adr", adr_style="nygard") }}
```

`adr_style` can be `nygard` or `MADR3`

## More customization

The page output is generated using a jinja template, but you can provide a custom one. The file path
must still be relative to the `mkdocs.yml` file.

```markdown
{{ adr_summary(adr_path="docs/adr", adr_style="MADR3", template_file="other.jinja") }}
```

The default template is:

```markdown
## Document list

{% for d in documents %}
* [{{ d.title }}]({{ d.filename }})
    * `{{ d.date.strftime('%d-%m-%Y') }}`
    * `{{ d.file_path }}`
    {% if d.statuses %}
    * Statuses:
        {% for status in d.statuses %}
        * {{ status }}
        {% endfor %}
    {% endif %}
{% endfor %}
```

The `documents` variable in the jinja template is a Sequence of `ADRDocument` models:

```python
@dataclass
class ADRDocument:
    file_path: str
    title: Optional[str] = None
    date: Optional[date] = None
    stasdetus: Optional[str] = None
    statuses: Sequence[str] = tuple()
    deciders: Optional[str] = None
    consulted: Optional[str] = None
    informed: Optional[str] = None
```

There are some differences in what metadata is available when using different formats:

|           | Nygard | MADR3 | MADR2 |
|-----------|--------|-------|-------|
| file_path | ✅︎     | ✅︎    | ✅︎    |
| title     | ✅︎     | ✅︎    | ✅︎    |
| date      | ✅︎     | ✅︎    | TODO  |
| status    | ⚠      | ✅︎    | TODO  |
| statuses  | ✅︎     | ⚠     | TODO  |
| deciders  | ❌      | ✅︎    | TODO  |
| consulted | ❌      | ✅︎    | TODO  |
| informed  | ❌      | ✅︎    | TODO  |

* **Nygard format**
  * `status` is the last item `statuses`. (I don't believe we should use multiple
    statuses, however `adr-tools` allows it)
  * `deciders`, `consulted` and `informed` are not supported by the format
* **MADR3**
  * I wasn't able to find an automated tool supporting superseding documents.
    By looking at the template it looks like there's a single status.
    `statuses` will return a list with a single status.

## Supported ADR formats

The supported ADR formats are:
* `nygard` format, it is recommended to use [adr-tools](https://github.com/npryce/adr-tools) to manage the directory
* `MADR` [version 3](https://github.com/adr/madr/blob/3.0.0/template/adr-template.md)

Support for [MADR](https://adr.github.io/madr/) version 2 will be added in a future version.

## Commands for development

All the common commands used during development can be run using make targets:

* `make dev-dependencies`: Install dev requirements
* `make update-dependencies`: Update dev requirements
* `make test`: Run test suite
* `make check`: Run tests, code style and lint checks
* `make fix`: Run code style and lint automatic fixes (where possible)
* `make docs`: Render the mkdocs website locally
