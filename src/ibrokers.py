from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree
import requests


class RowData:
    def __init__(self, row: Dict[str, str]):
        self._row = row

    def __repr__(self):
        return repr(self._row)


def load_ib_xml_report(ib_token: str, ib_query_id: str) -> ElementTree:
    ib_flex_url = f"https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={ib_token}&q={ib_query_id}&v=3"
    ib_response = requests.get(ib_flex_url)
    ib_report_location = ElementTree.fromstring(ib_response.content)
    ib_report_reference_code = ib_report_location.find('ReferenceCode').text
    ib_report_base_url = ib_report_location.find('Url').text
    ib_report_url = f"{ib_report_base_url}?t={ib_token}&q={ib_report_reference_code}&v=3"
    ib_report = requests.get(ib_report_url)
    return ElementTree.fromstring(ib_report.content)

def check_report_error(report_tree: ElementTree) -> Optional[Tuple[int, str]]:
    error_code = report_tree.find('.//ErrorCode')
    if error_code is not None:
        error_message = report_tree.find('.//ErrorMessage')
        return int(error_code.text), error_message.text
    
    return None

def make_ib_records(report_tree: ElementTree) -> List[RowData]:
    ib_records = []
    for position in report_tree.findall('.//OpenPosition'):
        ib_records.append(RowData(position.attrib))
    return ib_records
