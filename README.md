# DNSPod-python
Tencent Cloud(DNSPod), DDNS refresh solution（support Openwrt）
# Usage
## Dependency
```bash
python3 -m pip install pyyaml requests
```
## In use
Clone this repo
```bash
git clone https://github.com/XInitialize/DNSPod-python.git && cd DNSPod-python
```
## DDNS
At first, you should replace '...' in [ddns.yaml](https://github.com/XInitialize/DNSPod-python/blob/main/ddns.yaml) to your own settings.
Next, use ``python3 dnspod.py ddns -y ddns.yaml`` wo refresh your dns record.

## More
In file [tests/test_servers.py](https://github.com/XInitialize/DNSPod-python/blob/main/tests/test_servers.py), we provide some basic usage sample for testing interfaces, you can uncomment these methods and try yourself.
