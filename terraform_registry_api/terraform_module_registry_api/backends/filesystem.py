from os.path import join, exists

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
        pass

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
        pass

    def get_modules(self, namespace=None):
        """Get all modules in namespace provided.

        Args:
            namespace (str, optional): Namespace of modules. Defaults to None.

        Returns:
            json: JSON representation of the modules within the namespace
        """
        pass

    def search_modules(self, query):
        """Search the module list based on the query.

        Args:
            query (str): Query string used for the search

        Returns:
            json: List of modules including details
        """
        pass

    def get_latest_all_providers(self, namespace, name):
        """Get Latest versions for each deployed provider.

        Args:
            namespace (str): namespace for the version
            name (str): Name of the module

        Returns:
            json: List of all provders and latest version for
            defined namespace and name
        """
        pass

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
        pass
