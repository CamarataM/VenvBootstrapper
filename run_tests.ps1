# This file has a powershell section first followed by the bash section,
# as well as shared sections. But it is more complicated. Putting the
# the bash section first, followed by powershell, is simpler.
# ----------------------------------------------------------------------
echo @"
" > /dev/null ; echo > /dev/null <<"out-null" ###
"@ | out-null 
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# Powershell Start -----------------------------------------------------

$venv_bootstrapper_test_path = "./tests/venvbootstrapper.py"

if (Test-Path -Path $venv_bootstrapper_test_path) {
	$file = Get-Item -Path $venv_bootstrapper_test_path
	$file.IsReadOnly = $false
}

cp "./venvbootstrapper/venvbootstrapper.py" $venv_bootstrapper_test_path

if (Test-Path -Path $venv_bootstrapper_test_path) {
	$file = Get-Item -Path $venv_bootstrapper_test_path
	$file.IsReadOnly = $true
}

# Powershell End -------------------------------------------------------
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
out-null
echo @'
' > /dev/null
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# Bash Start -----------------------------------------------------------

# TODO: Untested
if [ -e "./tests/venv_bootstrapper.py" ] || [ -h "./tests/venv_bootstrapper.py" ]; then
	chmod a-w "./tests/venv_bootstrapper.py"
fi

cp "./venvbootstrapper/venv_bootstrapper.py" "./tests/venv_bootstrapper.py"

if [ -e "./tests/venv_bootstrapper.py" ] || [ -h "./tests/venv_bootstrapper.py" ]; then
	chmod a+w "./tests/venv_bootstrapper.py"
fi

# Bash End -------------------------------------------------------------
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
echo > /dev/null <<out-null
'@ | out-null
out-null
# ------------------------------------------------------

echo "Running import tests with vanilla Python:"
python "./tests/import_test.py"

echo ""

echo "Running download tests with vanilla Python:"
python "./tests/download_test.py"

echo "Required Version Check:"
poetry run vermin --eval-annotations -vv "venvbootstrapper"