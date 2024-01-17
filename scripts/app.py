from xml.etree import ElementTree
import requests
import os

from typing import Dict
from typing import Tuple
from typing import Optional

import ibrokers

host_name = "www.deribit.com"
deribit_endpoint_v2 = f"https://{host_name}/api/v2"
public_url = f"{deribit_endpoint_v2}/public"
private_url = f"{deribit_endpoint_v2}/private"


def authorize_with_credentials(client_id: str, client_secret: str) -> Tuple[Dict[str, str], str]:
    print(f"connecting with {client_id}")
    headers = {"Content-Type": "application/json"}
    auth_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    authentication = requests.get(f"{public_url}/auth", params=auth_params, headers=headers).json()
    headers["Authorization"] = f"Bearer {authentication['result']['access_token']}"
    refresh_token = authentication['result']['refresh_token']
    return headers, refresh_token

def authorize_refresh(refresh_token: str) -> Tuple[Dict[str, str], str]:
    print(f"refreshing authentication {refresh_token}")
    headers = {"Content-Type": "application/json"}
    auth_params = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    authentication = requests.get(f"{public_url}/auth", params=auth_params, headers=headers).json()
    headers["Authorization"] = f"Bearer {authentication['result']['access_token']}"
    new_refresh_token = authentication['result']['refresh_token']
    return headers, new_refresh_token

def run_get(target: str, params: Dict[str, str], headers: Dict[str, str], refresh_token: str=None) -> Optional[Tuple[Dict[str, str], str]]:
    response = requests.get(target, params=params, headers=headers)
    if response.status_code >= 399:
        error = response.json()
        if error['error']['code'] == 13009 and refresh_token:
            # re-run authorization
            new_headers, refresh_token = authorize_refresh(refresh_token)
            response = requests.get(target, params, new_headers)
        else:
            return None

    return response.json()['result'], headers, refresh_token

def main():
    ib_token = os.getenv("IB_FLEX_REPORT_TOKEN")
    ib_query_id = os.getenv("IB_FLEX_QUERY_ID")
    ib_report = ibrokers.load_ib_xml_report(ib_token, ib_query_id)
    error = ibrokers.check_report_error(ib_report)
    if error:
        raise ValueError(f'report in error: "{error[1]}" ({error[0]}), try again later')
    ib_positions = ibrokers.make_ib_records(ib_report)
    print(ib_positions)

if __name__ == "__main__":
    main()
