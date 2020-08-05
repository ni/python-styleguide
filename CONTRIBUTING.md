# How to contribute

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

Contributions are welcome from anyone, including those outside of NI.

## 🐛 Filing a Bug Report 🐛

Bugs are tracked as [GitHub Issues](https://github.com/ni/ni-python-styleguide/issues)

Before submitting a bug report, [perform a search](https://github.com/ni/ni-python-styleguide/issues) to see if the problem has already been reported.
When you are creating a bug report, please fill out the pre-populated template and include as many details as possible.

## 📝 Making a Code Contribution 📝

All code contributions should be in the form of [Pull Requests](https://guides.github.com/activities/forking/).

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in the template
1. Follow the styleguide
1. After you submit your pull request, verify that all status checks are passing

## ⭐️ Common Contributing Workflows ⭐️

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
