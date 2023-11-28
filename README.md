# pydkit

[![Release](https://img.shields.io/github/v/release/manimozaffar/pydkit)](https://img.shields.io/github/v/release/manimozaffar/pydkit)
[![Build status](https://img.shields.io/github/actions/workflow/status/manimozaffar/pydkit/main.yml?branch=main)](https://github.com/manimozaffar/pydkit/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/manimozaffar/pydkit/branch/main/graph/badge.svg)](https://codecov.io/gh/manimozaffar/pydkit)
[![Commit activity](https://img.shields.io/github/commit-activity/m/manimozaffar/pydkit)](https://img.shields.io/github/commit-activity/m/manimozaffar/pydkit)
[![License](https://img.shields.io/github/license/manimozaffar/pydkit)](https://img.shields.io/github/license/manimozaffar/pydkit)

Extended kit and tools for pydantic, to enjoy pydantic even more!

- **Github repository**: <https://github.com/manimozaffar/pydkit/>
- **Documentation** <https://manimozaffar.github.io/pydkit/>

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

``` bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:manimozaffar/pydkit.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project! The CI/CD
pipeline will be triggered when you open a pull request, merge to main,
or when you create a new release.

To finalize the set-up for publishing to PyPi or Artifactory, see
[here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see
[here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).

## Releasing a new version

- Create an API Token on [Pypi](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting
[this page](https://github.com/manimozaffar/pydkit/settings/secrets/actions/new).
- Create a [new release](https://github.com/manimozaffar/pydkit/releases/new) on Github.
Create a new tag in the form ``*.*.*``.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).