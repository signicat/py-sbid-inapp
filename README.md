# py-sbid-inapp
### A functional example of sbid-inapp implementation

---

This is a **functional example** of sbid-inapp. It does not illustrate how to implement the method in a mobile app, it merely illustrates the API calls required to make the flow work as expected. It can be viewed as a jumping-off point for your app implementation.

This example follows the documentation at [Swedish BankID: How to integrate authentication with Swedish BankID from a native app](https://developer.signicat.com/id-methods/swedish-bankid/#how-to-integrate-authentication-with-swedish-bankid-from-a-native-app).

**Dependencies**:

* Python 3
* Built in: sys, random, time, urllib.parse
* [Requests](http://docs.python-requests.org/en/master/): HTTP for Humans.


### Flow

1. Call /authorize using method "sbid-inapp".
2. Poll collectUrl until progressStatus is COMPLETE.
3. Call completeUrl - the last redirect will contain CODE and STATE.
4. Call /token end-point as normal (using CODE we got in STEP 3).
5. Call /userinfo with access token. (optional)

Note: Step 1-3 should be performed in your mobile app. Step 4 & 5 should be performed at the web service hosted at your redirect URI.

### Application Usage
You need to change the variable ```cfg['NID']``` to a valid Swedish BankID test-user. This test-user has to be setup in the sbid mobile app on a mobile device! See [Swedish BankID: Test Information](https://developer.signicat.com/id-methods/swedish-bankid/#test-information).

Once you have changed this variable, you can run it with ```python3 sbid-inapp.py```.


### References
For general information about the Authentication service, please refer to [Get Started With Authentication](https://developer.signicat.com/documentation/authentication/get-started-with-authentication/).
