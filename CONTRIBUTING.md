# How to contribute

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

Contributions are welcome from anyone, including those outside of NI.

## 🐛 Filing a Bug Report 🐛

Bugs are tracked as [GitHub Issues](https://github.com/ni/python-styleguide/issues)

Before submitting a bug report, [perform a search](https://github.com/ni/python-styleguide/issues) to see if the problem has already been reported.
When you are creating a bug report, please fill out the pre-populated template and include as many details as possible.

## 📝 Making a Code Contribution 📝

All code contributions should be in the form of [Pull Requests](https://guides.github.com/activities/forking/).

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in the template
1. Follow the styleguide
1. After you submit your pull request, verify that all status checks are passing

## ⭐️ Common Contributing Workflows ⭐️

## Install Git `pre-commit` Hook Scripts

This project uses [pre-commit](https://pre-commit.com/) to automatically run checks
when you commit changes to the code. Install the `pre-commit` hook scripts in
your local copy of the repo by running:

```cmd
poetry run pre-commit install
```

### Adding a new plugin

If you want to add a plugin to the list of plugins, here's how:

1. Run `poetry add <plugin_name>` to add it to the dependencies, virtual environment, and lock file
1. Edit `ni_python_styleguide/flakehell_config.toml` with any additional configuration settings needed

### Editing the conventions

The conventions (`docs/Coding-Conventions.md`) are in Markdown and follow a pattern:

- Sections are given a single letter and a name (E.g. "F" and "Formatting")
- Subsections are divided into logical groups, and use the section's letter, an
  incrementing number, and a name.
- Conventions themselves go underneath subsections, and use the subsection's letter/number,
  an additionally incrementing number, and the convention title.

The conventions are also hosted on GitHub Pages: https://ni.github.io/ni-python-styleguide/

If you want to see how your changes will look on the hosted version or make changes to
it, you can serve it locally by following [these steps](https://docs.github.com/en/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll).
(NOTE: The pages are served out of the `docs` directory, so you will need to `cd` to it before serving)

NOTE: There can be a delay between changes going into the `master` branch and
GitHub Pages rebuilding with the changes.

## Releasing

The version checked into source is kept in an alpha state until we are ready to release. The release workflow automatically increments the version to a non-alpha version when a GitHub Release is created, and then moves to the next alpha afterwards.

The release process is as follows:

1. Check the version located in [pyproject.toml](https://github.com/ni/python-styleguide/blob/main/pyproject.toml).
1. Create a [new release](https://github.com/ni/python-styleguide/releases/new) with the appropriate description.
1. Use the current version to specify the git tag. (remove the alpha part) (v1.0.0).
1. Publish the release.

Once this is released, it should show up on https://pypi.org/project/ni-python-styleguide/.

### Manually Setting Version

The Poetry verison can be manually overridden through `poetry version` commands. The version checked into source should be in an alpha state.

In a fork:

1. Run `poetry version preminor` for minor update (v0.1.7-alpha.0 -> v0.2.0-alpha.0).
1. Run `poetry version premajor` for major update (v0.6.7-alpha.0 -> v1.0.0-alpha.0).
1. Merge the fork and complete the normal release process above.
