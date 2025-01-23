import sys, json, subprocess, os, re
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("ncs_version")
args = parser.parse_args()
ncs_version = args.ncs_version


def get_toolchain_path(ncs_version: str) -> str | None:
    installed_toolchains = (
        json.loads(subprocess.run(["nrfutil", "toolchain-manager", "list", "--json"], capture_output=True).stdout)
        .get('data')
        .get('toolchains')
    )
    for toolchain in installed_toolchains:
        if ncs_version == toolchain.get('ncs_version'):
            return toolchain.get('path')


if os.environ.get('NCS_TOOLCHAIN_VERSION') == ncs_version:
    exit()
elif curr_ncs_toolchain := os.environ.get('NCS_TOOLCHAIN_VERSION'):
    curr_toolchain_path = get_toolchain_path(curr_ncs_toolchain)
else:
    curr_toolchain_path = None

toolchain_path = get_toolchain_path(ncs_version)
if not toolchain_path:
    exit()

with open(f'{toolchain_path}/environment.json', 'r') as f:
    environment = json.load(f).get('env_vars')

output_string = ''
for variable in environment:
    key = variable.get('key')
    match variable.get('type'):
        case 'relative_paths':
            paths = variable.get('values')
            paths_string = ":".join([f'{toolchain_path}/{path}' for path in paths])
            match variable.get('existing_value_treatment'):
                case 'prepend_to':
                    try:
                        curr_var = os.environ.pop(key)
                    except KeyError:
                        curr_var = ''
                    if curr_toolchain_path:
                        curr_var = re.sub(curr_toolchain_path + '/.+?:', '', curr_var)
                    output_string += f"\nexport {key}={paths_string}:{curr_var}"
                case 'overwrite':
                    output_string += f"\nexport {key}={paths_string}"
        case 'string':
            output_string += f"\nexport {key}={variable.get('value')}"

output_string += f"\nexport NCS_TOOLCHAIN_VERSION={ncs_version}"
sys.stdout.write(output_string)
