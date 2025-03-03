# Web Service Endpoints Health Checker

The objective of this Project is to continuously check multiple web service endpoint health and get an email alert if any endpoint is either unreachable or any error, exception occurs.
<br>
<br>

## Technology Used for the Project

- Python

- SMTP

- Linux


## Prerequisites
Genrate App Password for Trigger email on Gmail OR your Chosen email platform. 

Here, I used Gmail for gettting email alert.

1. Login into Gmail Account
2. Go to **Manage your Google Account**
3. Select **Security**
4. Enable Two-Step Verification
5. Once 2-Step Verification is enabled, return to the Security tab
<br> Scroll down and click on App Passwords.
6. Generate an App Password
7. Copy App Password (16-character app password) immediately as it can only be viewed once.
<br> Save it somewhere safe.


## Initial Steps
1. Add email key in Linux environment variable

```bash
export email_password="wnfunops********"
```

<br>

2. Varify email key in environment variable

```bash
echo $email_password

wnfunops********
```

<br>

3. Make Script Executable 
```bash
cd SRE_Scripts/Web_Service_Health_Checker 

sudo chmod +x Web_Service_Health_Checker.py
```

<br>

4. Run it
```bash
source ~/py_envs/bin/activate

python Web_Service_Health_Checker.py
```
<br>

## Demonstration
``` bash
✅ 2025-03-03 13:17:03.253390 => Jenkins Service is Healthy

🌐 Web Url : http://192.168.152.128:8080

⌚ Response time : 0.012169

= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


✅ 2025-03-03 13:17:03.260800 => Prometheus Service is Healthy

🌐 Web Url : http://192.168.152.128:9090

⌚ Response time : 0.002035

= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
/root/py_envs/lib/python3.12/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host 'github.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(


✅ 2025-03-03 13:17:03.725741 => GitHub Service is Healthy

🌐 Web Url : https://github.com/

⌚ Response time : 0.332207

= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
/root/py_envs/lib/python3.12/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host 'prometheus.io'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(


❌ 2025-03-03 13:17:07.157247 => Prometheus_error_link is NOT Reachable !!

🌐 Web Url : https://prometheus.io/events/

🔍 HTTP Status Code : 404

⌚ Response Time : 3.428108

📧 Email alert sent successfully.

= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


🚫 2025-03-03 13:17:32.835267 => Not_exist_url Service Fetching Error !!

🌐 Web Url : https://192.168.254.254/

⛔ Error Detail : HTTPSConnectionPool(host='192.168.254.254', port=443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7358fa88d760>: Failed to establish a new connection: [Errno 111] Connection refused'))

📧 Email alert sent successfully.

= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


* * * * * * * * * * * * * * * * * * * * * * * *

⌛ Rechecking in 15 Seconds.......

* * * * * * * * * * * * * * * * * * * * * * * *


✅ 2025-03-03 13:17:52.442144 => Jenkins Service is Healthy

🌐 Web Url : http://192.168.152.128:8080

⌚ Response time : 0.010943

= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


✅ 2025-03-03 13:17:52.448848 => Prometheus Service is Healthy

🌐 Web Url : http://192.168.152.128:9090

⌚ Response time : 0.001942
.
.
.
.
.
```
<br>


### Email Alert IF web service is Unreachable
![Email_Alert _For_Timeout_Error](https://github.com/rmodi2605/SRE_Scripts/blob/main/Web_Service_Health_Checker/images/Email_Alert%20_For_Timeout_Error.jpg)
<br>
<br>


### Email Alert IF web service exception occurs
![Email_Alert _For_Unreachable](https://github.com/rmodi2605/SRE_Scripts/blob/main/Web_Service_Health_Checker/images/Email_Alert%20_For_Unreachable.jpg)

<br>


## Scope of Application
- The Script Can be trigger with desired frequency with  <code style="color : Red">**CronJob**</code>
<br>

- It can be also use as a <code style="color : Red">**Linux Web Health Check Service**</code>
<br>

- The Script can integrate with any <code style="color : Red">**Monitoring Platfroms**</code> to continuously check web Health Check every few minutes or seconds.