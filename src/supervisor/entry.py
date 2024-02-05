    
from mch import *       
from container import *
from sizing import *
from managedCluster import *
from node import *
from apiServer import *
from etcd import *
from cpuAnalysis import *
from memoryAnalysis import *
from spokeMemoryAnalysis import *
from spokeCPUAnalysis import *
from thanos import *
from apiServerObjects import *
from managedClusterNodes import *
from colorama import Fore, Back, Style
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime
import matplotlib.pyplot as plt
import os

#Fore(text color)	BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
#Back(for highlight)	BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
#Style	DIM, NORMAL, BRIGHT, RESET_ALL

def parse_timedelta(arg):
    if 'd' in arg:
        return timedelta(days=int(arg[:-1]))
    elif 'h' in arg:
        return timedelta(hours=int(arg[:-1]))
    elif 'm' in arg:
        return timedelta(minutes=int(arg[:-1]))
    else:
        raise ValueError("Invalid time format. Use 'h' for hours or 'm' for minutes.")

# pass debug(boolean) as env
def main():
    step='1m'
    tsdb = sys.argv[1]

    cluster='hub'
    if len(sys.argv) > 2:
        cluster = sys.argv[2].lower()  
        if cluster not in ['hub', 'spoke']:
            print("Invalid cluster. Use 'hub' or 'spoke'. Defaulting to 'hub'.")
            cluster = 'hub'

    #start_time=dt.datetime(2021, 7, 31, 21, 30, 0, tzinfo=query.getUTC())
    #end_time=dt.datetime(2021, 8, 1, 12, 25, 0, tzinfo=query.getUTC())
    start_time=(datetime.now() - timedelta(days=7))
    if len(sys.argv) > 3 :
        start_time=(datetime.now() - parse_timedelta(sys.argv[3]))
    end_time=datetime.now()

    now = datetime.now()
    #print(Fore.MAGENTA+"")
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Starting date for this ACM Health Check  - ",now)
    print("Starting datetime for History collection - ", start_time)
    print("End date and time for History collection - ", end_time)
    print(f"Parameters passed to the script : ", tsdb)
    print("************************************************************************************************")
    print(Style.RESET_ALL)
   
    createSubdir()
    # hub only
    if cluster != "spoke" :
       mch = checkMCHStatus()
    node = checkNodeStatus()

    if tsdb == "prom" : #if route is cluster prom
         cont = checkACMContainerStatus(start_time, end_time, step)
         api = checkAPIServerStatus(start_time, end_time, step)
         etcd = checkEtcdStatus(start_time, end_time, step)
         cpu = checkCPUUsage(start_time, end_time, step)
         memory = checkMemoryUsage(start_time, end_time, step)
         podcpu = checkSpokeCPUUsage(start_time, end_time, step)
         podmemory = checkSpokeMemoryUsage(start_time, end_time, step)
         # hub only
         if cluster != "spoke" :
            thanos = checkThanosStatus(start_time, end_time, step)
            apiObjet = checkAPIServerObjects(start_time, end_time, step)
    else: #if route is observability thanos
         # does not work yet
         sizing = checkACMHubClusterUtilization() 
    
    # hub only
    if cluster != "spoke" :
        mc = checkManagedClusterStatus()
        getManagedClusterNodeCount()
        saveMasterDF()

    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("End ACM Health Check")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
if __name__ == "__main__":
    main()