# import platform
# import os
# import re
# import subprocess
#
#
# if platform.system() == "Windows":
#     print(platform.processor())
#
# elif platform.system() == "Linux":
#     command = "cat /proc/cpuinfo"
#     all_info = subprocess.check_output(command, shell=True).decode().strip()
#     print(all_info)
#     for line in all_info.split("\n"):
#         if "model name" in line:
#             print(re.sub(".*model name.*:", "", line, 1))


