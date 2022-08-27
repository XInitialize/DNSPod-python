from unittest import TestCase

from dnspod.servers import ServerBase


class TestServerBase(TestCase):
    def test_common_send(self):
        ...
        # pod_server = ServerBase(login_token=input("your login token:\n"))

    def test_user_detail(self):
        ...
        # pod_server = ServerBase(login_token=input("your login token:\n"))
        # print(pod_server.user_detail())

    def test_domain_list(self):
        ...
        pod_server = ServerBase(login_token=input("your login token:\n"))
        print(pod_server.domain_list())

    def test_record_list(self):
        ...
        # pod_server = ServerBase(login_token=input("your login token:\n"))
        # pod_server.record_list(domain_id=input("your domain id:\n"))

    def test_record_ddns(self):
        ...
        # pod_server = ServerBase(login_token=input("your login token:\n"))
        # data = dict(
        #     domain_id=input("domain_id: "),
        #     record_id=input("record_id: "),
        #     record_type=input("record_type: "),
        #     value=input("value: "),
        #     sub_domain=input("sub_domain: "),
        #     record_line=input("record_line: ")
        # )
        # pod_server.record_ddns(**data)
