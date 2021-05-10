import json
from terraform_registry_api.terraform_module_registry_api.exceptions import ModuleNotFoundException


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
    
    module_name="/{namespace}/{name}/{provider}".format(namespace=namespace, name=name, provider=provider)
    if module_name in dummy_data['modules'].keys():
        list_versions= []
        for version in dummy_data['modules'][module_name]['versions']:
            list_versions.append( {"version": version})
        versions = {
            "modules": [
                {
                    "versions": list_versions
                }
            ]
        }

        return json.dumps(versions)
    else:
        raise ModuleNotFoundException("Module Not Found: "+ module_name)

def download_version(namespace, name, provider, version):
    module_name="/{namespace}/{name}/{provider}".format(namespace=namespace, name=name, provider=provider)
    if module_name in dummy_data['modules'].keys() and version in version in dummy_data['modules'][module_name]['versions']:
        return "https://api.github.com/repos/{namespace}/terraform-{provider}-{name}/tarball/v{version}//*?archive=tar.gz".format(provider=provider, 
                                                                                                                       name=name,
                                                                                                                       version=version,
                                                                                                                       namespace = namespace)
    else:
        raise ModuleNotFoundException("Module Not Found: "+module_name )