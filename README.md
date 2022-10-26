# Tools for managing Courses

A collection of tools for managing courses run by Instil.

There is only one tool right now:

## `makerepo`

Given a template file defined in .ini format, copy files and folders from the 
training repository into the current directory, so they can be published as a
separate repository (typically on Space).

```shell
makerepo typescript-react
```

## Installation instructions

This is a python application which should be installable via pip, or pipx.

To install it as an editable package, make a virtualenv then install this via
pip, i.e.

```shell
python -m venv .venv
pip install -e .

makerepo -l # Should list available templates
```

You should also be able to do

```shell
pipx install git+ssh//git@github.com:instil/coursetools.git
```

## Configuration

You'll need to add a config file (it won't create it for you yet).

Put it at `~/.coursetools/config.ini` and put this content in it:

```ini
[config]
repo_root = /Users/ryan/Projects/training-repo
```