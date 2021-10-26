# Requires pyshark + tshark
import pyshark
import urllib.parse
import re

# Solve approach by looking at the payload
# - Look through each http packet
# - Check the substring index that it's accessing
# - Whenever it changes, that means the previous packet was successful (i.e. found a character)
# - Therefore, we can add that to the flag

# We only care about the HTTP packets that originate from the hacker
capture = pyshark.FileCapture(
    "hacker_exfiltration.pcapng", display_filter="http && ip.src==10.0.4.10"
)

# Go through each packet
previous_index = "1"
previous_char = ""

# This regex will find the substring index and the character of the query
data_regex = re.compile(r".* SUBSTRING\(password, (\d*), 1\) = \"(.)\"; --")

flag = ""

for packet in capture:
    request_uri = urllib.parse.unquote_plus(packet.http.request_uri_query)
    index, character = data_regex.match(request_uri).groups()

    # If the index of the previous packet was different to the index used in this packet, then the previous character
    if previous_index != index:
        print("Found a character: {}".format(previous_char))
        flag += previous_char

    previous_index = index
    previous_char = character

print("Flag: {}".format(flag))
