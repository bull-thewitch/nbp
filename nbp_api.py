import http.client
import json
import ssl
import socket

class NBPAPI:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("api.nbp.pl", context = ssl._create_unverified_context())
        self.hdrs = {"Accept": "application/json"}
        self.ERR_URL = -2
        self.ERR_CODE = -1
        self.ERR_RESP = -3
        self.ERR_ASCII = -4
        self.ERR_STRUCT = -5

    def destructor(self):
        self.conn.close()

    def get_current_rate(self, code):
        try:
            self.conn.request("GET", "/api/exchangerates/rates/A/{}/".format(code), headers = self.hdrs)
        except socket.error:
            return self.ERR_URL
        try:
            r1 = self.conn.getresponse()
            data1 = r1.read()
        except:
            return self.ERR_RESP
        try:
            data_str = data1.decode("ascii")
        except UnicodeDecodeError:
            return self.ERR_ASCII
        try:
            json_data = json.loads(data_str)
        except json.decoder.JSONDecodeError: 
            return self.ERR_CODE
        return float(json_data["rates"][0].get("mid"))

    def get_rate_for_date(self, code, date):
        try:
            self.conn.request("GET", "/api/exchangerates/rates/A/{}/{}/".format(code, date), headers = self.hdrs)
            json_data = json.loads(self.conn.getresponse().read().decode("ascii"))
        except json.decoder.JSONDecodeError: 
            return self.ERR_CODE
        except UnicodeDecodeError:
            return self.ERR_ASCII
        except socket.error:
            return self.ERR_URL
        except:
            return self.ERR_RESP

        return float(json_data["rates"][0].get("mid"))

    def get_rate_from_date_to_date(self, code, startDate, endDate):
        try:
            self.conn.request("GET", "/api/exchangerates/rates/A/{}/{}/{}/".format(code, startDate, endDate), headers = self.hdrs)
            json_data = json.loads(self.conn.getresponse().read().decode("ascii"))
        except json.decoder.JSONDecodeError: 
            return self.ERR_CODE
        except UnicodeDecodeError:
            return self.ERR_ASCII
        except socket.error:
            return self.ERR_URL
        except:
            return self.ERR_RESP

        res = {}
        if json_data.get("rates") != None and hasattr(json_data["rates"], '__iter__'):
            for d in json_data["rates"]:
                if d.get("effectiveDate") != None and d.get("mid") != None: 
                    res[d["effectiveDate"]] = d["mid"]    
                else:
                    return self.ERR_STRUCT        
            res = {d["effectiveDate"]:d["mid"] for d in json_data["rates"]}
            return res
        else: 
            return self.ERR_STRUCT
                
    
        #return json_data["rates"][0]["mid"]




            


