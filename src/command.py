from __future__ import annotations

from binascii import hexlify, unhexlify

from hashlib import (
    blake2b,
    blake2s,
    md5,
    sha1,
    sha224,
    sha256,
    sha384,
    sha3_224,
    sha3_256,
    sha3_384,
    sha3_512,
    sha512,
)
from base64 import (
    a85decode,
    a85encode,

    b16decode,
    b16encode,

    b32decode,
    b32encode,

    b32hexdecode,
    b32hexencode,

    b64decode,
    b64encode,

    b85decode,
    b85encode
)


from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, ClassVar


class CommandName(Enum):
    HELP = 'HELP'
    EXIT = 'EXIT'
    ENCODE = 'ENCODE'
    DECODE = 'DECODE'
    HASH = 'HASH'


class CommandNameConversionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def str_to_command_name(name: str) -> CommandName:
    if name.upper() not in CommandName.__members__.keys():
        raise CommandNameConversionError(f'Invalid command name: {name}')

    return CommandName[name.upper()]


def command_factory(name: CommandName) -> Command:
    if name == CommandName.EXIT:
        return ExitCommand(name)
    elif name == CommandName.HELP:
        return HelpCommand(name)
    elif name == CommandName.ENCODE:
        return EncodeCommand(name)
    elif name == CommandName.DECODE:
        return DecodeCommand(name)
    elif name == CommandName.HASH:
        return HashCommand(name)
    else:
        raise NotImplementedError(f'Command not implemented: {name}')


@dataclass
class Command(ABC):
    name: CommandName

    def get_name(self) -> CommandName:
        return self.name

    @abstractmethod
    def execute(self, argv: list[str]) -> None:
        # self._validate_argv()
        pass

    @abstractmethod
    def _validate_argv(self, argv: list[str]) -> None:
        pass


@dataclass
class HelpCommand(Command):
    DOCUMENTATION: ClassVar[str] = """

To encode/Decode:
    Encode/Decode <Text> <Algorithm>
    Encode/Decode only for help.
To hash:
    Hash <Text> <Algorithm>
    Hash only for help.

    """

    def execute(self, argv: list[str]) -> None:
        self._validate_argv(argv)
        print(HelpCommand.DOCUMENTATION)

    def _validate_argv(self, argv: list[str]) -> None:
        if len(argv) != 0:
            raise ValueError(f'This command takes no arguments: {self.name}')


@dataclass
class ExitCommand(Command):
    def execute(self, argv: list[str]) -> None:
        self._validate_argv(argv)
        print('Exiting...')
        exit(0)

    def _validate_argv(self, argv: list[str]) -> None:
        if len(argv) != 0:
            raise ValueError(f'This command takes no arguments: {self.name}')


@dataclass
class DecodeCommand(Command):
    ALGORITHMS: ClassVar[dict[str, Callable[[bytes | str], bytes]]] = {
        "A85": a85decode,
        "BASE16": b16decode,
        "BASE32": b32decode,
        "BASE32HEX": b32hexdecode,
        "BASE64": b64decode,
        "BASE85": b85decode,
        "HEXLIFY": unhexlify
    }

    DOCUMENTATION: str = f'Syntax: Decode <InputText> < {" | ".join(list(ALGORITHMS.keys()))} >'

    def execute(self, argv: list[str]) -> None:
        if len(argv) == 0:
            print(DecodeCommand.DOCUMENTATION)
            return

        self._validate_argv(argv)
        input_data, algorithm = argv

        func_ = DecodeCommand.ALGORITHMS[algorithm.upper().strip()]

        # first decode from text encoded string to bytes, then decode from bytes to python string
        print(func_(input_data).decode())

    def _validate_argv(self, argv: list[str]) -> None:
        if len(argv) != 2:
            raise ValueError(f'This command takes exactly 2 arguments: {self.name}')

        _, algorithm = argv
        available_algorithms = DecodeCommand.ALGORITHMS.keys()

        if algorithm.upper().strip() not in DecodeCommand.ALGORITHMS.keys():
            raise ValueError(f"Invalid algorithm name: {algorithm};" +
                             f"Available algorithms: {available_algorithms}")


@dataclass
class EncodeCommand(Command):

    ALGORITHMS: ClassVar[dict[str, Callable[[bytes], bytes]]] = {
        "A85": a85encode,
        "BASE16": b16encode,
        "BASE32": b32encode,
        "BASE32HEX": b32hexencode,
        "BASE64": b64encode,
        "BASE85": b85encode,
        "HEXLIFY": hexlify
    }

    DOCUMENTATION: str = f'Syntax: Encode <InputText> < {" | ".join(list(ALGORITHMS.keys()))} > '

    def execute(self, argv: list[str]) -> None:
        if len(argv) == 0:
            print(EncodeCommand.DOCUMENTATION)
            return

        self._validate_argv(argv)
        input_data, algorithm = argv

        func_ = EncodeCommand.ALGORITHMS[algorithm.upper().strip()]

        # character encoding, i.e. get bytes from string
        input_data_bytes = input_data.encode()

        # textual encoding, i.e. still bytes but encoded in a different way
        print(func_(input_data_bytes))

    def _validate_argv(self, argv: list[str]) -> None:
        if len(argv) != 2:
            raise ValueError(f'This command takes exactly 2 arguments: {self.name}')

        _, algorithm = argv
        available_algorithms = EncodeCommand.ALGORITHMS.keys()

        if algorithm.upper().strip() not in available_algorithms:
            raise ValueError(f"Invalid algorithm name: {algorithm};" +
                             f"Available algorithms: {available_algorithms}")


@dataclass
class HashCommand(Command):
    ALGORITHMS: ClassVar = {
        "BLAKE2B": blake2b,
        "BLAKE2S": blake2s,
        "MD5": md5,
        "SHA1": sha1,
        "SHA224": sha224,
        "SHA256": sha256,
        "SHA384": sha384,
        "SHA3_224": sha3_224,
        "SHA3_256": sha3_256,
        "SHA3_384": sha3_384,
        "SHA3_512": sha3_512,
        "SHA512": sha512
    }

    DOCUMENTATION: ClassVar[str] = f'Syntax: Hash <InputText> < {" | ".join(list(ALGORITHMS.keys()))} >'

    def execute(self, argv: list[str]) -> None:
        if len(argv) == 0:
            print(HashCommand.DOCUMENTATION)
            return None

        self._validate_argv(argv)
        input_data, algorithm = argv
        input_data_bytes = input_data.encode()

        hashing_fn = HashCommand.ALGORITHMS[algorithm.upper().strip()]
        print(hashing_fn(input_data_bytes).hexdigest())

    def _validate_argv(self, argv: list[str]) -> None:
        if len(argv) != 2:
            raise ValueError(f'This command takes exactly 2 arguments: {self.name}')

        _, algorithm = argv
        if algorithm.upper() not in HashCommand.ALGORITHMS.keys():
            raise ValueError(f'Invalid algorithm name: {algorithm}; Available algorithms: {HashCommand.ALGORITHMS.keys()}')
