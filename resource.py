import argparse
from dotenv import load_dotenv
from yaml import safe_load
from os import popen
from sys import exit

load_dotenv()
    
def nodeComputeUsage():
##Check pods on the node
    if args.namespace is None:
        pods_on_node = popen(f"kubectl get pods --field-selector=spec.nodeName={args.node},status.phase=Running -A -o yaml 2> /dev/null").read()
    else:
        pods_on_node = popen(f"kubectl get pods --field-selector=spec.nodeName={args.node},status.phase=Running  -n {args.namespace} -o yaml 2> /dev/null").read()
    pod_dict = safe_load(pods_on_node)
    final = []
    print(f"\nShowing Resource Consumption on {args.node}. Memory shown is in Mi. \n") if args.namespace is None else print(f"\nShowing Resource Consumption on {args.node} and for Namespace {args.namespace}. Memory shown is in Mi. \n")
    print(f"======================================================================\n")
    for data in pod_dict['items']:
        top = f'kubectl top pod -n {data["metadata"]["namespace"]} {data["metadata"]["name"]} --no-headers 2> /dev/null'
        pod_info_split = popen(top).read().split(" ")
        pod_split_data = [x for x in pod_info_split if x]
        if len(pod_split_data) > 0:
            cpu_usage = pod_split_data[1]
            mem_usage = pod_split_data[2].split("Mi")
        if args.namespace is None:
            pod_data = {
                "Memory": mem_usage[0],
                "Namespace": data["metadata"]["namespace"],
                "PodName": data["metadata"]["name"],
                # "CPU": cpu_usage,
            }
        else:
            pod_data = {
                "Memory": mem_usage[0],
                "PodName": data["metadata"]["name"],
                # "CPU": cpu_usage,
            }
        final.append(pod_data.copy())
    for data in final:
        print(data)
    print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", help="Node to check the usage for")
    parser.add_argument("--namespace", help="Namespace to check the usage for")
    args = parser.parse_args()

    #Exit if node name not given
    if not args.node:
        print("Provide the node name via --node option")
        exit()
    nodeComputeUsage()