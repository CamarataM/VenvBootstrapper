# VenvBootstrapper
**VenvBootstrapper** provides methods to automatically create, install, and activate a Python virtual environment using [venv](https://docs.python.org/3/library/venv.html). This allows for easily installing and using external packages without the need of additional files such as [requirements.txt](https://pip.pypa.io/en/stable/reference/requirements-file-format/) or user knowledge on how to use virtual environments.

In additional, using a download method listed below either as a Python method or one-liner, VenvBootstrapper can automatically be downloaded and used allow for single-file Python scripts to be easily distributed.

## Q/A
### Why Not *[Pipenv](https://pipenv.pypa.io/en/latest/)*, *[Poetry](https://python-poetry.org/docs/)*, *[Hatch](https://hatch.pypa.io/latest/)*, *[Conda](https://docs.conda.io/projects/conda/en/latest/index.html)*, *[UV](https://docs.astral.sh/uv/)*, *[PDM](https://pdm-project.org/en/latest/)*, *[Huak](https://cnpryer.github.io/huak/)* or Any Other Similar Tool?
VenvBootstrapper excels at having a single entry-point for the program which requires no prior knowledge of the complicated world of Python packages or dependency managers.

Since everything can be self-contained in one file using a minimal download method embedded in your original script, distribution and usage is as simple as running the Python file with a vanilla Python file and a virtual environment will automatically be created and used with the packages declared by your script.

### What Are Some Potential Use-Cases for VenvBootstrapper?
- **Utility Scripts**: VenvBootstrapper is uniquely suited to utility scripts for other projects, especially if those projects are shared. For example, my use-case is for generating code dynamically in a game-development project where other members might not have either the technical knowledge or a valid installation of a dependency manager, but do have the knowledge of how to run vanilla Python scripts.
- **Locked-Down Systems**: In systems where additional software cannot be installed (such as a dedicated dependency manager), VenvBootstrapper allows for the usage of 3rd-party packages without requiring any additional software other than a vanilla Python installation. These situations most commonly arise when using educational or business devices.

### How Does It Work?
Once imported into your script, three methods are publicly exposed, being `download_venvbootstrapper(...)`, `create_and_activate_virtualenv(...)`, `add(...)`. When `create_and_activate_virtualenv(...)` or `add(...)` is called, a virtual environment is searched for with the name being a combination of either the script name or the directory name (depending on arguments) and a hash of the absolute path to the running script. If not found, it is created, then the script is re-run with the virtual environment's Python, passing along all arguments of the original execution of the script, allowing access to either the currently installed packages of the virtual environment or any added using the `add(...)` method.

**Note**: Since VenvBootstrapper restarts the original script, no guarantees are made that the PID of the original process will remain in-tact and alive, so external functionality which depends on the PID of the original may not function correctly.

## Usage Examples
To use, simply download `venvbootstrapper.py` and put it next to your own Python script. Then, import VenvBootstrapper:
```python
from venvbootstrapper import add
```

Finally, call `add(...)`, passing the package source as the first parameter. Some examples of adding some popular packages are as follows:
```python
add('requests')
add('orjson')
add('opencv-python')
```

**Note**: The `add(...)` calls need to be **above** the import statements for the packages (e.g. `import requests`) to be able to be imported correctly.

While `create_and_activate_virtualenv(...)` can be used directly, it is **strongly recommended** to use `add(...)` instead as it will automatically handle the creation and activation of the virtual environment. Simply pass the package name and/or requirement string to the `add(...)` function and the creation and activation of the virtual environment will happen automatically.

## Download Methods
### Python Method (also in `venvbootstrapper.py`)
```python
def download_venvbootstrapper(download_directory_path : str | os.PathLike | None = None):
	import urllib.request
	from pathlib import Path
	locals()['download_directory_path'] = Path(locals().get('download_directory_path', Path.cwd()))
	locals()['download_directory_path'].mkdir(parents=True, exist_ok=True)
	Path(locals()['download_directory_path'], 'venvbootstrapper.py').write_bytes(urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(fullurl='https://raw.githubusercontent.com/CamarataM/VenvBootstrapper/refs/heads/main/venvbootstrapper/venvbootstrapper.py').read())
```

### Python Method One-Liner (generated using [Flatliner](https://github.com/hhc97/flatliner-src))
```python
(lambda urllib: (lambda _mod: (lambda Path: [[locals()['download_directory_path'].mkdir(parents=True, exist_ok=True), Path(locals()['download_directory_path'], 'venvbootstrapper.py').write_bytes(urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(fullurl='https://raw.githubusercontent.com/CamarataM/VenvBootstrapper/refs/heads/main/venvbootstrapper/venvbootstrapper.py').read())][-1] for locals()['download_directory_path'] in [Path(locals().get('download_directory_path', Path.cwd()))]][0])(_mod.Path))(__import__('pathlib', {}, {}, ['Path'])))(__import__('urllib.request'))
```

### Via [GitHub Releases](https://github.com/CamarataM/VenvBootstrapper/releases/latest)

### Via [GitHub Source Code](https://github.com/CamarataM/VenvBootstrapper/blob/main/venvbootstrapper/venvbootstrapper.py)

## License
`venvbootstrapper.py` is licensed under the [Zero Clause BSD license](https://landley.net/toybox/license.html), meaning you may use it however you like with/without attribution **as long as you agree to waive any liability of the original authors for any damage the software may cause**.

The code inside `tests` and `utilities` is licensed under the [MIT license](https://opensource.org/license/MIT).

COPYRIGHT.txt generated using [CopyrightGenerator](https://github.com/CamarataM/CopyrightGenerator).

## Contributing
Opening issues and flagging bugs are welcomed and encouraged. I will try to be receptive of feedback and incorporate changes when necessary.

Small, trivial patches ([<15 lines of code](https://www.gnu.org/prep/maintain/maintain.html#Legally-Significant)) are welcome, although past that I cannot guarantee patches will be accepted as I have not yet found a proper mechanism / CLA for 0BSD that doesn't encumber / burden active development of the project.

## Related Projects
- [auto_venv](https://github.com/amal-khailtash/auto_venv)