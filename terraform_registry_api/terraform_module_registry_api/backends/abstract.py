from abc import ABC, abstractmethod


class AbstractBackend(ABC):
    """Abstract Class defining the backend structure"""

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def get_modules(self, namespace=None):
        """Get all modules in namespace provided.

        Args:
            namespace (str, optional): Namespace of modules. Defaults to None.

        Returns:
            json: JSON representation of the modules within the namespace
        """

    @abstractmethod
    def search_modules(self, query):
        """Search the module list based on the query.

        Args:
            query (str): Query string used for the search

        Returns:
            json: List of modules including details
        """

    @abstractmethod
    def get_latest_all_providers(self, namespace, name):
        """Get Latest versions for each deployed provider.

        Args:
            namespace (str): namespace for the version
            name (str): Name of the module

        Returns:
            json: List of all provders and latest version for
            defined namespace and name
        """

    @abstractmethod
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
