import os
import sys
import inspect
import subprocess
import importlib.util

# Direct import of package.py to avoid triggering hcli_problem_details __init__ during the build process
spec = importlib.util.spec_from_file_location(
    "package",
    os.path.join(os.path.dirname(__file__), "hcli_problem_details", "package.py")
)
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)

version = package.__version__

if sys.argv[-1] == 'dry-run':
    branch = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).strip().decode("utf-8")
    if branch != "master":
        sys.exit("dry-run from a branch other than master is disallowed.")
    os.system("pip uninstall -y hcli_problem_details")
    os.system("rm -rf requirements.txt")
    os.system("rm -rf hcli_problem_details.egg-info")
    os.system("rm -rf build")
    os.system("rm -rf dist")
    os.system("python -m build --sdist --wheel")
    os.system("twine check dist/*")
    os.system("pip install -e .")
    sys.exit()

if sys.argv[-1] == 'publish':
    branch = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).strip()
    if branch.decode('ASCII') != "master":
        sys.exit("publishing from a branch other than master is disallowed.")
    os.system("pip uninstall -y hcli_problem_details")
    os.system("rm -rf requirements.txt")
    os.system("rm -rf hcli_problem_details.egg-info")
    os.system("rm -rf build")
    os.system("rm -rf dist")
    os.system("python -m build --sdist --wheel")
    os.system("twine upload dist/* -r pypi")
    os.system("pip install -e .")
    os.system("git tag -a %s -m 'version %s'" % ("hcli_problem_details-" + version, "hcli_problem_details-" + version))
    os.system("git push")
    os.system("git push --tags")
    sys.exit()

if sys.argv[-1] == 'tag':
    branch = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).strip()
    if branch != "master":
        sys.exit("tagging from a branch other than master is disallowed.")
    os.system("git tag -a %s -m 'version %s'" % ("hcli_problem_details-" + version, "hcli_problem_details-" + version))
    sys.exit()
