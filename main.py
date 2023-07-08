from colorama import Fore  # type: ignore
from src.shell import Shell


DOC = f"""

{Fore.YELLOW}

Original Author: Hossin azmoud (Moody0101)
Date: 10/18/2022
LICENCE: MIT
Language: {Fore.CYAN}Python3.10 {Fore.YELLOW}
Descripion: A tool to hash, encode, decode text.
command: hash, encode, decode, help, exit
Usage:
    To encode/Decode:
        Encode/Decode <Text> <Algorithm>
        Encode/Decode only for help.
    To hash:
        Hash <Text> <Algorithm>
        Hash only for help.
"""


def main() -> None:
    print(DOC)
    shell = Shell()
    while True:
        shell.enter_command_to_execute()


if __name__ == '__main__':
    main()
