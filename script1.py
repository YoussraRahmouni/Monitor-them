import paramiko
import apache_log_parser
from pprint import pprint
from datetime import datetime, timedelta
import time
from log_extract import log_tool

def getData(machine_name, fichier_log):

    #instanciation de la classe log_tool
    lt=log_tool()

    # initialisation de la connexion ssh
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(machine_name, 22, "interfadm", "Projet654!")

    try :
        #initialisation des données de temps (parse les dernières entrées du log
        previous_date=datetime.now()-timedelta(minutes=5)
        parsed_last_log=lt.initlastlog(fichier_log,client)
        last_line_date=parsed_last_log["time_received_datetimeobj"]

        #initialisation donnée
        #test de la nouveauté du log
        MemUsed=lt.getMemUsed(client)
        CpuUsage=lt.getCpuUsage(client)
        n=1
        error_count=0
        if last_line_date >= previous_date :
            response_time=[]
            ip_list=[]
            count_page_list=[]
            diff_page_list=[]
            log_date=last_line_date
            page_list=[[parsed_last_log['request_first_line'],1]]

            #tant que la ligne du log à une date plus récente que l'ancien log
            while log_date > previous_date:

                #Selection de la ligne de log a parser
                log="tail -"+str(n)+" /var/log/apache2/"+fichier_log+" | head -1"
                current_log=lt.sshcmd(log,client)
                current_log_data=lt.log_parsing(current_log)

                #en cas d'erreur, incrémentation du compteur d'erreur
                error_count+=lt.getError(current_log_data['status'])

                #incrémentation de la list des IP uniques
                lt.getIPlist(machine_name,current_log_data,ip_list)

                #incrémentation des pages visitée et du nombre de visites par pages
                lt.initpageLists(current_log_data,diff_page_list,count_page_list)

                #incrémentation de la liste des temps de réponses
                lt.getResponseTime(machine_name,n,response_time,client)

                #Changement de ligne de log à parser
                n+=1

                #Mise à jour de la ligne de log parsé pour le test de la boucle while
                log="tail -"+str(n)+" /var/log/apache2/"+fichier_log+" | head -1"
                current_log=lt.sshcmd(log,client)
                current_log_data=lt.log_parsing(current_log)#Dictionnary
                log_date=current_log_data["time_received_datetimeobj"]#timestamp

            #Récupération des pages demandées et des requêtes correspondantes
            page_list=lt.getPageLists(count_page_list,diff_page_list)
            #Si une ligne ou plus a été parsé, calcul de la moyenne du temps de réponse
            if n>1 :
                AVG_response_time=sum(response_time)/(n-1)

            #Fermeture de la connexion
            client.close()

            return[CpuUsage,MemUsed,page_list,error_count,len(ip_list), AVG_response_time]

    except Exception as e :
        client.close()
        print(e)
        return["Error","Error","Error","Error","Error", 0]
    
