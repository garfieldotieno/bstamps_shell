import os


redis_config = {
    'mode':'DEVELOPMENT',
    'port':6379
}



blu_config={}
blu_config['API_TOKEN'] = '1531611188:AAFS8bS14U8b4fnzRexd5cZRBoS3Gxq4ACk'
blu_config['WEBHOOK_HOST'] = 'bstamps.africa/'
blu_config['WEBHOOK_URL_BASE'] = "https://%s" % (blu_config['WEBHOOK_HOST'])
blu_config['WEBHOOK_URL_PATH'] = f"{blu_config['API_TOKEN']}/"



mk40_config={}
mk40_config['API_TOKEN']= '1084147196:AAH8ij0bHPqPDEOQln9UDmiMz6NXNNYF0uI'
mk40_config['WEBHOOK_HOST']= 'db02-102-217-65-31.eu.ngrok.io/'
mk40_config['WEBHOOK_URL_BASE'] = "https://%s" % (mk40_config['WEBHOOK_HOST'])
mk40_config['WEBHOOK_URL_PATH'] = f"{mk40_config['API_TOKEN']}/"



mk41_config={}
mk41_config['API_TOKEN'] = '1159524439:AAG360omBwX6mDvs5f2LC7RY-TYMwnY6ilE'
mk41_config['WEBHOOK_HOST'] = '55b7-102-217-64-15.eu.ngrok.io/'
mk41_config['WEBHOOK_URL_BASE'] = "https://%s" % (mk41_config['WEBHOOK_HOST'])
mk41_config['WEBHOOK_URL_PATH'] = f"{mk41_config['API_TOKEN']}/"


blu_site_config = {}
blu_site_config['API_TOKEN'] = ''



stickers_object = {}
stickers_object['tonystar_greeting_fid'] = 'CAACAgIAAxkBAAM0YlrPeq33MVXj9uTI9hkMka9hEbYAAmoAA6bKyAxrSu7GYigJLSQE'
stickers_object['tonystar_greeting_ufid'] = 'AgADagADpsrIDA'
stickers_object['elefun_greeting_fid'] = 'CAACAgIAAxkBAAILcWJa0uzQsVFfOZ90ROcX_MfZS3DBAAI4AAPBnGAMDpOgdzUpMCokBA'
stickers_object['elefun_greeting_ufid'] = 'AgADOAADwZxgDA'
