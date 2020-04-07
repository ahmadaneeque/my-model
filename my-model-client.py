#!/usr/bin/env python3


import base64
import json
import logging
import os
import numpy as np
import requests
import sys 

from PIL import Image

logger = logging.getLogger('__mymodelclient__')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


if __name__ == '__main__':
    url = sys.argv[1]
    path = sys.argv[2]    # base64 encode image for HTTP POST
    data = {}
    with open(path, 'rb') as f:
        data['binData'] = base64.b64encode(f.read()).decode('utf-8')    

    logger.info("sending image {} to {}".format(path, url))
    response = requests.post(url, json = data, timeout = None)
    print(response)
    logger.info("caught response {}".format(response))
    status_code = response.status_code
    print(status_code)
    js = response.json()   
   
    if response.status_code == requests.codes['ok']:
        logger.info('converting tensor to image')
        data = js.get('data')
        tensor = data.get('tensor')
        shape = tensor.get('shape')
        values = tensor.get('values')
        logger.info("output image shape = {}".format(shape))    
        # Convert Seldon tensor to image
        img_bytes = np.asarray(values)
        img = img_bytes.reshape(shape)
        Image.fromarray(img.astype(np.uint8)).save('result.jpg')
        logger.info('wrote result image to result.jpg')
    elif response.status_code == requests.codes['service_unavailable']:
        logger.error('Model service is not available.')
    elif response.status_code == requests.codes['internal_server_error']:
        logger.error('Internal model error.')
