import requests

class APIClient:
    """ Handle API calls for DRY code """
    def __init__(self,url,headers):
        self.url=url
        self.headers=headers
        
    def api_call(self, endpoint, **querystring):
        """ Make call to API with url and headers defined on class. Specify endpoint as string (no leading /) and pass in querystring keys and values to complete the request. Assumes API returns 'response'. """
        url = f"{self.url}{endpoint}"
        headers=self.headers
        querystring=querystring
        res = requests.request("GET", url, headers=headers, params=querystring)
        resjson=res.json()
        response = resjson['response']
        return response
    
    
api_football = APIClient(
    url="https://api-football-v1.p.rapidapi.com/v3/",
    headers={
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "0c53816d30mshaf76a97a06df018p1a51f7jsn5f2149fe7ff0"
    }) 