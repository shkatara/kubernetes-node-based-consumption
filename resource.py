#!/usr/bin/python3
import argparse
from dotenv import load_dotenv
from yaml import safe_load
from os import popen,environ
from sys import exit

    
def nodeComputeUsage():
##Check pods on the node
    if args.ns is None:
        pods_on_node = popen(f"kubectl get pods --field-selector=spec.nodeName={args.n},status.phase=Running -A -o yaml 2> /dev/null").read()
    else:
        pods_on_node = popen(f"kubectl get pods --field-selector=spec.nodeName={args.n},status.phase=Running  -n {args.ns} -o yaml 2> /dev/null").read()
    pod_dict = safe_load(pods_on_node)
    final = []
    print(f"\nShowing Resource Consumption on {args.n}. Memory shown is in Mi. \n") if args.ns is None else print(f"\nShowing Resource Consumption on {args.n} and for Namespace {args.ns}. Memory shown is in Mi. \n")
    print(f"======================================================================\n")
    for data in pod_dict['items']:
        top = f'kubectl top pod -n {data["metadata"]["namespace"]} {data["metadata"]["name"]} --no-headers 2> /dev/null'
        pod_info_split = popen(top).read().split(" ")
        pod_split_data = [x for x in pod_info_split if x]
        if len(pod_split_data) > 0:
            cpu_usage = pod_split_data[1]
            mem_usage = pod_split_data[2].split("Mi")
        pod_data = {
                "Memory": mem_usage[0],
                **({'Namespace': data["metadata"]["namespace"]} if args.ns is  None else {}),  #Read more about "dictionary unpacking"
                "PodName": data["metadata"]["name"],
                # "CPU": cpu_usage,
            }
        final.append(pod_data.copy())
    for data in final:
        print(data)
    print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="Node to check the usage for")
    parser.add_argument("-ns", help="Namespace to check the usage for")
    parser.add_argument("-c", help="Cluster to check for [prod,stage]")
    args = parser.parse_args()
    if args.c == "prod" or args.c == "Prod":
        environ['KUBECONFIG'] = "/Users/skatara/.kube/kube_prod"
    else:
        environ['KUBECONFIG'] = "/Users/skatara/.kube/kube_stage"
    #Exit if node name not given
    if not args.n:
        print("Provide the node name via --node option")
        exit()
    nodeComputeUsage()
