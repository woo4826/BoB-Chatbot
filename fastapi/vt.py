# from splunklib.searchcommands import dispatch, GeneratingCommand, Option, Configuration
import virustotal3.core
import json
from config import config


VIRUS_API = config["VIRUS_API"]




def virustotal(query_item, query_type):
    """ virustotal api """
    result = {}
    if query_type == 'ip':
        virus_total = virustotal3.core.IP(VIRUS_API)
        result = virus_total.info_ip(query_item)
    elif query_type == 'domain':
        virus_total = virustotal3.core.Domians(VIRUS_API)
        result = virus_total.info_domain(query_item)
    elif query_type == 'url':
        virus_total = virustotal3.core.URL(VIRUS_API)
        result = virus_total.info_url(query_item)
    elif query_type == 'hash':
        virus_total = virustotal3.core.Files(VIRUS_API)
        result = virus_total.info_file(query_item)
    if 'data' in result and 'attributes' in result['data']:
        return result['data']['attributes']['last_analysis_stats']
    else:
        return result
