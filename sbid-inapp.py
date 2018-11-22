import sys
import requests
import random
from time import sleep
import urllib.parse as urlparse

""" Needs to be a Swedish BankID test-user setup with the mobile app!
    See https://developer.signicat.com/id-methods/swedish-bankid/#test-information
    Format: yyyymmddnnnn
"""
cfg = {'NID': ''}
if str.isdigit(cfg['NID']) is False or len(cfg['NID']) is not 12:
    print("Please change the variable cfg['NID'] to a valid Swedish BankID test-user!")
    sys.exit()

# STEP 1: Call authorize using method "sbid-inapp"
headers1 = {'Accept': 'application/json'}
url1 = ('https://preprod.signicat.com/oidc/authorize?response_type=code&scope=openid+profile&client_id=demo-inapp&redirect_uri=https://example.com/redirect&acr_values=urn:signicat:oidc:method:sbid-inapp&state={}&login_hint=subject-{}'
    .format(''.join(random.choice('ABCDEF0123456789') for _ in range(8)), cfg['NID']))
r1 = requests.get(url1, headers=headers1)
jar = r1.cookies # !IMPORTANT! Saves all cookies - to be used in future requests.
res1 = r1.json()
print("Authorize Response: {}".format(res1))

# STEP 2: Poll collectUrl until progressStatus=COMPLETE
url2 = res1['collectUrl'] + '?orderRef=' + res1['orderRef']
PS = {'progressStatus': None}
print("\nPolling...")
while 'COMPLETE' not in PS: # Check if COMPLETE, if not sleep 5s and check again.
    sleep(5)
    res2 = requests.get(url2, headers=headers1, cookies=jar).json()
    PS = res2['progressStatus']
    print("  -- Status: {}".format(PS))
print("collectUrl Response: {}".format(res2))

# STEP 3: Call completeUrl - the last redirect will contain CODE and STATE.
url3 = res2['completeUrl']
r3 = requests.get(url3, cookies=jar) # requests.get() method automatically follows redirects.
res3 = r3.history[-1].headers['Location'] # Get the LAST of the redirects. This contains code and state.
res3_params = urlparse.parse_qs(urlparse.urlparse(res3).query)
print("\nFinal redirect from completeURL: {}".format(res3))
print("  -- CODE: '{}'".format(res3_params['code'][0]))
print("  -- STATE: '{}'".format(res3_params['state'][0]))

# STEP 4: Call /token end-point as normal (using CODE we got in STEP 3)
headers2 = {'Authorization': 'Basic ZGVtby1pbmFwcDptcVotXzc1LWYyd05zaVFUT05iN09uNGFBWjd6YzIxOG1yUlZrMW91ZmE4'}
payload = {
    'client_id': 'demo-inapp',
    'redirect_uri': 'https://example.com/redirect',
    'grant_type': 'authorization_code',
    'code': res3_params['code'][0]
}
res4 = requests.post('https://preprod.signicat.com/oidc/token', data=payload, headers=headers2).json()
print("Normal auth Response: {}".format(res4))
token = res4['access_token'] # Access token!
print("\nAccess Token: {} ... ({} Bytes)".format(token[:33], len(token)))

# STEP 5 (optional): Call /userinfo with access token.
headers3 = {'Authorization': 'Bearer ' + token}
res5 = requests.get('https://preprod.signicat.com/oidc/userinfo', headers=headers3).json()
print("UserInfo Response: {}".format(res5))