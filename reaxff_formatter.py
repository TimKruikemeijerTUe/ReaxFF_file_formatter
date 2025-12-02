# Based on https://github.com/arvk/EZFF under MIT
from pathlib import Path
from typing import Callable


class ReaxFF_formatter:
    def __init__(
        self,
        filename: Path | str | None = None,
        filestring: str | None = None,
    ):
        """ReaxFF forcefield class. Used for formatting ReaxFF forcefields

        Parameters
        ----------
        filename : Path | str | None, optional
            ReaxFF forcefield filename, by default None
        filestring : str | None, optional
            ReaxFF forcefield filestring, if filename is provided, this does nothing, by default None
        """

        if not filename is None:
            self._read_forcefield_from_txt_file(filename)
        elif not filestring is None:
            self._read_forcefield_from_string(filestring)

    def write_formatted_forcefields(self, path_out: Path | str):
        """Function to write the formatted ReaxFF forcefield

        Parameters
        ----------
        path_out : Path | str
            File where the forcefield will be written to
        """
        string: str = self.header

        # Write general parameters
        for line_nr, line in enumerate(self.general):
            if line_nr == 0:
                string += f" {int(line[0]):2d}        {" ".join(line[1:]):s}\n"
            else:
                string += f"{float(line[0]):10.4f} {" ".join(line[1:]):s}\n"

        # One-body term
        for line_nr, line in enumerate(self.onebody[:4]):
            if line_nr == 0:
                string += f"{int(line[0]):3d}    {" ".join(line[1:]):s}\n"
            else:
                string += f"            {" ".join(line):s}\n"

        for line_nr, line in enumerate(self.onebody[4:]):
            if line_nr % 4 == 0:
                string += (
                    f" {line[0]:<2}"
                    + "".join([f"{float(val):9.4f}" for val in line[1:]])
                    + "\n"
                )
            else:
                string += "   " + "".join([f"{float(val):9.4f}" for val in line]) + "\n"

        # Two-body terms
        for line_nr, line in enumerate(self.twobody[:2]):
            if line_nr == 0:
                string += f"{int(line[0]):3d}    {" ".join(line[1:]):s}\n"
            else:
                string += f"            {" ".join(line):s}\n"

        for line_nr, line in enumerate(self.twobody[2:]):
            if line_nr % 2 == 0:
                string += (
                    f"{int(line[0]):3d}"
                    + f"{int(line[1]):3d}"
                    + "".join([f"{float(val):9.4f}" for val in line[2:]])
                    + "\n"
                )
            else:
                string += (
                    "      " + "".join([f"{float(val):9.4f}" for val in line]) + "\n"
                )

        # Off-diagonal
        for line_nr, line in enumerate(self.offdiagonal):
            if line_nr == 0:
                string += f"{int(line[0]):3d}    {" ".join(line[1:]):s}\n"
            else:
                string += (
                    f"{int(line[0]):3d}"
                    + f"{int(line[1]):3d}"
                    + "".join([f"{float(val):9.4f}" for val in line[2:]])
                    + "\n"
                )

        # Threebody
        for line_nr, line in enumerate(self.threebody):
            if line_nr == 0:
                string += f"{int(line[0]):3d}    {" ".join(line[1:]):s}\n"
            else:
                string += (
                    f"{int(line[0]):3d}"
                    + f"{int(line[1]):3d}"
                    + f"{int(line[2]):3d}"
                    + "".join([f"{float(val):9.4f}" for val in line[3:]])
                    + "\n"
                )

        # Fourbody
        for line_nr, line in enumerate(self.fourbody):
            if line_nr == 0:
                string += f"{int(line[0]):3d}    {" ".join(line[1:]):s}\n"
            else:
                string += (
                    f"{int(line[0]):3d}"
                    + f"{int(line[1]):3d}"
                    + f"{int(line[2]):3d}"
                    + f"{int(line[3]):3d}"
                    + "".join([f"{float(val):9.4f}" for val in line[4:]])
                    + "\n"
                )

        # Hbond
        for line_nr, line in enumerate(self.hbond):
            if line_nr == 0:
                string += f"{int(line[0]):3d}    {" ".join(line[1:]):s}\n"
            else:
                string += (
                    f"{int(line[0]):3d}"
                    + f"{int(line[1]):3d}"
                    + f"{int(line[2]):3d}"
                    + "".join([f"{float(val):9.4f}" for val in line[3:]])
                    + "\n"
                )

        with open(path_out, "w", newline="\n") as f:
            f.write(string)

    def _read_forcefield_from_txt_file(self, filename: Path | str):
        """Read ReaxFF forcefield from txt file

        Parameters
        ----------
        filename : Path | str
            ReaxFF forcefield filename
        """

        with open(filename, "r") as ff_file:
            ff_text = ff_file.read()

        # Parse forcefield from read-in string
        self._read_forcefield_from_string(ff_text)

    def _read_forcefield_from_string(self, ff_text: str):
        """Read ReaxFF forcefield from a given forcefield string

        Parameters
        ----------
        ff_text : str
            ReaxFF forcefield string
        """
        list_of_strings = [line + "\n" for line in ff_text.split("\n")]

        self.full_text = list_of_strings
        self._split_forcefield()

    def _split_forcefield(self):
        """
        Split ReaxFF forcefield into sections corresponding to general, one-body, two-body, three-body, four-body, offdiagonal and H-bond sections
        """
        ff: list[str] = self.full_text

        # Read HEADER line
        header = ff[0]

        i_line: int = 1

        ## For parsing blocks
        # Gets first int
        get_nr: Callable[[str], int] = lambda line: int(line.strip().split()[0])
        get_text: Callable[[list[str], int, int, int], list[str]] = (
            lambda ff, i, nr, mult: ff[i : i + (nr * mult) + mult]
        )  # one for the header another for the number of parameters

        def parse_block(ff: list[str], i_line: int, mult: int):
            nr_lines = get_nr(ff[i_line])
            block_text = get_text(ff, i_line, nr_lines, mult)
            block_lines = [line.strip().split() for line in block_text]
            i_line += nr_lines * mult + mult
            return block_lines, i_line

        # Mult determines the lines per item
        general, i_line = parse_block(ff, i_line, 1)
        onebody, i_line = parse_block(ff, i_line, 4)
        twobody, i_line = parse_block(ff, i_line, 2)
        offdiag, i_line = parse_block(ff, i_line, 1)
        threebody, i_line = parse_block(ff, i_line, 1)
        fourbody, i_line = parse_block(ff, i_line, 1)
        hbond, i_line = parse_block(ff, i_line, 1)

        self.header = header
        self.general = general
        self.onebody = onebody
        self.twobody = twobody
        self.offdiagonal = offdiag
        self.threebody = threebody
        self.fourbody = fourbody
        self.hbond = hbond
