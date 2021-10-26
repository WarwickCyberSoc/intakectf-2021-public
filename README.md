# intakectf-2021-public
Challenge repository for IntakeCTF 2021. This repository contains most of the challenges that were used for Intake CTF 2021 as well as the challenge.jsons created by the challenge creators. Where challenges are missing, they've been excluded upon the author's request.

## Submitting Challenges
When submitting challenges, please follow the examples set inside base64/ and binaryfile/

Your folder can be named anything and must contain, at the very least, a challenge.json file with the following structure:

```json
{
    "title":"RIP Terminal",
    "description":"Binary files tend to ruin your terminal, maybe it's best to use some tools to help interpret them!",
    "author":"Josh",
    "points":10,
    "category":"Misc",
    "difficulty":"Easy",
    "hint":"grep is your friend!",
    "unlock_requirement": "What's this weird string?",
    "url":"",
    "file":"binary_data.txt",
    "tags":[
        "Tools"
    ],
    "education_resources":[
        "https://linux.die.net/man/1/grep"
    ],
    "flag":"WMG{BinArY_FilES_RuIn_TermINalS}",
    "flagType": "string",
    "disabled":false
}
```

If your challenge includes a file, please ensure this file is in the folder as well as the `file` parameter is set. `file`, `unlock_requirement` and `url` can be empty strings if you do not have a file or any hosted content. If your challenge should be hosted, please enter `SET ME LATER PLEASE` on the URL so we know to fill it in later. `unlock_requirement` should be the name of the challenge required to unlock this challenge. 

Please include the script of the challenge, or the Netkit lab which generated the pcap, or the web files if it's a web challenge etc. In the event we need to recreate flags, we need to be able to generate them as easily as possible. For some challenges this may not be possible, but some instructions on how you did generated would be appreciated.

Supported difficulties:
- `Very Easy`
- `Easy`
- `Medium`
- `Hard`
- `Very Hard`

If your app contains multiple challenges, you can use a `challenges.json` file which is an array of challenges in JSON.

There are two supported flag types:
- string
- location

String flags are in the style of "WMG{AAAAAA}". 
Location flags are in the style of "43.414,6.411", corresponding to latitude/longitude.