from backends import dummy as backend

def list_versions(namespace, name, provider):
    return backend.get_versions(namespace, name, provider)

def download_version(namespace, name, provider, version):
    return ""