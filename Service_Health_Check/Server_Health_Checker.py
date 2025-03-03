import datetime 
import os, psutil
import paramiko
from colorama import Fore, Style


# Check Ping connectivity of the server
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def check_ping_connection():
    ping_response = os.system(f"ping -n 3 {Server_address}")

    if ping_response == 0:
        print(f"\n\n✅ {Server_address} is UP and Running Fine.")
    else:
        print(Fore.RED + f"\n\n⚠️ {Server_address} is NOT Pingable !!" + Style.RESET_ALL)


# Check SSH connection of the server
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def check_ssh_connection():
    try:
        # Create a Paramiko SSH client instance
        client = paramiko.SSHClient()

        # Automatically add the SSH key if it's not in known hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server using the private key
        client.connect(hostname, port=port, username=username, key_filename=private_key_path)

        print(f"\n\n✅ SSH Connection to {hostname} is Successful.")

        # Run a simple command to verify the connection (optional)
        stdin, stdout, stderr = client.exec_command('hostname')
        print(f"\n{hostname} Hostname : {stdout.read().decode()}")

        stdin, stdout, stderr = client.exec_command("uptime")
        print(f"\n{hostname} Uptime : ", stdout.read().decode())

        stdin, stdout, stderr = client.exec_command("cat /etc/os-release | grep PRETTY")
        print(f"\n{hostname} OS Version : ", stdout.read().decode())

        check_linux_service()
        check_cpu_usage()
        check_memory_usage()
        check_storage_usage()

        client.close()

    except Exception as exception:
        print(Fore.RED + f"\n\n❌ SSH Connection Failed !!" + Style.RESET_ALL)
        print(f"\n⌚ Last Check Time = {datetime.datetime.now()}")
        print(f"\n{exception}")


# Check if Linux Services is running or not in the server
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def check_linux_service():
    for service in services:
        try:
            service_status= os.system(f"systemctl is-active {service}")
            if service_status == "active":
                print(f"\n\n✅{service} is Running Fine in server {Server_address}.")
            elif service_status == "inactive":
                print(Fore.RED + f"\n\n❌ {service} is NOT Running in server {Server_address} !!" + Style.RESET_ALL)
                print(f"\n⌚ Last Check Time = {datetime.datetime.now()}")
            else:
                print(f"\n\n🚫 {service} status is Unknown for server {Server_address} !!")
                print(f"\n⌚ Last Check Time = {datetime.datetime.now()}")
        except Exception as exception:
                print(Fore.RED + f"\n\n🚨 Error : {service} service in server {Server_address}"  + Style.RESET_ALL)
                print(f"\n{exception}")
                print(f"\n⌚ Last Check Time = {datetime.datetime.now()}")


# Check CPU Usage in the server
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    top_five_cpu_consuming_process = os.system("ps aux --sort=-%cpu | head -n 7")
    if cpu_usage >= 90:
        print(f"\n\n🚨 {Server_address} CPU Usage is Critical !!")
        print(f"\n{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%s")} : CPU Utilization = {cpu_usage}%")
        print(f"Top Five CPU Utilization Process is Following :")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -")
        print(f"{top_five_cpu_consuming_process}")
    elif cpu_usage >= 80:
        print(f"\n\n ⚠️ {Server_address} CPU Usage is High !!")
        print(f"\n{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%s")} : CPU Utilization = {cpu_usage}%")
        print(f"Top Five CPU Utilization Process is Following :")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -")
        print(f"{top_five_cpu_consuming_process}")
    elif cpu_usage >= 50 and cpu_usage <=79:
        print(f"\n\n💙 {Server_address} CPU Usage is in Normal Range !!")
        print(f"\n{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%s")} : CPU Utilization = {cpu_usage}%")
        print(f"Top Five CPU Utilization Process is Following :")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -")
        print(f"{top_five_cpu_consuming_process}")
    else:
        print(f"\n\n💚 {Server_address} CPU Usage is Healthy.")
        print(f"\n{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%s")} : CPU Utilization = {cpu_usage}%")
        print(f"Top Five CPU Utilization Process is Following :")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -")
        print(f"{top_five_cpu_consuming_process}")


# Check Memory Usage in the server
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def check_memory_usage():
    memory_usage = psutil.virtual_memory()
    total_memory = memory_usage.total / (1024 * 1024 * 1024)
    used_memory = memory_usage.used / (1024 * 1024 * 1024)
    available_memory = memory_usage.available / (1024 * 1024 * 1024)
    percent_use_memory = memory_usage.percent
    top_five_memory_consuming_process = os.system("ps aux --sort=-%mem | head -n 6")

    if percent_use_memory >= 90:
        print(f"\n\n🚨 {Server_address} Memory Status is Critical !! ")
        print("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(f"\t\nTotal Memory : ", {total_memory})
        print(f"\t\nUsed Memory : ", {used_memory})
        print(f"\t\nFree Memory : ", {available_memory})
        print(f"\t\nMemory Utilization in Percentage : ", {percent_use_memory})
        print(f"\n\nTop Five Memory Utilization Process is Following :")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -")
        print(f"{top_five_memory_consuming_process}")
    else:
        print(f"\n\n🎚️ {Server_address} Memory Status :- ")
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(f"\nTotal Memory : ", {total_memory})
        print(f"\nUsed Memory : ", {used_memory})
        print(f"\nFree Memory : ", {available_memory})
        print(f"\nMemory Utilization in Percentage : ", {percent_use_memory})
        print(f"\n\nTop Five Memory Utilization Process is Following :")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -")
        print(f"{top_five_memory_consuming_process}")


# Check Storage Usage in the server
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def check_storage_usage():
    disk_usage = psutil.disk_usage("/")
    total_disk = disk_usage.total 
    used_disk = disk_usage.used
    available_disk = disk_usage.free
    percent_use_disk = disk_usage.percent
    
    if percent_use_disk >= 90:
        print(f"\n\n🚨 {Server_address} Storage Status Critical !! ")
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(f"\nTotal Disk Storage : ", {total_disk})
        print(f"\nUsed Sotrage: ", {used_disk})
        print(f"\nFree Storage : ", {available_disk})
        print(f"\nStorage Utilization in Percentage : ", {percent_use_disk})
    else:
        print(f"\n\n💽 {Server_address} Storage Status :- ")
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(f"\nTotal Disk Storage : ", {total_disk})
        print(f"\nUsed Sotrage: ", {used_disk})
        print(f"\nFree Storage : ", {available_disk})
        print(f"\nStorage Utilization in Percentage : ", {percent_use_disk})


# Get Server Address & List of services to check in Linux server
# Perform All the Check
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
print("❤️ Server Health Checker . . . . . > > > 📈")
print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")
Server_address = input("\n\n➕ Enter the Server Hostname, Url OR IP Address : ")

hostname = Server_address
port = 22 
username = "root"
private_key_path = '/etc/ssh/ssh_host_rsa_key'
services = ["ssh", "httpd", "prometheus", "grafana", "jenkins"]

check_ping_connection()
check_ssh_connection()
