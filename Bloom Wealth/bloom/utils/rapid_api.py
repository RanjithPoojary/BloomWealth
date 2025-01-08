import requests
from flask import current_app

def get_mutual_fund_data(**query_params):
    url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"
    headers = {
        "X-RapidAPI-Key": current_app.config['RAPID_API_KEY'],
        "X-RapidAPI-Host": current_app.config['RAPID_API_HOST']
    }
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as ex:
        current_app.logger.error(f"Error fetching mutual fund data: {ex}")
        return {"error": "Failed to fetch mutual fund data", "details": str(ex)}

def get_fund(id, **query_params):
    url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"
    headers = {
        "X-RapidAPI-Key": current_app.config['RAPID_API_KEY'],
        "X-RapidAPI-Host": current_app.config['RAPID_API_HOST']
    }
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        for fund in response.json():
            if fund["Unique_No"] == id:
                return fund
        return ""
    except requests.exceptions.RequestException as ex:
        current_app.logger.error(f"Error fetching mutual fund data: {ex}")
        return {"error": "Failed to fetch mutual fund data", "details": str(ex)}

def get_fund_houses(funds):
    fund_family = {fund["AMC_Code"] for fund in funds}
    return sorted(fund_family)
