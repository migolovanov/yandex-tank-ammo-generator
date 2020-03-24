# Yandex tank ammo generator

This is a simple script to generate ammo file with various requests:
* set GET-arguments (from file or choose random)
* set random IP in some HTTP-header (e.g. X-Forwarded-For, X-Real-IP etc.)
* set random User-Agent (choose from file)
* add web attack to request (choose from file)

# Usage

```
usage: ammo-gen.py [-h] [-c COUNT] [-f FILE] [-H HOST]
                   [--header-connection {close,keep-alive}] [-u USER_AGENT]
                   [-a ATTACKS] [-p PARAMS] [-A ATTACK_PERCENT] [-i IP_HEADER]
                   [-P] [-U]

Ammo.txt generator for Yandex-Tank

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Ammo count (default: 100)
  -f FILE, --file FILE  Output file (default: ammo.txt)
  -H HOST, --hosts HOST
                        Hostnames used in Host header (default: 127.0.0.1,
                        comma-separated)
  --header-connection {close,keep-alive}
                        Connection header: close, keep-alive (default)
  -u USER_AGENT, --user-agent USER_AGENT
                        File with list of user_agents
  -a ATTACKS, --attacks ATTACKS
                        File with list of attack samples
  -p PARAMS, --params PARAMS
                        File with list of parameter names
  -A ATTACK_PERCENT, --attack-percent ATTACK_PERCENT
                        Percent of attacks (default: 100)
  -i IP_HEADER, --ip IP_HEADER
                        Specify header where to send IP-address from client
  -P, --random-params   Enable random parameters for attacks
  -U, --random-path     Enable random path for requests
```
## Example

Generate `ammo.txt` file:
```
python3 ammo-gen.py -H test.app -a attacks.txt -A 10 -P -U -u user_agents.txt -c 10 -i X-Real-IP
```

Run docker container:
```
/usr/bin/docker run --rm -v $(pwd):/var/loadtest -i direvius/yandex-tank -c ./load.yml
```

