import requests
import psutil
import platform

def get_provider_name():
    provider_name = "unknown"
    try:
        aws_metadata_url = "http://169.254.169.254/latest/meta-data/"
        aws_response = requests.get(aws_metadata_url, timeout=1)
        if aws_response.status_code == 200:
            provider_name = "AWS"
    except requests.RequestException:
        pass

    try:
        gcp_metadata_url = "http://metadata.google.internal/computeMetadata/v1/"
        gcp_headers = {"Metadata-Flavor": "Google"}
        gcp_response = requests.get(gcp_metadata_url, headers=gcp_headers, timeout=1)
        if gcp_response.status_code == 200:
            provider_name = "GCP"
    except requests.RequestException:
        pass

    try:
        azure_metadata_url = "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
        azure_headers = {"Metadata": "true"}
        azure_response = requests.get(azure_metadata_url, headers=azure_headers, timeout=1)
        if azure_response.status_code == 200:
            provider_name = "Azure"
    except requests.RequestException:
        pass

    return provider_name

def get_instance_type(provider_name):
    instance_type = "unknown"
    try:
        if provider_name == "AWS":
            aws_instance_type_url = "http://169.254.169.254/latest/meta-data/instance-type"
            instance_type = requests.get(aws_instance_type_url, timeout=1).text
        elif provider_name == "GCP":
            gcp_instance_type_url = "http://metadata.google.internal/computeMetadata/v1/instance/machine-type"
            gcp_headers = {"Metadata-Flavor": "Google"}
            instance_type = requests.get(gcp_instance_type_url, headers=gcp_headers, timeout=1).text.split('/')[-1]
        elif provider_name == "Azure":
            azure_instance_type_url = "http://169.254.169.254/metadata/instance/compute/vmSize?api-version=2021-02-01"
            azure_headers = {"Metadata": "true"}
            instance_type = requests.get(azure_instance_type_url, headers=azure_headers, timeout=1).json()["vmSize"]
    except requests.RequestException:
        pass

    return instance_type

def get_cpu_info():
    cpu_freq = psutil.cpu_freq()
    cpu_info = {
        'Model': platform.processor(),
        'CPU': psutil.cpu_count(logical=False),
        'CPU Speed(MHz)': cpu_freq.current if cpu_freq else "N/A",
        'Architecture': platform.machine()
    }
    return cpu_info

def get_ram_info():
    ram_info = {
        'Ram (MB)': str(psutil.virtual_memory().total // (1024 * 1024))
    }
    return ram_info

def get_system_info():
    system_info = {}
    system_info.update(get_cpu_info())
    system_info.update(get_ram_info())
    system_info['Provider'] = get_provider_name()
    system_info['Instance'] = get_instance_type(system_info['Provider'])
    return system_info

def get_system_info_list():
    system_info = get_system_info()
    system_info_list = [f"{key}={value}" for key, value in system_info.items()]
    return system_info_list