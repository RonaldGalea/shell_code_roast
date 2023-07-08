
from colorama import Fore  # type: ignore
from .command import (  # type: ignore
    Command, CommandName, command_factory, str_to_command_name,
    CommandNameConversionError)


class Shell:
    """ A basic shell out of the box. """

    def __init__(self) -> None:
        self.supported_commands: dict[CommandName, Command] = {
            name: command_factory(name) for name in CommandName
        }

    def enter_command_to_execute(self) -> None:
        while True:
            user_input = input(f"  {Fore.YELLOW}[*] {Fore.CYAN}-> {Fore.WHITE}")
            try:
                self.execute_command(user_input)
            except (CommandNameConversionError, ValueError) as error:
                print(error)
                continue

    def execute_command(self, cmd: str) -> None:
        command_name, argv = self._parse_cmd(cmd)
        self.supported_commands[command_name].execute(argv)

    def _parse_cmd(self, cmd: str) -> tuple[CommandName, list[str]]:
        input_elements = cmd.split(' ')
        binary = input_elements[0].strip().upper()
        argv = [i.strip() for i in input_elements[1:]]

        command_name = str_to_command_name(binary)
        return command_name, argv
