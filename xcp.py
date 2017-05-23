import urllib.request, json

_current_toplevel = "http://node1.rarepepe.party:4000"
_current_endpoint = _current_toplevel + "/api/"
_current_endpoint_user = "rpc"
_current_endpoint_password = "rpc"
seq_id = 0

def setup_pwd_mgr():
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, _current_toplevel, _current_endpoint_user, _current_endpoint_password);

    auth_handler = urllib.request.HTTPBasicAuthHandler(p)

    opener = urllib.request.build_opener(auth_handler)

    urllib.request.install_opener(opener)

def xcp_call(method, data):
    global seq_id
    params = json.dumps({
        "method": method,
        "params": data,
        "jsonrpc": "2.0",
        "id": seq_id
        }).encode('utf8')
    seq_id += 1
    req = urllib.request.Request(
        _current_endpoint, data=params,
        headers={'content-type': 'application/json'})
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        if "error" in data:
            raise data["error"]
        return data["result"]

setup_pwd_mgr()
