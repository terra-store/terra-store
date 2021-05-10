import json

def get_versions(namespace, name, provider):
    versions = {
        "modules": [
            {
                "versions": [
                    {"version": "1.0.0"},
                    {"version": "1.1.0"},
                    {"version": "2.0.0"}
                ]
            }
        ]
    }
    return json.dumps(versions)

def download_version(namespace, name, provider, version):
    return "https://api.github.com/repos/{namespace}/terraform-{provider}-{name}/tarball/v{version}//*?archive=tar.gz".format(provider=provider, 
                                                                                                                       name=name,
                                                                                                                       version=version,
                                                                                                                       namespace = namespace)