# -*- coding: utf-8 -*-
"""
Copyright (c) Microsoft Open Technologies (Shanghai) Co. Ltd.  All rights reserved.
 
The MIT License (MIT)
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Bian Hu'

import sys

sys.path.append("..")
from azure.storage import BlobService
from hackathon.log import log
from hackathon.functions import get_config

blob_service = BlobService(account_name=get_config("storage.account_name"),
                           account_key=get_config("storage.account_key"))
container_name = get_config("storage.container_name")


def create_container_in_storage():
    # create a container if doesn't exist
    container_name = get_config("storage.container_name")
    names = map( lambda x: x.name, blob_service.list_containers())
    if container_name not in names:
        blob_service.create_container(container_name)
    else:
        log.debug("container already exsit in storage")



def upload_file_to_azure(file, filename):
    try:
        create_container_in_storage()
        blob_service.put_block_blob_from_file(container_name, filename, file)
        return blob_service.make_blob_url(container_name, filename)
    except Exception as ex:
        log.error(ex.message)