# Before you can use the jobs API, you need to set up an access token.
# Log in to the Quantum Experience. Under "Account", generate a personal 
# access token. Replace 'PUT_YOUR_API_TOKEN_HERE' below with the quoted
# token string. Uncomment the APItoken variable, and you will be ready to go.

#MOVE UNDER CK
import os 

if 'CK_IBM_API_TOKEN' in os.environ:
    API_TOKEN = os.environ['CK_IBM_API_TOKEN']
else:
#    API_TOKEN = '227cf74859f37ff7b4612bdbd02fab3c287f23e40dda92e61a3f674f9d0c2c2d939955096fdf8a920dca4dcf8cf92c5b570cab5fb84d15d08301b921b26ca8f6'
    API_TOKEN='YOUR TOKEN HERE'

config = {
    'url': 'https://quantumexperience.ng.bluemix.net/api',

    # If you have access to IBM Q features, you also need to fill the "hub",
    # "group", and "project" details. Replace "None" on the lines below
    # with your details from Quantum Experience, quoting the strings, for
    # example: 'hub': 'my_hub'
    # You will also need to update the 'url' above, pointing it to your custom
    # URL for IBM Q.
    'hub': None,
    'group': None,
    'project': None
}
# some programs use different var name
APItoken = API_TOKEN

if 'APItoken' not in locals():
    raise Exception('Please set up your access token. See Qconfig.py.')
