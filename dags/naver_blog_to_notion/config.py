from dataclasses import dataclass


@dataclass
class MinioConfig:
    minio_host: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str


@dataclass
class Config:
    minio_config: MinioConfig
