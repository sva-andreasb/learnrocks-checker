#!/usr/bin/python3
"""
This example shows how to display content in columns.
The data is pulled from https://randomuser.me
"""

import json
from urllib.request import urlopen

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
import subprocess
import os

import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
IPAddr=get_ip_address()

def get_service_stub(name='',servicename='',url='',credentials=''):
    return {'Name':name,'Status':'Unknown','color':'magenta','servicename':servicename,'url':url,'credentials':credentials}
def get_services():
    services = []
    services.append(checkService(get_service_stub('smtp4dev (E-Mails)','fakeSMTP',f'http://{IPAddr}:5000/', 'ohne Anmeldung')))
    services.append(checkService(get_service_stub('DB2','db2')))
    services.append(checkService(get_service_stub('LogViewer','logviewer',f'http://{IPAddr}:8111/','ohne Anmeldung')))
    services.append(checkService(get_service_stub('Cloudbeaver (SQL)','cloudbeaver',f'http://{IPAddr}:8978/','User cbadmin Pw cbadmin')))
    services.append(checkService(get_service_stub('WebSphere DMgr','websphere-dmgr',f'https://{IPAddr}:9043/ibm/console/','User wasadmin Pw wasadmin')))
    services.append(checkService(get_service_stub('IBM Control Desk / Maximo','websphere-node',f'http://{IPAddr}/maximo/','Standardbenutzer')))
    services.append(checkService(get_service_stub('Service Portal','ibm-svcportal',f'https://{IPAddr}:3000/','Standardbenutzer')))
    return services

def get_content(service):
    """Extract text from user dict."""
    status = service["Status"]
    url = service["url"]
    creds = service["credentials"]
    name = f"{service['Name']}"

    return f"[b]{name}[/b]\n[{service['color']}]{status}[/{service['color']}]\n{url}\n{creds}"

def checkService(service):
    if is_service_running(service['servicename']):
        service['Status'] = 'Running'
        service['color'] = 'green'
    else:
        service['Status'] = 'NOT Running'
        service['color'] = 'red'
    return service
def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        try:
            exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
        except:
            return False
        return exit_code == 0

if __name__ == '__main__':
    os.system('alias log="cd /opt/IBM/WebSphere/AppServer/profiles/ctgAppSrv01/logs/MXServer/')
    os.system('alias tlog="tail -f /opt/IBM/WebSphere/AppServer/profiles/ctgAppSrv01/logs/MXServer/SystemOut.log')
    services = get_services()
    console = Console()
    #users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
    #console.print(services, overflow="ignore", crop=False)
    service_renderables = [Panel(get_content(service), expand=True) for service in services]
    console.print(Columns(service_renderables))