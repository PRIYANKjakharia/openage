# Copyright 2020-2020 the openage authors. See copying.md for legal info.

# TODO pylint: disable=C,R
"""
Creates debug output from data in a conversion run.
"""
from openage.convert.value_object.read.media.datfile.empiresdat import EmpiresDatWrapper
from openage.convert.value_object.read.read_members import SubdataMember,\
    IncludeMembers, MultisubtypeMember


def debug_gamedata_format(debugdir, game_version, loglevel):
    """
    Logs the data format of a .dat file of a specific a game version.
    """
    logfile = debugdir.joinpath("read/")["data_format"]
    logtext = ""

    discovered_structs = {EmpiresDatWrapper}
    handled_structs = set()

    while discovered_structs:
        struct = discovered_structs.pop()

        if struct in handled_structs:
            continue

        members = struct.get_data_format_members(game_version)
        logtext += f"struct name: {struct.name_struct}\n"
        logtext += f"total member count: {len(members)}\n"

        max_name_width = 1
        max_vmemb_width = 1
        for member in members:
            # Find out width of columns for table formatting
            if len(str(member[1])) > max_name_width:
                max_name_width = len(str(member[1]))

            if len(str(member[2])) > max_vmemb_width:
                max_vmemb_width = len(str(member[2]))

            # Search for sub-structs
            if isinstance(member[3], IncludeMembers):
                discovered_structs.add(member[3].cls)

            elif isinstance(member[3], MultisubtypeMember):
                discovered_structs.update(member[3].class_lookup.values())

        for member in members:
            logtext += (
                f"{str(member[0].value):8}  "
                f"{str(member[1]):{max_name_width}}  "
                f"{str(member[2]):{max_vmemb_width}}  "
                f"{str(member[3])}\n"
            )

        handled_structs.add(struct)
        logtext += "\n"

    with logfile.open("w") as log:
        log.write(logtext)
