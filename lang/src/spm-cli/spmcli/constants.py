
PACKAGE_JSON_PATH = "package.json"
SPM_PACKAGES_PATH = "spm_packages"

IS_REMOTE = True

LOCAL_BASE_URL = "http://localhost" #http://host.docker.internal"
SEARCH_INDEX_API_URL = "https://spm.bjelicaluka.com/api" if IS_REMOTE else f"{LOCAL_BASE_URL}:3000/api"
IPFS_NODE_URL = "https://gw.spm.bjelicaluka.com/ipfs" if IS_REMOTE else f"{LOCAL_BASE_URL}:9090/ipfs"
