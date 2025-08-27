#!/usr/bin/env python3
from pathlib import Path
import sys
import tempfile
from venvbootstrapper import download_venvbootstrapper

def main():
	download_directory_path = Path(tempfile.gettempdir(), 'venvbootstrappertests')

	download_venvbootstrapper(download_directory_path=download_directory_path)
	assert Path(download_directory_path, 'venvbootstrapper.py').exists(), f"Function Path({download_directory_path}, 'venvbootstrapper.py').exists() == False"

	Path(download_directory_path, 'venvbootstrapper.py').unlink()

	(lambda urllib: (lambda _mod: (lambda Path: [[locals()['download_directory_path'].mkdir(parents=True, exist_ok=True), Path(locals()['download_directory_path'], 'venvbootstrapper.py').write_bytes(urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(fullurl='https://raw.githubusercontent.com/CamarataM/VenvBootstrapper/refs/heads/main/venvbootstrapper/venvbootstrapper.py').read())][-1] for locals()['download_directory_path'] in [Path(locals().get('download_directory_path', Path.cwd()))]][0])(_mod.Path))(__import__('pathlib', {}, {}, ['Path'])))(__import__('urllib.request'))
	assert Path(Path.cwd(), 'venvbootstrapper.py').exists(), f"One-Liner Path({Path.cwd()}, 'venvbootstrapper.py').exists() == False"

	Path(Path.cwd(), 'venvbootstrapper.py').unlink()

	print("Passed All Tests")

	return 0

if __name__ == '__main__':
	sys.exit(main())