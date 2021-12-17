import paramiko
import apache_log_parser
from pprint import pprint
import datetime
from datetime import tzinfo

def sshcmd(hostname, port, username, password, command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    client.connect(hostname, port=port, username=username, password=password)

    _, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode("utf-8")
    #for line in output.splitlines():
        #print(line)
    return output


#sshcmd("161.3.160.65", 22, "interfadm", "Projet654!", "tail -100 /var/log/apache2/access.log")

#log=sshcmd("161.3.160.65", 22, "interfadm", "Projet654!","tail -1 /var/log/apache2/access.log")






def log_parsing(log_line):
    line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
    log_line_data=line_parser(log_line)
    return log_line_data



###
#test_parser= '127.0.0.1 - - [07/Dec/2021:12:26:14 +0100] "GET /index.html HTTP/1.1" 200 3477 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"'

previous_date=datetime.datetime(2021, 12, 7, 12, 26, 23)

def count_difference():
    last_log=sshcmd("161.3.160.65", 22, "interfadm", "Projet654!","tail -1 /var/log/apache2/access.log")
    parsed_last_log=log_parsing(last_log)
    last_line_date=parsed_last_log["time_received_datetimeobj"]

    n=1
    ip_list=[]
    error_count=0



    if last_line_date >= previous_date :
        count_page_list=[]
        diff_page_list=[]
        log_date=last_line_date
        page_list=[[parsed_last_log['request_first_line'],1]]
        while log_date > previous_date:

            log="tail -"+str(n)+" /var/log/apache2/access.log | head -1"
            current_log=sshcmd("161.3.160.65", 22, "interfadm", "Projet654!",log);
            current_log_data=line_parser(current_log)#Dictionnary
            log_date=current_log_data["time_received_datetimeobj"]#timestamp


            if current_log_data['status']>'399' and current_log_data['status']<'600':
                error_count+=1

            if current_log_data['remote_host'] not in ip_list:
                ip_list.append(current_log_data['remote_host'])
            #get visited pages and count visit number
            log_page=current_log_data['request_first_line']

            if log_page in diff_page_list:
                count_page_list.append(log_page)
            if log_page not in diff_page_list:
                diff_page_list.append(log_page)
                count_page_list.append(log_page)
            page_list=[0]*(len(diff_page_list))
            for i in range (0,len(diff_page_list)):
                c=0
                for j in range (0,len(count_page_list)):
                    if count_page_list[j]==diff_page_list[i]:
                        c+=1
                page_list[i]=([diff_page_list[i],c])





            n+=1

        print(page_list)
        print(error_count)
        print(len(ip_list))
        print(n-1)
