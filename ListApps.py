import boto3
from columnar import columnar
bucketname='orman-market'
s3 = boto3.resource('s3')
s3client = boto3.client('s3')
market = s3.Bucket(bucketname)
market_apps = dict()
for market_object in market.objects.all():
    app_head = s3client.head_object(Bucket=bucketname, Key=market_object.key) 
    meta = app_head["Metadata"]
    namespace = meta["namespace"]
    market_apps[namespace] = meta

print("""



\t\t ▄██████▄     ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████ ███▄▄▄▄   
\t\t███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███▀▀▀██▄ 
\t\t███    ███   ███    ███ ███   ███   ███   ███    ███ ███   ███ 
\t\t███    ███  ▄███▄▄▄▄██▀ ███   ███   ███   ███    ███ ███   ███ 
\t\t███    ███ ▀▀███▀▀▀▀▀   ███   ███   ███ ▀███████████ ███   ███ 
\t\t███    ███ ▀███████████ ███   ███   ███   ███    ███ ███   ███ 
\t\t███    ███   ███    ███ ███   ███   ███   ███    ███ ███   ███ 
\t\t ▀██████▀    ███    ███  ▀█   ███   █▀    ███    █▀   ▀█   █▀  
\t\t             ███    ███                                        
\t\t
\t\t\t Reverse engineering the internet since 1999.
""")

market_headers = ["Space", "Title", "Description"]
market_table = list()
for app in market_apps:
    name = market_apps[app]["name"]
    namespace = str(app)
    description = market_apps[app]["description"]
    row = [namespace,name,description]
    market_table.append(row)

table = columnar(market_table, market_headers, no_borders=True)
print(table)