import re

pattern = re.compile(r'[A-Z]{3}[0-9]{3}')
msg = 'SUB001.amf_dns_show({{Group_AMF}}) '
result = pattern.search(msg).group(0)
print(result)
print(type(result))