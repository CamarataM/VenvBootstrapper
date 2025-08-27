#!/usr/bin/env python3
# Copyright (C) 2025 by CamarataM CamarataM@outlook.com
#
# Permission to use, copy, modify, and/or distribute this software for any purpose # with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH # REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND # FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, # INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS # OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER # TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF # THIS SOFTWARE.
import contextlib
import hashlib
import io
import logging
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import List
import venv

def _get_default_virtualenvs_path():
	return Path(Path.home(), '.virtualenvs').expanduser().resolve().absolute()

def _get_virtualenvs_path(use_script_directory_for_virtualenv_name : bool = False, virtualenvs_folder_path : str | os.PathLike | None = None):
	if virtualenvs_folder_path == None:
		virtualenvs_folder_path = _get_default_virtualenvs_path()

	script_file_path = Path(sys.argv[0]).expanduser().resolve().absolute()
	virtual_environment_base_name = script_file_path.parent.name if use_script_directory_for_virtualenv_name and script_file_path.parent != script_file_path else script_file_path.stem

	script_path_hashed_string : str = str(script_file_path.parent) if use_script_directory_for_virtualenv_name else str(script_file_path.parent)

	# usedforsecurity=False >=3.9
	try:
		virtual_environment_name = f'{virtual_environment_base_name}-{hashlib.sha256(script_path_hashed_string.encode(), usedforsecurity=False).hexdigest()[:8]}'
	except:
		virtual_environment_name = f'{virtual_environment_base_name}-{hashlib.sha256(script_path_hashed_string.encode()).hexdigest()[:8]}'

	return Path(Path(virtualenvs_folder_path), virtual_environment_name)

def _get_virtualenv_python_path(use_script_directory_for_virtualenv_name : bool = False, virtualenvs_folder_path : str | os.PathLike | None = None):
	python_executable_name : str

	platform_system = platform.system()
	if platform_system == "Windows":
		python_executable_name = 'python.exe'
	else:
		python_executable_name = 'python'

	return Path(_get_virtualenvs_path(use_script_directory_for_virtualenv_name=use_script_directory_for_virtualenv_name, virtualenvs_folder_path=virtualenvs_folder_path), 'Scripts', python_executable_name)

def download_venvbootstrapper(download_directory_path : str | os.PathLike | None = None):
	import urllib.request
	from pathlib import Path
	locals()['download_directory_path'] = Path(locals().get('download_directory_path', Path.cwd()))
	locals()['download_directory_path'].mkdir(parents=True, exist_ok=True)
	Path(locals()['download_directory_path'], 'venvbootstrapper.py').write_bytes(urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(fullurl='').read())

# Restarts the current script under the virtual environment if it is not already.
def create_and_activate_virtualenv(use_script_directory_for_virtualenv_name : bool = False, clear : bool = False, virtualenvs_folder_path : str | os.PathLike | None = None):
	virtual_environment_path = _get_virtualenvs_path(use_script_directory_for_virtualenv_name=use_script_directory_for_virtualenv_name, virtualenvs_folder_path=virtualenvs_folder_path)
	if not virtual_environment_path.exists():
		venv.EnvBuilder(clear=clear, with_pip=True).create(virtual_environment_path)

	virtual_environment_python_path = _get_virtualenv_python_path(use_script_directory_for_virtualenv_name=use_script_directory_for_virtualenv_name, virtualenvs_folder_path=virtualenvs_folder_path)
	if not virtual_environment_python_path.exists():
		raise NotImplementedError(f"Unsupported platform '{platform.system()}'.")

	current_python_path = Path(sys.executable)
	if current_python_path != virtual_environment_python_path:
		virtual_environment_python_path_string = str(virtual_environment_python_path.expanduser().resolve().absolute())

		exec_arguments = [virtual_environment_python_path_string] + sys.argv

		# os.execv will exit the parent process on Windows due to [this](https://github.com/python/cpython/issues/63323) bug meaning we need to use subprocess instead.
		if platform.system() == "Windows":
			# Catch KeyboardInterrupt to not print venv_bootstrapper's stacktrace.
			try:
				subprocess.run(exec_arguments)
			except KeyboardInterrupt:
				pass

			exit()
		else:
			os.execv(virtual_environment_python_path_string, exec_arguments)

def add(package_name : str, additional_pip_args : List[str] | None = None, silent : bool = True, activate_before_install : bool = True, use_script_directory_for_virtualenv_name : bool = False, clear : bool = False, virtualenvs_folder_path : str | os.PathLike | None = None):
	if virtualenvs_folder_path == None:
		virtualenvs_folder_path = _get_default_virtualenvs_path()

	if activate_before_install:
		create_and_activate_virtualenv(use_script_directory_for_virtualenv_name=use_script_directory_for_virtualenv_name, clear=clear, virtualenvs_folder_path=virtualenvs_folder_path)

	if Path(sys.executable).is_relative_to(virtualenvs_folder_path):
		# TODO: Since this is deprecated (but not likely for removal), should handle it's non-existence by using a subprocess solution which calls pip using the environments Python.
		from pip._internal import main as pip

		with io.StringIO() as stdout_capture:
			with io.StringIO() as stderr_capture:
				# Ensure we block any standard / error output from this block...
				with contextlib.redirect_stdout(stdout_capture) and contextlib.redirect_stderr(stderr_capture):
					# ...which doesn't include logging. This was the only solution which would work, as it doesn't seem like pip will have initialized it's loggers until it starts to call the function (which would be too late for us to interfere with). This excludes getting loggers using 'logging.root.manager.loggerDict' to disable them, as it will not find pip's loggers.
					previous_disable = logging.root.manager.disable
					if silent:
						logging.disable(sys.maxsize)

					# TODO: If not silent, logging will get output before stdout text which doesn't match default pip behaviour. Would have to swap default handlers out, then back in. This wouldn't be a problem if we used subprocess instead since it would all log to a captured pipe.
					return_code = pip(['install', package_name] + (additional_pip_args if additional_pip_args != None else []))

					stdout_capture.flush()
					stderr_capture.flush()

					caught_stdout = stderr_capture.getvalue()
					caught_stderr = stderr_capture.getvalue()

					if not silent:
						print(caught_stdout, sys.stdout)

					# TODO: More efficient matching method.
					if caught_stderr != None and 'WARNING: pip is being invoked by an old script wrapper.' not in caught_stderr:
						print(caught_stderr, file=sys.stderr)

					# Revert logging blocker to initial value.
					if silent:
						logging.disable(previous_disable)

					return return_code
	else:
		return 1