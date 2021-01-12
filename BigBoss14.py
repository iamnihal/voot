import requests
    
i = 1
j = 1
user_email = ""
password = "mypassword" #Change this
def login_voot():
    global j
    global i
    global user_email
    user_email = f'myemail{i}@gmail.com'  #Change this
    i += 1
    print(f'[+] {j} vote done!!')
    j += 1
    print(f'[+] Email:- {user_email}')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://voting.voot.com',
            'Connection': 'keep-alive',
            'Referer': 'https://voting.voot.com/vote/ec324230-02f2-11eb-bf8c-d128fef771cc?&platform=web',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers',
        }
        login_data = '{"type":"traditional","deviceId":"Windows NT 10.0","deviceBrand":"PC/MAC","data":{"email":"' +str(user_email)+ '","password":"' +str(password)+ '"}}'
        response = requests.post('https://us-central1-vootdev-stg.cloudfunctions.net/usersV3/v3/login', headers=headers, data=login_data)
        login_data_json = response.json()
        return login_data_json
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)

    # Extract Access Token
def extract_access_token(login_data_json):
    try:
        print('[+] Access Token Extracted')
        access_token = login_data_json["data"]["authToken"]["accessToken"]
        return access_token
    except KeyError:
        print("KeyError exception. Ignoring")
    except TypeError:
        print("TypeError exception. Ignoring")
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)

def extract_user_id(login_data_json):
    try:
        print('[+] User Id Extracted')
        user_id = login_data_json["data"]["uId"]
        return user_id
    except KeyError:
        print("KeyError exception. Ignoring")
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)

def generate_jwt_token(user_id, access_token):
    try:
        headers = {
            'Referer': 'https://voting.voot.com/vote/ec324230-02f2-11eb-bf8c-d128fef771cc?&platform=web',
            'Deviceinfo': 'Windows NT 10.0',
            'Lastloginprovider': 'Traditional',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://voting.voot.com',
            'Uid': f'{user_id}',
            'Accesstoken': f'{access_token}',
            'Buildnumber': 'v0',
        }
        # Getting JWT Authentication Token
        response = requests.get('https://us-central1-vootdev.cloudfunctions.net/usersV3/v3/getAuthKey', headers=headers)
        get_auth_token_data = response.json()
        return get_auth_token_data
    except KeyError:
        print("KeyError exception. Ignoring")
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    
    
def extract_auth_token(get_auth_token_data):
    # Extracting JWT Authentication Token
    try:
        print("[+] JWT Authentication Token Extracted")
        auth_token = get_auth_token_data["accessToken"]
        return auth_token
    except KeyError:
        print("KeyError exception. Ignoring")
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)

def verify_auth_token(auth_token, user_id):
    print("[+] Verifying JWT Token")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'Origin': 'https://voting.voot.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        verify_data = '{{"token":"{0}"}}'.format(auth_token)
        response = requests.post('https://voting-api.voot.com/v1/verifyjwttoken', headers=headers, data=verify_data)
        verify_data_json = response.json()
        uid_verify = verify_data_json["UID"]
        if uid_verify == user_id:
            return "[+] Token Verified Successfully"
        else:
            return "[+] Verification Failed"
    except KeyError:
        print("KeyError occured. Ignoring")
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)

def voting(cname, cid, user_id):
    print("[+] Doing Voting, Please Wait")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'Origin': 'https://voting.voot.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        
        final_voting_data = '{{"showId":"ec324230-02f2-11eb-bf8c-d128fef771cc","showName":"Bigg Boss 14","categoryId":"","categoryName":"","contestantId":"{0}","contestantName":"{1}","cycleId":"06718c80-4ea4-11eb-a43a-79863c893531","userId":"{2}","userName":"","userEmail":"{3}","region":"in","ip":"202.142.67.203","loginProvider":"Traditional"}}'.format(cid, cname, user_id, user_email)
        response = requests.post('https://voting-api.voot.com/v1/addvote', headers=headers, data=final_voting_data)
        return response
    except requests.exceptions.ConnectionError:
        print("Connection Refused!!")
    except AttributeError:
        print("Attribute Error. Ignore")
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except KeyError:
        print("[+] Escaping this Email")
        raise
    
def main():
    login = login_voot()
    access_token = extract_access_token(login)
    user_id = extract_user_id(login)
    jwt_token = generate_jwt_token(user_id, access_token)
    token = extract_auth_token(jwt_token)
    verify = verify_auth_token(token, user_id)
    print(verify)
    vote = voting("Aly Goni", "f6108f30-2dab-11eb-8b50-a705ce356216", user_id) #Change this - (Only Contestant name and Contestant Id )
    print(vote.text)
    
for _ in range(10000):
    main()
