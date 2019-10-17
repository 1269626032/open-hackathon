# -*- coding: utf-8 -*-
"""
This file is covered by the LICENSING file in the root of this project.
"""
import os
# "javascript" section for javascript. see @app.route('/config.js') in app/views.py

# oauth constants
QQ_OAUTH_STATE = "openhackathon"  # todo state should not be constant. Actually it should be unguessable to prevent CSFA

HACKATHON_SERVER_ENDPOINT = "http://localhost:15000"

MONGODB_HOST = os.environ["DB_SERVER"]
MONGODB_PORT = int(os.environ["DB_PORT"])
MONGODB_DB = "hackathon"

Config = {
    "environment": "local",
    "endpoint": HACKATHON_SERVER_ENDPOINT,
    "app": {
        "secret_key": "secret_key"
    },
    "mongodb": {
        "database": MONGODB_DB,
        "host": MONGODB_HOST,
        "port": MONGODB_PORT
    },
    "login": {
        "token_valid_time_minutes": 60
    },
    "guacamole": {
        "host": "http://" + os.environ["GUACAMOLE"] + ":" + os.environ["GUACAMOLE_PORT"]

    },
    "scheduler": {
        # "job_store": "mysql",
        # "job_store_url": 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
        "job_store": "mongodb",
        "database": MONGODB_DB,
        "collection": "jobs",
        "host": MONGODB_HOST,
        "port": MONGODB_PORT
    },
    "storage": {
        "type": "local",
        "size_limit_kilo_bytes": 5 * 1024,
        },
    "docker": {
        "alauda": {
            "token": "",
            "namespace": "",
            "endpoint": "http://api.int.alauda.io",
            "region_name": "BEIJING1"
        }
    },
    "email": {
        "host": "",
        "port": 587,
        "default_sender": "",
        "receivers_forced": [],
        "username": "",
        "password": "",
        "email_templates": {
            "dev_plan_submitted_notify": {
                "title": "开放黑客松: %s 团队开发计划书已提交",
                "default_file_name": "dev_plan_notification.html"
            }
        }
    },
    "voice_verify": {
        "enabled": False,
        "provider": "",
        "rong_lian": {
            "account_sid": "",
            "auth_token": "",
            "app_id": "",
            "server_ip": "https://app.cloopen.com",
            "server_port": "8883",
            "soft_version": "2013-12-26",
            "play_times": 3,
            "display_number": "",
            "response_url": "",
            "language": "zh"
        }
    },
    "sms": {
        "enabled": False,
        "provider": "",
        "china_telecom": {
            "url": "http://api.189.cn/v2/emp/templateSms/sendSms",
            "app_id": "",
            "app_secret": "",
            "url_access_token": "https://oauth.api.189.cn/emp/oauth2/v3/access_token"
        }
    },
    "ukylin": {
        "k8s": {
            "ips": ["119.3.202.71", "49.4.90.39"],
            "template": {
                "name": "Kubernetes",
                "description": "Kubernetes",
                "virtual_environments": [
                    {
                        "images": [
                            {
                                "image": "SOME IMAGE"
                            }
                        ],
                        "cluster": {
                            "token": "SOME TOKEN",
                            "namespace": "default",
                            "api_url": "SOME URL"
                        },
                        "ports": [
                            {
                                "public": True,
                                "public_port": 30006,
                                "protocol": "TCP",
                                "name": "UKylin",
                                "port": 5900
                            }
                        ],
                        "provider": 3,
                        "name": "ukylin"
                    }
                ]
            }
        }
    }
}