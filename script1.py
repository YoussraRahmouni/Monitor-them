import paramiko

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
