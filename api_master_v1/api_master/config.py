import os


redis_config = {
    'mode':'PRODUCTION',
    'port':6379
}

hermes_config={}
hermes_config['API_TOKEN'] = '7976895822:AAEUPexN5oSVvjV-mdRE0Z7yT2dA3r9A9Rw'
hermes_config['WEBHOOK_HOST'] = 'mutually-advanced-pegasus.ngrok-free.app/'
hermes_config['WEBHOOK_URL_BASE'] = "https://%s" % (hermes_config['WEBHOOK_HOST'])
hermes_config['WEBHOOK_URL_PATH'] = f"{hermes_config['API_TOKEN']}/"



blu_config={}
blu_config['API_TOKEN'] = '6716887285:AAGS79w1cXeJd8h71aBOl1ppTrQKnGVTy24'
blu_config['WEBHOOK_HOST'] = 'mutually-advanced-pegasus.ngrok-free.app/'
blu_config['WEBHOOK_URL_BASE'] = "https://%s" % (blu_config['WEBHOOK_HOST'])
blu_config['WEBHOOK_URL_PATH'] = f"{blu_config['API_TOKEN']}/"



mk40_config={}
mk40_config['API_TOKEN']= '1084147196:AAH8ij0bHPqPDEOQln9UDmiMz6NXNNYF0uI'
mk40_config['WEBHOOK_HOST']= 'c86d-172-232-146-119.ngrok-free.app/'
mk40_config['WEBHOOK_URL_BASE'] = "https://%s" % (mk40_config['WEBHOOK_HOST'])
mk40_config['WEBHOOK_URL_PATH'] = f"{mk40_config['API_TOKEN']}/"


mk41_config={}
mk41_config['API_TOKEN'] = '1159524439:AAG360omBwX6mDvs5f2LC7RY-TYMwnY6ilE'
mk41_config['WEBHOOK_HOST'] = '92ed-102-217-67-96.ngrok-free.app/'
mk41_config['WEBHOOK_URL_BASE'] = "https://%s" % (mk41_config['WEBHOOK_HOST'])
mk41_config['WEBHOOK_URL_PATH'] = f"{mk41_config['API_TOKEN']}/"


blu_site_config = {}
blu_site_config['API_TOKEN'] = ''

stickers_object = {}
stickers_object['tonystar_greeting_fid'] = 'CAACAgIAAxkBAAM0YlrPeq33MVXj9uTI9hkMka9hEbYAAmoAA6bKyAxrSu7GYigJLSQE'
stickers_object['tonystar_greeting_ufid'] = 'AgADagADpsrIDA'
stickers_object['elefun_greeting_fid'] = 'CAACAgIAAxkBAAILcWJa0uzQsVFfOZ90ROcX_MfZS3DBAAI4AAPBnGAMDpOgdzUpMCokBA'
stickers_object['elefun_greeting_ufid'] = 'AgADOAADwZxgDA'
