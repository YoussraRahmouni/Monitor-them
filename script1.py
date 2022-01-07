import paramiko
import apache_log_parser
from pprint import pprint
import datetime
import time

def sshcmd(hostname, port, username, password, command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    client.connect(hostname, port=port, username=username, password=password)

    _, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode("utf-8")
    #for line in output.splitlines():
        #print(line)
    client.close();
    return output



#sshcmd("161.3.160.65", 22, "interfadm", "Projet654!", "tail -100 /var/log/apache2/access.log")

#log=sshcmd("37.110.193.25", 22, "interfadm", "Projet654!","tail -1 /var/log/apache2/access.log.1")

MemUsed=sshcmd("37.110.193.25", 22, "interfadm", "Projet654!","free | tail -2 | head -1 | awk '{ print $5 }' ")

CpuUsage=sshcmd("37.110.193.25", 22, "interfadm", "Projet654!","cat /proc/stat |grep cpu |tail -1|awk '{print ($5*100)/($2+$3+$4+$5+$6+$7+$8+$9+$10)}'|awk '{print 100-$1}'")


def log_parsing(log_line):
    line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
    log_line_data=line_parser(log_line)
    return log_line_data



###
#test_parser= '127.0.0.1 - - [07/Dec/2021:12:26:14 +0100] "GET /index.html HTTP/1.1" 200 3477 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"'

previous_date=datetime.datetime(2022, 1, 4, 12, 15, 0)


line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
#delay_parser = apache_log_parser.make_parser("%D")

def count_difference(machine_name, fichier_log):
    last_log=sshcmd(machine_name, 22, "interfadm", "Projet654!",("tail -1 /var/log/apache2/"+fichier_log))
    parsed_last_log=log_parsing(last_log)
    #print(parsed_last_log)
    last_line_date=parsed_last_log["time_received_datetimeobj"]
    #print(last_line_date)
    n=1
    ip_list=[]
    error_count=0

    MemUsed=sshcmd("37.110.193.25", 22, "interfadm", "Projet654!","free | tail -2 | head -1 | awk '{ print $5 }' ")

    CpuUsage=sshcmd("37.110.193.25", 22, "interfadm", "Projet654!","cat /proc/stat |grep cpu |tail -1|awk '{print ($5*100)/($2+$3+$4+$5+$6+$7+$8+$9+$10)}'|awk '{print 100-$1}'")

    if last_line_date >= previous_date :
        count_page_list=[]
        diff_page_list=[]
        log_date=last_line_date
        page_list=[[parsed_last_log['request_first_line'],1]]
        while log_date > previous_date:

            log="tail -"+str(n)+" /var/log/apache2/"+fichier_log+" | head -1"
            current_log=sshcmd(machine_name, 22, "interfadm", "Projet654!",log);
            current_log_data=line_parser(current_log)#Dictionnary

            print(current_log_data["time_received_datetimeobj"])

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
            #Update variables
            log="tail -"+str(n)+" /var/log/apache2/"+fichier_log+" | head -1"
            current_log=sshcmd(machine_name, 22, "interfadm", "Projet654!",log);
            current_log_data=line_parser(current_log)#Dictionnary
            log_date=current_log_data["time_received_datetimeobj"]#timestamp

        #print("Cpu Usage : ",CpuUsage)
        #print("Memory Used : ",MemUsed)
        #print(page_list)
        #print("Error Count : ",error_count)
        #print("Unique Ips : ",len(ip_list))
        #print(n-1)
        return[CpuUsage,MemUsed,page_list,errror_count,len(ip_list)]
        
        #pour récupérer les données : 
        #countdifference(nom_machine, nom_fichier_logs)[0] : utilisation cpu
        #countdifference(nom_machine, nom_fichier_logs)[1] : utilisation memoire
        
        #countdifference(nom_machine, nom_fichier_logs)[2][x][0/1] : page visitée et nb de fois(faire une boucle pour tout afficher)
        #countdifference(nom_machine, nom_fichier_logs)[3] : nb erreurs
        #countdifference(nom_machine, nom_fichier_logs)[4] : nb de connection uniques
