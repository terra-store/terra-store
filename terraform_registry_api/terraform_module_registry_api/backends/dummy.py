import json

from .abstract import AbstractBackend

from terraform_registry_api.terraform_module_registry_api.exceptions \
    import ModuleNotFoundException


class Dummy(AbstractBackend):
    """Dummy implementation of backend used for testing."""

    dummy_data = {
        "modules":
            {
                "/terra/test/aws": {
                    "versions": [
                        "1.0.0",
                        "1.1.0",
                        "2.0.0"
                    ]
                },
                "/terra/k8s/aws": {
                    "versions": [
                        "1.0.0",
                        "1.1.0",
                        "2.0.0"
                    ]
                }
            }
    }

    def get_versions(self, namespace, name, provider):
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
        if module_name in self.dummy_data['modules'].keys():
            list_versions = []
            for version in self.dummy_data['modules'][module_name]['versions']:
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

    def download_version(self, namespace, name, provider, version):
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
        if module_name in self.dummy_data['modules'].keys() and \
                version in self.dummy_data['modules'][module_name]['versions']:
            if name == "k8s":
                base_url = ""
            else:
                base_url = "https://api.github.com/repos/"
            return "{base_url}{namespace}/{provider}-{name}/v{version}".format(
                provider=provider, base_url=base_url,
                name=name, version=version, namespace=namespace)
        raise ModuleNotFoundException("Module Not Found: " + module_name)

    def download_latest(self, namespace, name, provider):
        """Find the latest version of the module.

        Find the latest version of the module and return
        a 302 to the download url for the module.

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
        if module_name in self.dummy_data['modules'].keys():
            url = "{base_url}{module_name}/2.0.0/download".format(
                module_name=module_name,
                base_url="http://localhost:5000/v1/modules")
            return url
        raise ModuleNotFoundException("Module Not Found: " + module_name)

    def get_modules(self, namespace=None):
        """Get all modules in namespace provided.

        Args:
            namespace (str, optional): Namespace of modules. Defaults to None.

        Returns:
            json: JSON representation of the modules within the namespace
        """
        modules = []
        if namespace is None:
            modules = self.dummy_data['modules'].keys()
        else:
            search_string = "/" + namespace
            modules = [module for module in self.dummy_data['modules']
                       if module.startswith(search_string)]
        details = {
            'meta': {
                'limit': 0,
                'current_offset': 0,
            },
            'modules': get_module_details(modules)
        }
        return json.dumps(details)

    def search_modules(self, query):
        """Search the module list based on the query.

        Args:
            query (str): Query string used for the search

        Returns:
            json: List of modules including details
        """
        modules = [module for module in self.dummy_data['modules']
                   if query in module]

        response = {
            "meta": {
                "limit": 0,
                "current_offset": 0,
            },
            "modules": get_module_details(modules)
        }
        return json.dumps(response)

    def get_latest_all_providers(self, namespace, name):
        """Get Latest versions for each deployed provider.

        Args:
            namespace (str): namespace for the version
            name (str): Name of the module

        Returns:
            json: List of all provders and latest version for
            defined namespace and name
        """
        module_name = "/{namespace}/{name}/".format(
            namespace=namespace, name=name)

        providers = [module for module in self.dummy_data['modules']
                     if module.startswith(module_name)]
        return json.dumps({
            "meta": {
                "limit": 0,
                "current_offset": 0
            },
            "modules": get_module_details(providers)
        })

    def get_module(self, namespace, name, provider, version=None):
        """Get module with extended details.

        Args:
            namespace (str): namespace for the version
            name (str): Name of the module
            provider (str): Provider for the module
            version (str, optional): Version for the module. Defaults to None.

        Raises:
            ModuleNotFoundException: If module not found raise exception

        Returns:
            dict: Module details with all extended attributes
        """
        if version is None:
            version = "2.0.0"
        module_name = "/{namespace}/{name}/{provider}".format(
            namespace=namespace, name=name, provider=provider)
        if module_name in self.dummy_data['modules'].keys() and \
                version in self.dummy_data['modules'][module_name]['versions']:
            return json.dumps(get_extended_details(namespace,
                                                   name,
                                                   provider,
                                                   version))
        raise ModuleNotFoundException("Module Not Found: " + module_name)


def get_extended_details(namespace, name, provider, version):
    """Get Module with fully extended details.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module
        version (str): Version for the module

    Returns:
        dict: dict with all the module extended metadata
    """
    module_name = "{namespace}/{name}/{provider}/{version}".format(
        namespace=namespace, name=name,
        provider=provider, version=version)
    return {
        'id': module_name,
        'owner': 'noone',
        'namespace': namespace,
        'name': name,
        'version': version,
        'provider': provider,
        'description': 'Fake Module.',
        'source': 'http://localhost:5000/storage/{module}'.format(
            module=module_name),
        'published_at': '2021-10-17T01:22:17.792066Z',
        'downloads': 213,
        'verified': True,
        "root": {
            "path": "",
            "readme": "# Title",
            "empty": False,
            "inputs": [
            ],
            "outputs": [
            ],
            "dependencies": [],
            "resources": []
        },
        "submodules": [
        ],
        "providers": [
            "aws",
        ],
        "versions": [
            "1.0.0",
            "1.1.0",
            "2.0.0"
        ]
    }


def get_module_details(modules):
    """Get extended details for the modules in the list.

    Args:
        modules (list): [description]

    Returns:
        list: List of modules including details
    """
    module_details = []
    for mod in modules:
        data = mod.split("/")
        details = {
            'id': '{module}/2.0.0'.format(module=mod),
            'owner': 'noone',
            'namespace': data[1],
            'name': data[2],
            'version': '2.0.0',
            'provider': data[3],
            'description': 'Fake Module.',
            'source': 'http://localhost:5000/storage{module}/2.0.0'.format(
                module=mod),
            'published_at': '2021-10-17T01:22:17.792066Z',
            'downloads': 213,
            'verified': True
        }
        module_details.append(details)
    return module_details
