import yaml, os, boto3
from pathlib import Path as GetHomePath 
import glob
import tarfile
import os.path

required_keys = ['Name', 'Description', 'Namespace', 'DeveloperNamespace']

def make_tarfile(alias):
    output_filename = ( "/tmp/%s.tar.gz" % (alias))
    source_dir = os.environ["ORMAN_APP_DIR"]
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return output_filename

def get_app_config():
    glob_cwd=( "%s/**" % ( os.getcwd() ) )
    for full_path in glob.glob(glob_cwd, recursive=True):
        file_name = os.path.basename(full_path)
        if file_name == 'orman.yml':
            os.environ["ORMAN_APP_DIR"] = os.path.dirname(full_path)
            with open(full_path) as app_config:
                return yaml.full_load(app_config)

def config_is_valid(app_config):
    app_config_keys = list( app_config.keys() )
    for key in required_keys:
        if key not in app_config_keys:
            return False
    return True

def init_market_config(app_config):
    market_dict = dict()
    for key in required_keys:
        value = app_config[key]
        market_dict[key] = str(value)
        exec( ( '%s="""%s"""' % (key,value) ), globals() )
    return market_dict

bucketname = 'orman-market'
config = get_app_config()
appKey = list(config.keys())[0] 
app_config = config[appKey]
config_is_valid = config_is_valid(app_config)
print(config_is_valid)
if config_is_valid:
    market_dict = init_market_config(app_config)
    of = make_tarfile(appKey)
    boto3.client('s3').upload_file(of, bucketname, appKey, ExtraArgs={"Metadata": market_dict})