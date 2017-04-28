import requests

API_ROOT = "https://spending-api.us"

awards_endpoint = "/api/v1/awards"

def get_



def post_
 data =  {
      "verbose": true,
      "order": ["recipient__location__state_code", "-recipient__recipient_name"],
      "fields": ["fain", "total_obligation"],
      "exclude": ["recipient"],
      "filters": [
        {
          "field": "piid",
          "operation": "equals",
          "value": "SBAHQ16M0163"
        },
        {
          "combine_method": "OR",
          "filters": [...]
        }
      ]
    }

