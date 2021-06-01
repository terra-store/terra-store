import json
import yaml

from distutils.version import StrictVersion
from os.path import join, exists, basename, relpath
from os import scandir
from .abstract import AbstractBackend

from terraform_registry_api.terraform_module_registry_api.exceptions \
    import ModuleNotFoundException


class Filesystem(AbstractBackend):
    """Backend using local Filesystem for storage."""

    def __init__(self, basedirectory):
        self.basedir = basedirectory
        super().__init__()

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
        provider_dir = join(self.basedir, namespace, name, provider)
        if exists(provider_dir):
            versions = [basename(f.path) for f in scandir(provider_dir) if f.is_dir()]
            response = {
                "modules": [
                    {
                        "versions": [{"version": ver} for ver in versions]
                    }
                ]

            }
            return json.dumps(response)
        else:
            raise ModuleNotFoundException("Module Not Found")

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
        if exists(join(self.basedir, namespace, name, provider, version)):
            filename = "{namespace}_{name}-{provider}-{version}.tar.gz".format(namespace=namespace,
                                                                               name=name,
                                                                               provider=provider,
                                                                               version=version)
            return join(namespace, name, provider, version, filename)
        else:
            raise ModuleNotFoundException("Module Not Found")

    def determine_latest(self, namespace, name, provider):
        provider_dir = join(self.basedir, namespace, name, provider)
        versions = [basename(f.path) for f in scandir(provider_dir) if f.is_dir()]
        versions.sort(key=StrictVersion)
        versions.reverse()
        return versions[0]

    def download_latest(self, baseurl, namespace, name, provider):
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
        provider_dir = join(self.basedir, namespace, name, provider)
        if exists(provider_dir):
            latest_version = self.determine_latest(namespace, name, provider)
            url = "{base_url}/{namespace}/{name}/{provider}/{version}/download".format(
                namespace=namespace, name=name,
                provider=provider, version=latest_version,
                base_url=baseurl+"v1/modules")
            return url
        raise ModuleNotFoundException("Module Not Found")

    def get_modules(self, baseurl, namespace=None):
        """Get all modules in namespace provided.

        Args:
            namespace (str, optional): Namespace of modules. Defaults to None.

        Returns:
            json: JSON representation of the modules within the namespace
        """
        pass

    def search_modules(self, baseurl, query):
        """Search the module list based on the query.

        Args:
            query (str): Query string used for the search

        Returns:
            json: List of modules including details
        """
        pass

    def get_latest_all_providers(self, baseurl, namespace, name):
        """Get Latest versions for each deployed provider.

        Args:
            namespace (str): namespace for the version
            name (str): Name of the module

        Returns:
            json: List of all provders and latest version for
            defined namespace and name
        """
        module_dir = join(self.basedir, namespace, name)
        if exists(module_dir):
            providers = [relpath(f.path, self.basedir) for f in scandir(module_dir) if f.is_dir()]
        else:
            providers = []
        return json.dumps({
            "meta": {
                "limit": 0,
                "current_offset": 0
            },
            "modules": self.get_module_details(baseurl, providers)
        })


    def get_module(self, baseurl, namespace, name, provider, version=None):
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
        provider_dir = join(self.basedir, namespace, name, provider)
        if exists(provider_dir):
            if version is None:
                version = self.determine_latest(namespace, name, provider)

            return json.dumps(self.get_extended_details(baseurl,
                                                        namespace,
                                                        name,
                                                        provider,
                                                        version))
        else:
            raise ModuleNotFoundException("Module Not Found")


    def get_extended_details(self, baseurl, namespace, name, provider, version):
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
        provider_dir = join(self.basedir,
                            namespace,
                            name,
                            provider)
        mod_dir = join(self.basedir, namespace, name)
        meta = self.load_metadata(namespace, name)
        print(meta)
        return {
            'id': module_name,
            'owner': meta['owner'],
            'namespace': namespace,
            'name': name,
            'version': version,
            'provider': provider,
            'description': meta['description'],
            'source': '{baseurl}dl/modules/{module}'.format(
                baseurl=baseurl, module=module_name),
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
            "providers": [basename(f.path) for f in scandir(mod_dir) if f.is_dir()],
            "versions": [basename(f.path) for f in scandir(provider_dir) if f.is_dir()]
        }


    def get_module_details(self, baseurl, modules):
        """Get extended details for the modules in the list.

        Args:
            modules (list): [description]

        Returns:
            list: List of modules including details
        """
        module_details = []
        for mod in modules:
            data = mod.split("/")
            version = self.determine_latest(data[0], data[1], data[2])
            meta = self.load_metadata(data[0], data[1])
            details = {
                'id': '/{module}/{version}'.format(
                    module=mod, version=version),
                'owner': meta['owner'],
                'namespace': data[0],
                'name': data[1],
                'version': version,
                'provider': data[2],
                'description': meta['description'],
                'source': '{baseurl}dl/modules/{module}/{version}'.format(
                    baseurl=baseurl, module=mod, version=version),
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
            module_details.append(details)
        return module_details

    def load_metadata(self, namespace, name):
        metafile = join(self.basedir, namespace, name, "module_metadata.yaml")
        if exists(metafile):
            with open(metafile) as metayaml:
                return yaml.safe_load(metayaml)
