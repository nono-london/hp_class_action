from json import loads
from typing import Dict, Union, List
from urllib.error import URLError
from urllib.request import Request, urlopen

from hp_class_action.hp_database.mdb_handlers import (fetch_query)


def get_visitors_info() -> List[Dict]:
    """Returns True if csv row has already been uploaded to mdb"""
    sql_query = """
        SELECT *
        FROM website_visitors_info
        ORDER BY visit_datetime    
    """
    parameters = None
    results = fetch_query(sql_query=sql_query, variables=parameters)

    return results


def get_json_request(url):

    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print("The server couldn't fulfill the request.")
            print('Error code: ', e.code)
        return None

    # read JSOn data
    # https://stackoverflow.com/questions/32795460/loading-json-object-in-python-using-urllib-request-and-json-modules
    encoding = response.info().get_content_charset('utf-8')
    data = response.read()
    response = loads(data.decode(encoding))
    return response


def get_arin_info(ip_address: str) -> Union[None, Dict]:
    """https://www.arin.net/resources/registry/whois/rdap/"""
    """ same without using requests lib
        https://github.com/rush-dev/arin-whois/blob/master/whois.py
    """
    response_format = "json"
    url = f'http://whois.arin.net/rest/ip/{ip_address}.{response_format}'
    print(url)
    ip_response = get_json_request(url=url)

    print(ip_response.get('net').get('resources').get("limitExceeded"))
    # IP network categories
    start_address = ip_response['net']['startAddress']['$']
    end_address = ip_response['net']['endAddress']['$']
    handle = ip_response['net']['handle']['$']
    name = ip_response['net']['name']['$']
    org_name = ip_response['net']['orgRef']['@name']
    org_handle = ip_response['net']['orgRef']['@handle']
    last_updated = ip_response['net']['updateDate']['$']
    rest_link = ip_response['net']['ref']['$']

    # Second GET request with organization name

    url = f'https://whois.arin.net/rest/org/{org_handle}.{response_format}'
    org_response = get_json_request(url=url)

    # Organization categories

    city = org_response['org']['city']['$']
    postal = org_response['org']['postalCode']['$']
    country = org_response['org']['iso3166-1']['code2']['$']
    org_last_updated = org_response['org']['updateDate']['$']
    org_rest_link = org_response['org']['ref']['$']

    # Try statements to catch commonly blank fields and differences in indexing on ARIN's side

    try:
        cidr = ip_response['net']['netBlocks']['netBlock']['cidrLength']['$']

    except TypeError:
        cidr = ip_response['net']['netBlocks']['netBlock'][0]['cidrLength']['$']

    try:
        net_type = ip_response['net']['netBlocks']['netBlock']['description']['$']

    except TypeError:
        net_type = ip_response['net']['netBlocks']['netBlock'][0]['description']['$']

    try:
        parent_name = ip_response['net']['parentNetRef']['@name']
        parent_handle = ip_response['net']['parentNetRef']['@handle']

    except KeyError:
        parent_name = ''
        parent_handle = ''

    try:
        origin_as = ip_response['net']['originASes']['originAS'][0]['$']

    except KeyError:
        origin_as = ''

    try:
        reg_date = ip_response['net']['registrationDate']['$']

    except KeyError:
        reg_date = ''

    try:
        org_reg_date = org_response['org']['registrationDate']['$']

    except KeyError:
        org_reg_date = ''

    try:
        state = org_response['org']['iso3166-2']['$']

    except KeyError:
        state = ''

    try:
        street = org_response['org']['streetAddress']['line']['$']

    except TypeError:
        street = org_response['org']['streetAddress']['line'][0]['$']

    # Output to terminal
    print(f'You searched for: {ip_address}\n')
    print('Network')
    print(f'NetRange:         {start_address} - {end_address}')
    print(f'CIDR:             {start_address}/{cidr}')
    print(f'Name:             {name}')
    print(f'Handle:           {handle}')
    print(f'Parent:           {parent_name} ({parent_handle})')
    print(f'NetType:          {net_type}')
    print(f'OriginAS:         {origin_as}')
    print(f'Organization:     {org_name} ({org_handle})')
    print(f'RegistrationDate: {reg_date}')
    print(f'LastUpdated:      {last_updated}')
    print(f'RESTful Link:     {rest_link}\n')
    print('Organization')
    print(f'Name:             {org_name}')
    print(f'Handle:           {org_handle}')
    print(f'Street:           {street}')
    print(f'City:             {city}')
    print(f'State/Province:   {state}')
    print(f'PostalCode:       {postal}')
    print(f'Country:          {country}')
    print(f'RegistrationDate: {org_reg_date}')
    print(f'LastUpdated:      {org_last_updated}')
    print(f'RESTful Link:     {org_rest_link}')


if __name__ == '__main__':
    get_visitors_info()
    print(get_arin_info(ip_address="172.58.187.155"))
