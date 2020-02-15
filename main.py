import requests
from colorama import Fore, init
from threading import Thread
import random, time, names, string, json, os
from threading import Lock
from random import choice


s_print_lock = Lock()


def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


def log(tag, text):
    # Info tag
    if(tag == 'i'):
        s_print("[INFO] " + str(text))
    # Error tag
    elif(tag == 'e'):
        s_print("[ERROR] " + str(text))
    # Success tag
    elif(tag == 's'):
        s_print("[SUCCESS] " + str(text))

def get_proxy(proxy_list):
    '''
    (list) -> dict
    Given a proxy list <proxy_list>, a proxy is selected and returned.
    '''
    # Choose a random proxy
    proxy = random.choice(proxy_list)

    m = proxy.strip().split(':')
    if len(m) == 4:
        base = f"{':'.join(m[:2])}"  # ip:port
        if len(m) == 4:
            proxies = {
                'http': f"http://{':'.join(m[-2:])}@{base}" + '/',
                'https': f"http://{':'.join(m[-2:])}@{base}" + '/'
            }
    else:
        # Set up the proxy to be used
        proxies = {
            "http": str(proxy),
            "https": str(proxy)
        }
    # Return the proxy
    return proxies

def read_from_txt(path):
    '''
    (None) -> list of str
    Loads up all sites from the sitelist.txt file in the root directory.
    Returns the sites as a list
    '''
    # Initialize variables
    raw_lines = []
    lines = []

    # Load data from the txt file
    try:
        f = open(path, "r")
        raw_lines = f.readlines()
        f.close()

    # Raise an error if the file couldn't be found
    except Exception:
        log('e', Fore.RED + "Couldn't locate <" + path + ">.")

    if (len(raw_lines) == 0):
        log('e', Fore.RED + "No data in <" + path + ">.")

    # Parse the data
    for line in raw_lines:
        lines.append(line.strip("\n"))

    # Return the data
    return lines

def gen_phone(international_format=False):
    first = str(random.randint(2, 9)).zfill(1)
    second = str(random.randint(1, 9)).zfill(2)
    last = (str(random.randint(1, 9)).zfill(2))
    b = (str(random.randint(1, 9)).zfill(2))
    a = (str(random.randint(1, 9)).zfill(2))

    calling_code = "0" if not international_format else "+33"

    return f'{calling_code}{first}{second}{last}{b}{a}'

ua = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
]

def genacc(proxy_list, s):

    runs = 0
    try:
        while runs < 5:

            #client info --------------------------------------------------------------------
            config = json.loads(open('config.json').read())
            fname = names.get_first_name()
            lname = names.get_last_name()
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            addy1 = random.choice(string.ascii_letters[0:4]).upper() + random.choice(string.ascii_letters[0:26]).upper() + random.choice(string.ascii_letters[0:26]).upper() + random.choice(string.ascii_letters[0:26]).upper() + " " + config['addressLine1']
            addy2 = config['addressLine2']
            addy3 = config['addressLine3']
            city = config['city']
            country = config['country_id']
            country_code = config['country_code']
            email = fname + lname + str(random.randint(1, 1000)) + config['catchall']
            state_id = config['state_id']
            state = config['state']
            zipcode = config['zipcode']
            phone = gen_phone()
            #--------------------------------------------------------------------------------
            
            ua1 = choice(ua)
            
            if len(proxy_list) > 0:
                s.proxies = get_proxy(proxy_list)

            data = {"name": fname + " " + lname, "username": email, "email": email, "password": password, "countryCode": country_code, "receiveNewsletters": False}
            headers = {
                'Host': 'www.off---white.com',
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://www.off---white.com',
                'user-agent': ua1,
                'content-type': 'application/json;charset=UTF-8',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'referer': 'https://www.off---white.com/',
            }

            r1 = s.post('https://www.off---white.com/en-de/api/account/register', headers=headers, data=json.dumps(data), timeout=8)
            #print(data)
            #print(r1.content)
            if r1.status_code != 200:
                log('e', Fore.RED + "Failed creating account")
                time.sleep(1)
                runs += 1
                continue 
            

            log('s', Fore.GREEN + "Account Created now adding address..")

            if country_code == "US":
                data = {"firstName":fname,"lastName":lname,"phone":phone,"country":{"id":country},"addressLine1":addy1,"addressLine2":addy2,"addressLine3":addy3,"city":{"name":city},"state":{"id":state_id},"zipCode":zipcode}
            else:
                data = {"firstName":fname,"lastName":lname,"phone":phone,"country":{"id":country},"addressLine1":addy1,"addressLine2":addy2,"addressLine3":addy3,"city":{"name":city},"state":{"name":state},"zipCode":zipcode}

            r2 = s.post('https://www.off---white.com/en-us/api/addressbook', headers=headers, json=data, timeout=8)
            
            if r2.status_code != 200:
                log('i', Fore.RED + "Failed added address to account")
                time.sleep(1)
                runs += 1
                continue
            else:
                log('s', Fore.GREEN + "Address added successfully, saving account in file [%s]" % email)
                with open("off_white_accounts.txt", 'a') as account:
                    account.write(email + ':' + password + '\n')
                account.close()
                break

        if runs == 5:
            log('e', Fore.YELLOW + "Failed requesting site 5 times, quitting...") 

    except (requests.exceptions.ProxyError, requests.exceptions.SSLError):
        log('e', Fore.RED + "Proxy is banned")
        genacc(proxy_list, s)

    except Exception as e:
        log('i', Fore.RED + str(e))
        pass

def main():
    requests.packages.urllib3.disable_warnings()
    #---------------------------------------------#
    try:
        tc = int(input('How many accounts ? -> '))
    except ValueError:
        log('i', Fore.RED + "Please input a number")
        input("Press any key to exit")
        os._exit(0)
    #---------------------------------------------#
    try:
        proxies = read_from_txt("proxies.txt")
    except Exception:
        log('i', Fore.RED + "Proxy file is empty, using localhost")
 
    #---------------------------------------------#

    log('i', Fore.CYAN + str(len(proxies)) + " proxies loaded.")
    log('i', Fore.CYAN + "Starting Account gen")

    threads = []

    for i in range(tc):
        s = requests.session()
        t = Thread(target=genacc, args=(proxies, s))

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    init(autoreset=True)
    main()
