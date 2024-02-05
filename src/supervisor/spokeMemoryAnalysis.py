from prometheus_api_client import *
import datetime
import sys
import numpy as np
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

def checkSpokeMemoryUsage(startTime, endTime, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking Memory Usage on the spoke cluster")
    pc=promConnect()
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True

    status=ACMPodKlusterletMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodKlusterletMemUsageWSS(pc,startTime, endTime, step)
    status=ACMPodWorkmgrMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodWorkmgrMemUsageWSS(pc,startTime, endTime, step)
    status=ACMPodAppMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodAppMemUsageWSS(pc,startTime, endTime, step)
    status=ACMPodSearchMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodSearchMemUsageWSS(pc,startTime, endTime, step)
    status=ACMPodGRCMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodGRCMemUsageWSS(pc,startTime, endTime, step)
    status=ACMPodClusterProxyMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodClusterProxyMemUsageWSS(pc,startTime, endTime, step)
    status=ACMPodMgmtSAMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodMgmtSAMemUsageWSS(pc,startTime, endTime, step)
    status=ACMPodObsMemUsageRSS(pc,startTime, endTime, step)
    status=ACMPodObsMemUsageWSS(pc,startTime, endTime, step)

    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Memory Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
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


def ACMPodKlusterletMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM Klusterlet Memory (rss) usage MB"
    column_name = "ACMKlusterletMemUsageRSSMB"
    file = "acm-pod-klusterlet-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent", workload_type="deployment",workload=~"klusterlet|klusterlet-agent"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)


def ACMPodKlusterletMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM Klusterlet Memory (wss) usage MB"
    column_name = "ACMKlusterletMemUsageWSSMB"
    file = "acm-pod-klusterlet-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent", workload_type="deployment",workload=~"klusterlet|klusterlet-agent"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)


def ACMPodWorkmgrMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM Workmgr Memory (rss) usage MB"
    column_name = "ACMWorkmgrMemUsageRSSMB"
    file = "acm-pod-workmgr-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"klusterlet-addon-workmgr"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodWorkmgrMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM Workmgr Memory (wss) usage MB"
    column_name = "ACMWorkmgrMemUsageWSSMB"
    file = "acm-pod-workmgr-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"klusterlet-addon-workmgr"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodAppMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM Application Memory (rss) usage MB"
    column_name = "ACMApplicationMemUsageRSSMB"
    file = "acm-pod-application-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"application-manager"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodAppMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM Application Application (wss) usage MB"
    column_name = "ACMSearchMemUsageWSSMB"
    file = "acm-pod-application-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"application-manager"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodSearchMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM Search Memory (rss) usage MB"
    column_name = "ACMSearchMemUsageRSSMB"
    file = "acm-pod-search-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"klusterlet-addon-search"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodSearchMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM Search Memory (wss) usage MB"
    column_name = "ACMSearchMemUsageWSSMB"
    file = "acm-pod-search-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"klusterlet-addon-search"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodGRCMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM GRC Memory (rss) usage MB"
    column_name = "ACMGRCMemUsageRSSMB"
    file = "acm-pod-grc-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"cert-policy-controller|config-policy-controller|governance-policy-framework|iam-policy-controller"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodGRCMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM GRC Memory (wss) usage MB"
    column_name = "ACMGRCMemUsageWSSMB"
    file = "acm-pod-grc-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"cert-policy-controller|config-policy-controller|governance-policy-framework|iam-policy-controller"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodClusterProxyMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM Cluster Proxy Memory (rss) usage MB"
    column_name = "ACMGRCMemUsageRSSMB"
    file = "acm-pod-cluster-proxy-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"cluster-proxy-proxy-agent|cluster-proxy-service-proxy"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodClusterProxyMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM Cluster Proxy Memory (wss) usage MB"
    column_name = "ACMGRCMemUsageWSSMB"
    file = "acm-pod-cluster-proxy-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"cluster-proxy-proxy-agent|cluster-proxy-service-proxy"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodMgmtSAMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM Mgmt Service Accout Memory (rss) usage MB"
    column_name = "ACMMgmtSAMemUsageRSSMB"
    file = "acm-pod-mgmt-sa-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"managed-serviceaccount-addon-agent"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodMgmtSAMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM Mgmt Service Accout Memory (wss) usage MB"
    column_name = "ACMMgmtSAMemUsageWSSMB"
    file = "acm-pod-mgmt-sa-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-agent-addon", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-agent-addon", workload_type="deployment",workload=~"managed-serviceaccount-addon-agent"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodObsMemUsageRSS(pc,startTime, endTime, step):
    title = "ACM OBS Memory (rss) usage MB"
    column_name = "ACMOBSMemUsageRSSMB"
    file = "acm-pod-obs-mem-usage-rss"
    query = '(sum( \
        container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-addon-observability", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-addon-observability", workload_type="deployment",workload=~"endpoint-observability-operator|metrics-collector-deployment"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)

def ACMPodObsMemUsageWSS(pc,startTime, endTime, step):
    title = "ACM OBS Memory (wss) usage MB"
    column_name = "ACMOBSMemUsageWSSMB"
    file = "acm-pod-obs-mem-usage-wss"
    query = '(sum( \
        container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", namespace="open-cluster-management-addon-observability", container!="", image!=""} \
      * on(namespace,pod) \
        group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster="", namespace="open-cluster-management-addon-observability", workload_type="deployment",workload=~"endpoint-observability-operator|metrics-collector-deployment"} \
        ) by (workload, workload_type))/(1024*1024)'

    return print_save_query_prometheus_result(pc, startTime, endTime, step, query, column_name, title, file)
