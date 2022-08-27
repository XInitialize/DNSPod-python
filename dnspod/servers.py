import functools
import json
from typing import Tuple, Any
from urllib.parse import urlencode

import requests


def name_call(log: bool = False):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            kwargs["__call__"] = function.__name__
            if log:
                ...
            return function(*args, **kwargs)

        return wrapper

    return decorator


class ServerBase:
    server_domain: str
    api_routes: dict
    login_token: str
    common_post: dict
    return_code: dict
    __slots__ = [
        "server_domain",
        "api_routes",
        "login_token",
        "common_post",
        "return_code"
    ]

    def __init__(self, *args, **kwargs):
        # routes
        self.server_domain = kwargs.get("server_domain", "https://dnsapi.cn").rstrip("/")
        self.api_routes = kwargs.get("api_routes", {
            "user_detail": "User.Detail",
            "domain_list": "Domain.List",
            "record_list": "Record.List",
            "record_ddns": "Record.Ddns"
        })
        # user
        self.login_token = kwargs.get("login_token")

        # server return
        self.return_code = {
            "-1": "login fail",
            "-2": "api usage out of limits",
            "-3": "illegal proxy (only proxy)",
            "-4": "not under the proxy (only proxy)",
            "-7": "no right at the interface",
            "-8": "blocked by too many failure login",
            "-85": "block by remote login",
            "-99": "try later for this application not open yet",
            "1": "Operation successful",
            "2": "only support POST request",
            "3": "unknown error",
            "6": "user id wrong (only proxy)",
            "7": "user not in your account (only proxy)",
            "83": "blocked at this account",
            "85": "current IP address not in allowed list for login in area protection"
        }
        self.return_code.update(kwargs.get("return_code", {}))
        # init
        self.common_post = {
            "login_token": self.login_token,
            "format": "json",
            "lang": "en"
        }

    def common_send(self, **kwargs) -> Tuple[bool, str, Any]:
        co_name = kwargs.pop("__call__")
        # noinspection PyBroadException
        try:
            payload = self.common_post.copy()
            payload.update(kwargs)
            req = requests.request("POST", self.server_domain + "/" + self.api_routes[co_name],
                                   headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                   data=urlencode(payload))
            ret = json.loads(req.text)
            code = ret["status"]["code"]
            flag = False
            if code == "1":
                flag = True
            return_msg = self.return_code.get(ret["status"]["code"], ret["status"]["message"])
            return flag, code + ": " + return_msg, ret
        except Exception as e:
            return False, "PYERROR: " + str(e), None

    @name_call(log=False)
    def user_detail(self, **kwargs) -> Tuple[bool, dict]:
        flag, info, ret = self.common_send(**kwargs)
        if not flag:
            print(info)
        return flag, ret

    @name_call(log=False)
    def domain_list(self, **kwargs) -> Tuple[bool, dict]:
        flag, info, ret = self.common_send(**kwargs)
        if not flag:
            print(info)
            return flag, ret
        return flag, ret["domains"]

    @name_call(log=False)
    def record_list(self, **kwargs) -> Tuple[bool, dict]:
        kwargs["domain_id"]: str
        flag, info, ret = self.common_send(**kwargs)
        if not flag:
            print(info)
            return flag, ret
        return flag, ret["records"]

    @name_call(log=False)
    def record_ddns(self, **kwargs) -> Tuple[bool, dict]:
        kwargs["value"]: str
        kwargs["sub_domain"]: str
        kwargs["domain_id"]: str

        kwargs["record_id"]: str
        kwargs["record_type"]: str
        kwargs["record_line"]: str
        flag, info, ret = self.common_send(**kwargs)
        if not flag:
            print(info)
            return flag, ret
        return flag, ret["record"]


class DnsPodServer(ServerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ddns(self, **kwargs):
        # ip_addr: str, i_record_id: str = None, i_name:str = None
        # get domain list
        flag, domain_list = self.domain_list()
        if not flag:
            print("get domain list fail. exit")
            return
        for domain in domain_list:
            print("domain:\n", {
                "id": domain["id"],
                "status": domain["status"],
                "grade": domain["grade"],
                "ttl": domain["ttl"],
                "name": domain["name"],
                "grade_ns": domain["grade_ns"],
                "remark": domain["remark"]
            })
            if domain["status"] == "enable":
                domain_id = domain["id"]
                # get record list
                flag, record_list = self.record_list(domain_id=str(domain["id"]))
                if not flag:
                    print(f"domain:{domain_id} can't get record. next")
                    continue

                # DDNS
                for record in record_list:
                    print("record:\n", {
                        "id": record["id"],
                        "ttl": record["ttl"],
                        "value": record["value"],
                        "status": record["status"],
                        "name": record["name"],
                        "line": record["line"],
                        "type": record["type"]
                    })
                    if record["status"] == "enable":
                        record_id = record["id"]
                        record_type = record["type"]
                        record_line = record["line"]
                        if (record_id == kwargs["record_id"]) & \
                                (record_type == kwargs["record_type"]) & \
                                (record_line == kwargs["record_line"]):
                            sub_domain = kwargs["sub_domain"]
                            value = kwargs["value"]
                            data = dict(
                                domain_id=domain_id,
                                record_id=record_id,
                                record_type=record_type,
                                value=value,
                                sub_domain=sub_domain,
                                record_line=record_line
                            )
                            flag, ddns_rst = self.record_ddns(**data)
                            if not flag:
                                print(f"ddns record {record_id} update failed.")
                            print(f"ddns record {record_id} update successfully.")
                            return
                        else:
                            print(f"record {record_id} not match aim.")
                    else:
                        print(f"record {record['id']} not enabled.")

    def static_ddns(self, **kwargs):
        self.record_ddns(**kwargs)
