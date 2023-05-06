from auto_everything.terminal import Terminal #type: ignore
from auto_everything.io import IO #type: ignore

terminal = Terminal()
io_ = IO()

ip_address = "192.168.56.101"

hosts_text = io_.read("/etc/hosts")
print(hosts_text)

target_domain_list = ["alternatives.domain.local", "user_alternatives.domain.local", "admin_alternatives.domain.local"]

new_lines = ""
for line in hosts_text.split("\n"):
    line = line.strip()
    if line == "":
        new_lines += "\n"
        continue
    if any([(one in line) == True for one in target_domain_list]):
        pass
    else:
        new_lines += line + "\n"
new_lines += f"{ip_address}        {' '.join(target_domain_list)}"

io_.write('/etc/hosts', new_lines)
print(new_lines)


        
