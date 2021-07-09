#IBM TONE ANALYZER KEYS 
apikey = "sk1Ao6MG0VXyOk-p0Q9tFfCie1hfVcd_jMry3Jb1d3sm"
url = "https://api.us-east.tone-analyzer.watson.cloud.ibm.com/instances/d15d2672-79e3-46af-9c96-4d5ad8c5a149"
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
authenticator = IAMAuthenticator(apikey)
ta = ToneAnalyzerV3(version='2017-09-21', authenticator=authenticator)
ta.set_service_url(url)
chat = [
    {
    "text":"I feel great, it's sunny outside, and I've got all my work done.", 
    "user":"He who shall not be named"
    }, 
    {
    "text":"No!", 
    "user":"Whoa"
    }
]

data = ta.tone_chat(chat).get_result()
