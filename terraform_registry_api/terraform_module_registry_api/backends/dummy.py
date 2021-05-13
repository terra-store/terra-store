import json
from terraform_registry_api.terraform_module_registry_api.exceptions \
    import ModuleNotFoundException


dummy_data = {
    "modules":
        {
            "/pexa/test/aws": {
                "versions": [
                    "1.0.0",
                    "1.1.0",
                    "2.0.0"
                ]
            }
        }
}


def get_versions(namespace, name, provider):
    """Get The Versions.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module

    Raises:
        ModuleNotFoundException: Error if module does not exist

    Returns:
        json: JSON object containing the versions of the module on the server
    """
    module_name = "/{namespace}/{name}/{provider}".format(
        namespace=namespace, name=name, provider=provider)
    if module_name in dummy_data['modules'].keys():
        list_versions = []
        for version in dummy_data['modules'][module_name]['versions']:
            list_versions.append({"version": version})
        versions = {
            "modules": [
                {
                    "versions": list_versions
                }
            ]
        }
        return json.dumps(versions)
    raise ModuleNotFoundException("Module Not Found: " + module_name)


def download_version(namespace, name, provider, version):
    """Generate Download URL for module version.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module
        version (str): Version for the module

    Raises:
        ModuleNotFoundException: Error if module does not exist

    Returns:
        str: Download url of the module itself
    """
    module_name = "/{namespace}/{name}/{provider}".format(
        namespace=namespace, name=name, provider=provider)
    if module_name in dummy_data['modules'].keys() and \
            version in dummy_data['modules'][module_name]['versions']:

        return "{base_url}/{namespace}/{provider}-{name}/v{version}".format(
            provider=provider, base_url="https://api.github.com/repos",
            name=name, version=version, namespace=namespace)
    raise ModuleNotFoundException("Module Not Found: "+module_name)


def download_latest(namespace, name, provider):
    """Find the latest version of the module and return a 302 to the download
    url for the module.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module

    Raises:
        ModuleNotFoundException: Error if module does not exist

    Returns:
        str: URL for downloading module
    """
    module_name = "/{namespace}/{name}/{provider}".format(
        namespace=namespace, name=name, provider=provider)
    if module_name in dummy_data['modules'].keys():
        url = "{base_url}{module_name}/2.0.0/download".format(
            module_name=module_name,
            base_url="http://localhost:5000/v1/modules")
        return url
    raise ModuleNotFoundException("Module Not Found: "+module_name)
