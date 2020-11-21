import json
from datetime import datetime
from io import BytesIO
from typing import Dict, List

import pandas as pd
import requests
import xmltodict

from dags.common import datetime_to_ds


def rss_to_dataframe(start_date: datetime, **kwargs) -> None:
    """RSS 파싱 후 DataFrame을 리턴합니다.

    :return:
    """
    yeonny_blog_url = "https://rss.blog.naver.com/ye_onny.xml"
    task_name = rss_to_dataframe.__name__
    config = kwargs['params']['config']

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

    def _write_df_to_minio_in_csv(df: pd.DataFrame, minio_config: Dict) -> None:
        from minio import Minio
        minio_client = Minio(minio_config.get('host'),
                             access_key=minio_config.get('access_key'),
                             secret_key=minio_config.get('secret_key'),
                             secure=False)
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(minio_config.get('bucket_name'),
                                f'{task_name}/{datetime_to_ds(start_date)}/rss.csv',
                                data=csv_buffer,
                                length=len(csv_bytes),
                                content_type='application/csv')

    blog_items = _get_xml_root_from_url(url=yeonny_blog_url) \
        .get('rss') \
        .get('channel') \
        .get('item')
    df = _xml_dict_to_dataframe(xml_input_dict=blog_items)
    if df.empty:
        raise ValueError('Dataframe is empty')

    _write_df_to_minio_in_csv(df=df, minio_config=config.get('minio_config'))
