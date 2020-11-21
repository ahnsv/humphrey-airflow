import json
import pandas as pd
from datetime import datetime
from typing import Dict, List

import requests
import xmltodict


def rss_to_dataframe():
    """RSS 파싱 후 DataFrame을 리턴합니다.

    :return:
    """
    yeonny_blog_url = "https://rss.blog.naver.com/ye_onny.xml"

    def _get_xml_root_from_url(url: str) -> Dict:
        xml_in_text = requests.get(url).text
        return json.loads(json.dumps(xmltodict.parse(xml_input=xml_in_text)))

    def _xml_dict_to_dataframe(xml_input_dict: Dict,
                               columns: List[str] = ['category', 'title', 'link', 'pubDate', 'tag']) -> pd.DataFrame:
        items = []
        for item in xml_input_dict:
            items.append({
                **{column: item.get(column) for column in columns}
            })
        return pd.DataFrame(items)

    blog_items = _get_xml_root_from_url(url=yeonny_blog_url) \
        .get('rss') \
        .get('channel') \
        .get('item')
    df = _xml_dict_to_dataframe(xml_input_dict=blog_items)
    return df
