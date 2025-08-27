# VenvBootstrapper History
Originally, I needed a way to share Python scripts for helping the build process of our game without the need of dependency management programs like [Poetry](https://python-poetry.org/), my preferred dependency manager.

My first attempt at solving this was by parsing the metadata for packages using the [PyPi Index API](https://docs.pypi.org/api/index-api/) and manually downloading and extracting the package to a relative location, then importing the modules manually using [importlib](https://docs.python.org/3/library/importlib.html).

This was extremely error prone, but did work for simple modules. However, for any modules which included OS-native libraries such as DLL's of .pyd files, I was incapable of getting those to work correctly. This eventually lead me to scrap the entire project as using virtual environments is not only the right way to do things, but is also much, much simpler than my original solution.