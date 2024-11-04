import pexpect
import re
import rich
import os
from pathlib import Path

destination = Path("/home/pavel/Pictures/Fairphone")
device_pattern = "Fairphone FP3 \[\d+%\]:.*> "
storage = "Interní sdílené úložiště"
storage_path = Path("DCIM/OpenCamera")

child = pexpect.spawn('/usr/bin/aft-mtp-cli', encoding = 'utf-8')
assert child.isalive()

child.expect(device_pattern)
print(child.before)

# SET storage
child.sendline(f'storage "{storage}"')
child.expect(device_pattern)
print(child.before)

# MOVE to source directory
for directory in str(storage_path).split("/"):
    child.sendline(f"cd {directory}")
    child.expect(device_pattern)
    print(child.before)

# LIST files
child.sendline("ls")
child.expect("Fairphone FP3 \[\d+%\]:.*> ")
print(child.before)

# GET files
for line in child.before.splitlines():
    if m := re.match('(\d+) +(.+\..+)', line):
        size, name = m.groups()

        #check if file is already downloaded
        file_path = destination / Path(name.strip())
        if file_path.is_file():
            #if so, then skip
            rich.print(f"File [cyan]{file_path}[/cyan] already exists, skipping.")
        else:
            #if not, download it and move to the destination folder
            rich.print(f"Downloading file [red]{name}[/red]...")
            child.sendline(f"get {name}")
            child.expect("Fairphone FP3 \[\d+%\]:.*> ")
            print(child.before)
            downloaded_file = Path(".")/Path(name.strip()).absolute()
            rich.print(f"Moving [green]{downloaded_file}[/green] to [blue]{file_path}[/blue].")
            os.rename(downloaded_file, file_path)
