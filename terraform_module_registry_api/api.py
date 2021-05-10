def list_versions(namespace, name, provider):
    print(namespace)
    return """{
   "modules": [
      {
         "versions": [
            {"version": "1.0.0"},
            {"version": "1.1.0"},
            {"version": "2.0.0"}
         ]
      }
   ]
}"""

def download_version(namespace, name, provider, version):
    print(version)
    return """{
   "modules": [
      {
         "versions": [
            {"version": "1.0.0"},
            {"version": "1.1.0"},
            {"version": "2.0.0"}
         ]
      }
   ]
}"""