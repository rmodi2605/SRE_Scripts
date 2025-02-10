import os
import requests
import time, datetime
import smtplib
from email.mime.text import MIMEText
from colorama import Fore, Style


# List of Web Services
# Load environment variables from .env file
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
services = [{"name": "Jenkins", "url" : "http://192.168.152.128:8080"},
            {"name": "Prometheus", "url" : "http://192.168.152.128:9090"},
            {"name": "GitHub", "url" : "https://github.com/"},
            {"name": "Prometheus_error_link", "url" : "https://prometheus.io/events/"},
            {"name": "Not_exist_url", "url" : "https://192.168.254.254/"}]


# Send email alert if service is not reachable
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def send_email_alert(web_name, web_url, downtime, http_code):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_from = "rajmodi2605@gmail.com"
    email_to = "rajmodi2605@gmail.com"
    email_pass = os.environ.get("email_password")
    email_subject = (f"⚠️ Alert : {web_name} is Unreachable")
    email_body =  (f"""
    🚨 {web_name} is NOT Reachable OR Down !! \n\n
    ⌚ Last Check Time =  {downtime} \n\n
    🌐 Web Service URL = {web_url}\n\n
    🔍 HTTP Response code = {http_code} \n\n
    👀 Please investigate the service error & endpoint associated with it.""")

    email_msg = MIMEText(email_body)
    email_msg["Subject"] = email_subject
    email_msg["From"] = email_from
    email_msg["To"] = email_to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as email_server:
            email_server.starttls()
            email_server.login(email_from, email_pass)
            email_server.send_message(email_msg)
            print("\nEmail alert sent successfully.")
    except Exception as email_excep:
            print(f"\nFailed to send email alert.")
            print(f"\nReason to Failed send email : {email_excep}")


# Send email alert if service exception occurs
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def send_exeception_email_alert(web_name, web_url, downtime, web_execption):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_from = "rajmodi2605@gmail.com"
    email_to = "rajmodi2605@gmail.com"
    email_pass = os.environ.get("email_password")
    email_subject = (f"🔔 Alert : {web_name} Service Fetching Issue")
    email_body =  (f"""
    🚫 {web_name} web service fetching error occured !! \n\n
    ⌚ Last Check Time =  {downtime} \n\n
    🌐 Web Service URL = {web_url}\n\n
    ❌ Web Fetching Error = {web_execption} \n\n
    👀 Please investigate the web service issue.""")

    email_msg = MIMEText(email_body)
    email_msg["Subject"] = email_subject
    email_msg["From"] = email_from
    email_msg["To"] = email_to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as email_server:
            email_server.starttls()
            email_server.login(email_from, email_pass)
            email_server.send_message(email_msg)
            print("\nEmail alert sent successfully.")
    except Exception as email_excep:
            print(f"\nFailed to send email alert.")
            print(f"\nReason to Failed send email : {email_excep}")


# Check Service Health
# If Error or Execption occurs then print it as Log
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def check_web_service():
    for service in services:
        try:
            service_url = service['url']
            service_name = service['name']
            service_response = requests.get(service['url'], verify=False)
            if service_response.status_code == 200 or service_response.status_code == 403:
                print(Fore.GREEN + f"\n\n{datetime.datetime.now()} : {service_name} Service is Healthy" + Style.RESET_ALL)
                print(f"\nWeb Url : {service_url}")
                print(f"\nResponse time : {service_response.elapsed.total_seconds()}")
                print("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")
            else:
                print(Fore.RED + f"\n\n{datetime.datetime.now()} : {service_name} is NOT Reachable !!" + Style.RESET_ALL)
                print(f"\nWeb Url : {service_url}")
                print(f"\nHTTP Status Code : {service_response.status_code}")
                print(f"\nResponse Time : {service_response.elapsed.total_seconds()}")
                send_email_alert(service_name, service_url, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), service_response.status_code)
                print("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")
        except requests.exceptions.RequestException as exception:
                print(Fore.RED + f"\n\n{datetime.datetime.now()} : {service_name} Service Fetching Error!" + Style.RESET_ALL)
                print(f"\nWeb Url : {service_url}")
                print(f"\n{exception}")
                send_exeception_email_alert(service_name, service_url, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), exception)
                print("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")


# Perform service health check every 15 seconds
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
while True:
    check_web_service()
    print ("\n\n* * * * * * * * * * * * * * * * * * * * * * * * ")
    print ("\n⌛ Rechecking in 15 Seconds.......")
    print ("\n* * * * * * * * * * * * * * * * * * * * * * * * ")
    time.sleep(15)
