import pexpect
import re

device_pattern = "Fairphone FP3 \[\d+%\]:.*> "
storage = "Interní sdílené úložiště"
path = "DCIM/OpenCamera" #TODO pathlib

child = pexpect.spawn('/usr/bin/aft-mtp-cli', encoding = 'utf-8')
assert child.isalive()

child.expect(device_pattern)
print(child.before)

# SET storage
child.sendline(f'storage "{storage}"')
child.expect(device_pattern)
print(child.before)

# MOVE to source directory
for directory in path.split("/"):
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

        print(f"Downloading file...{name}")
        child.sendline(f"get {name}")
        child.expect("Fairphone FP3 \[\d+%\]:.*> ")
        print(child.before)
