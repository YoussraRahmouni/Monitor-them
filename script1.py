import paramiko
import apache_log_parser
from pprint import pprint

def sshcmd(hostname, port, username, password, command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    print(hostname, port, username, password)
    client.connect(hostname, port=port, username=username, password=password)

    _, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode("utf-8")
    try:
        for line in output.splitlines():
            print(line)
    finally:
        if client:
            client.close()
    return output

#sshcmd("161.3.160.65", 22, "interfadm", "Projet654!", "ifconfig -a")

log_line=sshcmd("161.3.160.65", 22, "interfadm", "Projet654!","head /var/log/apache2/access.log")
print(log_line)

def log_parsing(log_line):
    line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
    log_line_data=line_parser(log_line)
    return(log_line_data)
