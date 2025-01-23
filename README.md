# nrfutil toolchain selector

Tool for using a nRF Connect SDK toolchain managed by nrfutil in the main shell.

## Requirements
- nrfutil
  - toolchain-manager
- Python >= 3.10.0

## Install
Place nuts.py wherever you like, and add the following function to either .bashrc or .zshrc

```
nuts(){
    if [ $# -ne 0 ]
    then
        if [ "$1" = "$NCS_TOOLCHAIN_VERSION" ]
        then
            echo Toolchain version $1 is already in use.
        else
            echo Changing toolchain $NCS_TOOLCHAIN_VERSION to $1.
            source <(python <path_to_nuts.py> $1)
        fi
    else
        echo No toolchain version supplied
    fi
}
```

## Usage
```
  nuts <toolchain_version>
```

