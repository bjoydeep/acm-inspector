from prometheus_api_client import *
import datetime
import sys
import numpy as np
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

def checkSpokeCPUUsage(startTime, endTime, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking CPU Usage on the spoke cluster")
    pc=promConnect()
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True

    status=ACMPodKlusterletCPUUsage(pc,startTime, endTime, step)
    status=ACMPodWorkmgrCPUUsage(pc,startTime, endTime, step)
    status=ACMPodAppCPUUsage(pc,startTime, endTime, step)
    status=ACMPodSearchCPUUsage(pc,startTime, endTime, step)
    status=ACMPodGRCCPUUsage(pc,startTime, endTime, step)
    status=ACMPodClusterProxyCPUUsage(pc,startTime, endTime, step)
    status=ACMPodMgmtSACPUUsage(pc,startTime, endTime, step)
    status=ACMPodObsCPUUsage(pc,startTime, endTime, step)

    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("CPU Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    return status
 
def print_query_prometheus_result(pc, query, column_name):
    try:
        result = pc.custom_query(query)
        df = MetricSnapshotDataFrame(result)
        df["value"] = df["value"].astype(float)
        df.rename(columns={"value": column_name}, inplace = True)
        print(df[['workload',column_name]].to_markdown())
        return df

    except Exception as e:
        print(Fore.RED + f"Error in print querying Prometheus: {e}")
        print(Style.RESET_ALL)

def print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file):
    print(title)

    try:
        print_query_prometheus_result(pc, query, column_name)

        query_range = pc.custom_query_range(
            query=query,
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        df = MetricRangeDataFrame(query_range)
        df["value"]=df["value"].astype(float)
        df.index= pandas.to_datetime(df.index, unit="s")
        df = df.pivot(columns='workload',values='value')
        df.rename(columns={"value": column_name}, inplace = True)
        df.plot(title=title,figsize=(30, 15))

        plt.savefig('../../output/breakdown/' + file + '.png')
        saveCSV(df,file)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + f"Error in querying Prometheus: {e}")
        print(Style.RESET_ALL)
    print("=============================================")
   
    status=True
    return status

def ACMPodKlusterletCPUUsage(pc,startTime, endTime, step):
    title = "ACM Klusterlet CPU usage"
    column_name = "ACMKlusterletCPUUsage"
    file = "acm-pod-klusterlet-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-agent"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent", workload_type="deployment",workload=~"klusterlet|klusterlet-agent"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodWorkmgrCPUUsage(pc,startTime, endTime, step):
    title = "ACM Workmgr CPU usage"
    column_name = "ACMWorkmgrCPUUsage"
    file = "acm-pod-workmgr-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-agent-addon"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"klusterlet-addon-workmgr"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodAppCPUUsage(pc,startTime, endTime, step):
    title = "ACM Application CPU usage"
    column_name = "ACMApplicationCPUUsage"
    file = "acm-pod-application-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-agent-addon"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"application-manager"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodSearchCPUUsage(pc,startTime, endTime, step):
    title = "ACM Search CPU usage"
    column_name = "ACMSearchCPUUsage"
    file = "acm-pod-search-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-agent-addon"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"klusterlet-addon-search"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodGRCCPUUsage(pc,startTime, endTime, step):
    title = "ACM GRC CPU usage"
    column_name = "ACMGRCCPUUsage"
    file = "acm-pod-grc-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-agent-addon"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"cert-policy-controller|config-policy-controller|governance-policy-framework|iam-policy-controller"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodClusterProxyCPUUsage(pc,startTime, endTime, step):
    title = "ACM Cluster Proxy CPU usage"
    column_name = "ACMClusterProxyCPUUsage"
    file = "acm-pod-cluster-proxy-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-agent-addon"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"cluster-proxy-proxy-agent|cluster-proxy-service-proxy"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodMgmtSACPUUsage(pc,startTime, endTime, step):
    title = "ACM Mgmt Service Account CPU usage"
    column_name = "ACMMgmtSACPUUsage"
    file = "acm-pod-mgmt-sa-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-agent-addon"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"managed-serviceaccount-addon-agent"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodObsCPUUsage(pc,startTime, endTime, step):
    title = "ACM OBS CPU usage"
    column_name = "ACMOBSCPUUsage"
    file = "acm-pod-obs-cpu-usage"
    query = 'sum( \
          node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster="", namespace="open-cluster-management-addon-observability"} \
        * on(namespace,pod) \
          group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-addon-observability", workload_type="deployment",workload=~"endpoint-observability-operator|metrics-collector-deployment"} \
        ) by (workload, workload_type)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)