# tufts-meals: meal swipe and JumboCash balances 
Instead of trudging over to https://www.jumbocash.net, just check your 
remaining meal swipes and JumboCash balance from the command line. 

## Requirements
- You'll need BeautifulSoup4 and Requests, so go ahead and `pip install -r requirements.txt` to take care of that.

## Example
The login process may take a few seconds (remember that weird loading page on the jumbocash.net site?). A typical dialog should look something like this (except maybe with less JumboCash):
```
Tufts ID #: XXXXXXX
Password: 
Remaining Swipes: 122
JumboCash Balance: $1000000000.00
```
