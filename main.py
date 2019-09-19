from flask import Flask, request, redirect, render_template, Response
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import requests
import json
import uuid

# init Flask 
app = Flask(__name__)
bootstrap = Bootstrap(app)
CORS(app, supports_credentials = True)
'''
@app.route('/', methods=['GET'])
def test():
    return "it works"
'''

@app.route('/ThirdParty/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ThirdParty/getUsagePoint', methods=['GET'])
def get_usage_point():
    access_token = request.args.get('access_token')
    resourceURI = request.args.get('resourceURI')
    if(access_token == None or resourceURI == None):
        return "Missing parameters", 400
        
    hed = {'Authorization': 'Bearer ' + access_token}
    url = resourceURI #+ "/UsagePoint"
    print(hed)
    res = requests.get(url, headers=hed)
    print(res.text)
    return Response(str(res.text), mimetype='application/atom+xml')
    #return str(res.text)
    
@app.route('/ThirdParty/login', methods=['GET'])
def login():
    return "welcome to yochien third party login"

@app.route('/ThirdParty/redirect', methods=['GET'])
def redirect_to_data_custodian():
    return redirect("http://140.121.196.23:6001/DataCustodian/RetailCustomer/ScopeSelectionList?scope=FB=1_3_4_5_6_7_8_9_10_11_29_12_13_14_15_16_17_18_19_27_28_32_33_34_35_37_38_39_40_41_44;IntervalDuration=3600;BlockDuration=monthly;HistoryLength=13&scope=FB=1_3_4_5_13_14_39;IntervalDuration=3600;BlockDuration=monthly;HistoryLength=13&scope=FB=1_3_4_5_13_14_15_39;IntervalDuration=900;BlockDuration=monthly;HistoryLength=13&ThirdPartyID=third_party_yochien", code=302)

@app.route('/ThirdParty/RetailCustomer/ScopeSelection', methods=['GET'])
def scope_selection():
    return render_template('scope.html')
    #return "welcome to yochien third party ScopeSelection"
    

@app.route('/ThirdParty/RetailCustomer/ScopeSelection', methods=['POST'])
def scope_selection_post():
    client_id = "third_party_yochien"
    redirect_uri = "http://140.121.196.23:6012/ThirdParty/espi/1_1/OAuthCallBack"
    random_state = str(uuid.uuid1())
    return redirect("http://140.121.196.23:6001/DataCustodian/oauth/authorize?client_id="+ client_id +"&redirect_uri="+ redirect_uri +"&response_type=code&scope=FB=1_3_4_5_6_7_8_9_10_11_29_12_13_14_15_16_17_18_19_27_28_32_33_34_35_37_38_39_40_41_44;IntervalDuration=3600;BlockDuration=monthly;HistoryLength=13&state="+ random_state, code=302)
    #return "welcome to yochien third party scope_selection_post"


@app.route('/ThirdParty/espi/1_1/OAuthCallBack', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    redirect_uri  = "http://140.121.196.23:6012/ThirdParty/espi/1_1/OAuthCallBack"
    access_token = ""
    '''
    return redirect("http://140.121.196.23:6001/DataCustodian/oauth/authorize?redirect_uri=http://140.121.196.23:6012/ThirdParty/espi/1_1/OAuthCallBack&code="+ code +"&grant_type=authorization_code", code=302)
    '''
    try:
        access_token = requests.get("http://140.121.196.23:6001/DataCustodian/oauth/token?redirect_uri="+ redirect_uri +"&code="+ code +"&grant_type=authorization_code",auth=requests.auth.HTTPBasicAuth(
                          'third_party_yochien',
                          'secret'))
        print(access_token.text)
    except:
        pass
    #print(code, state, access_token)
    return render_template('token.html', data = json.loads(access_token.text))
    #return str(request.headers)+"welcome to yochien third party oauth_callback"
    

@app.route('/ThirdParty/RetailCustomer/<retailCustomerId>/DataCustodianList', methods=['GET'])
def data_custodian_list(retailCustomerId):
    return "welcome to yochien third party DataCustodianList"

@app.route('/ThirdParty/espi/1_1/Notification', methods=['GET'])
def notification():
    return "welcome to yochien third party notification"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=6012, debug=True)
