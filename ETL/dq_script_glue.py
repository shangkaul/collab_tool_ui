import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.commit()
# -------------------------Glue Job housekeeping section -----------------------
import boto3 
from botocore.errorfactory import ClientError
from urllib.parse import urlparse
import pandas as pd
import pandera as pa
import datetime as dt
import logging
import json
import copy
# --------------------End of Script imports---------------------------
def setLog(e,check):
    """add success/fail logs to the file_list.

    Parameters
    ----------
    e :[str]
        An exception or the string value of an exception
    check:[str]
        DQ check for which logs are being added
    """
    log_msg = f"{check} -> {e}" 
    file_status.append(log_msg)


def setTaskVal(source,file,status,error_loc=""):
    """Append file status to a global df exit_status
    Parameters
    ----------
    source:[str]
        Source file for which DQ logs are being added
    status:[str]
        Status of File DQ check (success/fail)
    error_loc:[str]
        Location of error file, if DQ check failed, blank otherwise.
    
    """
    ts=dt.datetime.now()
    logs=copy.deepcopy(file_status)
    exit_status.loc[len(exit_status.index)] = [ts,layer,source,file,status,error_loc,logs] 
    file_status.clear()
    return

def extractBotoParams(config_path):
    """Extract bucket name and key from s3 path.

    Parameters
    ----------
    config_path : str
        path of application configuration file
    Returns
    -------
    pair
        pair with bucket name and path key.
    """
    parsed_url = urlparse(config_path)
    bucket_name = parsed_url.hostname
    s3_path = parsed_url.path[1:]
    
    return bucket_name,s3_path

    

def getConfig(config_path: str):
    """Read application configuration file into json

    Parameters
    ----------
    config_path : str
        path of application configuration file
    Returns
    -------
    dict
        return a json dictionary contain application configuration
    """
    try:
        logger.info(f'Reading config from {config_path}')
        bucket_name,s3_path = extractBotoParams(config_path)
        obj = s3_connect.get_object(Bucket=bucket_name, Key=s3_path)
        config = obj['Body'].read().decode("utf-8")
        logger.info("Config file read successfully!")
        return json.loads(config)
    except FileNotFoundError as e:
        logger.exception('CONFIGURATION ERROR: Couldnt find the configuration file : ' + str(e))
        raise FileNotFoundError('CONFIGURATION ERROR: Couldnt find the configuration file : ' + str(e))
    except ValueError as e:
        if not config_path:
            logger.exception('CONFIGURATION ERROR: Null config path : ' + str(e))
            raise ValueError('CONFIGURATION ERROR: Null config path : ' + str(e))
        else:
            logger.exception(
                'CONFIGURATION ERROR: Invalid json. Error occurred while loading configuration file : ' + str(e))
            raise ValueError(
                'CONFIGURATION ERROR: Invalid json. Error occurred while loading configuration file : ' + str(e))
    except Exception as e:
        logger.exception('CONFIGURATION ERROR: Error occurred while loading configuration file : ' + str(e))
        err_msg = f"{type(e).__name__} : CONFIGURATION ERROR: Error occurred while loading configuration file : {str(e)}"
        raise Exception(err_msg) from e



def move_file(src,dest):
    """Method to move file between directories. If path is not a file -> return, do nothing.

    Args:
        src (str): Source path with filename
        dest (str): Destination path with file name
    """
    try:
        s3 = boto3.resource('s3')
        src_bucket,src_key=extractBotoParams(src)
        dest_bucket,dest_key=extractBotoParams(dest)
        copy_source = {
        'Bucket': src_bucket,
        'Key': src_key
        }
    
        bucket = s3.Bucket(dest_bucket)
        obj = bucket.Object(dest_key)
        obj.copy(copy_source)
        s3.Object(src_bucket, src_key).delete()
        logger.info(f"{src.split('/')[-1]} moved to : {dest}")
    except Exception as e:
        msg=f"Failed to move file to {dest} due to -> {e}"
        logger.error(msg)
        raise msg #try block in main for will catch this exception and push file status to df then continue with next file.
        
    

def create_dir(path):
    """Create a new directory, do nothing if directory exists.

    Args:
        path (string): directory path
    """
    try:
        if directoryExists(path):
          return
        else:
          bucketname,key=extractBotoParams(path)
          s3_connect.put_object(Bucket=bucketname,Key=key)
          logger.info(f"Directory created at: {path}")
    except Exception as e:
        msg=f"Failed to create directory {path} due to -> {e}"
        logger.error(msg)
        raise msg #try block in main for will catch this exception and push file status to df then continue with next file.
        

def directoryExists(path):
    """Check if directory/file exists.
    Note: Folder paths must end with '/'

    Args:
        path (string): directory path
    Returns:
    bool
    """
    bucket,key = extractBotoParams(path)
    try:
        s3_connect.head_object(Bucket=bucket, Key=key)
    except ClientError:
        return False
    return True
    
def listDir(path):
    """List all files present in dir and return list.

    Args:
        path (string): directory path
    Returns:
    list: List of file keys.
    """
    try:
        files=[]
        s3 = boto3.resource('s3')
        bucket,key=extractBotoParams(path)
        my_bucket = s3.Bucket(bucket)
        for object_summary in my_bucket.objects.filter(Prefix=key):
            file_key=object_summary.key
            if file_key[-1]!='/':
              files.append(file_key)
        return files
    except Exception as e:
        msg=f"Failed to list dir {path} due to -> {e}"
        logger.error(msg)
        raise e
        

def perform_generic_checks(file_path):
    """The method performs generic file checks on the file. These include - 
    - Csv extension check
    - Check is file is empty

    Args:
        file_path (str): File path on which dq checks are performed.
    """
    try:
        status=True
        file=file_path.split("/")[-1]
        logger.info(f"Starting generic DQ Checks for: {file}")

        #DQ1: File extension check
        ext=file_path[-3:]
        if ext!=config["source_ext"]:
            msg=f"CSV format check failed for: {file}"
            logger.warning(msg)
            setLog(msg,"File extension check")
            status=False
            return status
        else:
            msg=f"CSV format check passed for: {file}"
            logger.info(msg)
            # setLog(msg,"File extension check")
        
        #DQ2: File Not Empty check
        try:
            df=pd.read_csv(file_path)
            if df.shape[0] == 0:
                msg=f"File Not Empty check failed for: {file}"
                logger.warning(msg)
                setLog(msg,"File Not Empty")
                status=False
                return status
            else:
                msg=f"File Not empty check passed for: {file}"
                logger.info(msg)
                # setLog(msg,"File Not Empty check")
        except pd.errors.EmptyDataError as e:
                msg=f"File Not Empty check failed for: {file}"
                logger.warning(msg)
                setLog(msg,"File Not Empty")
                status=False
                return status
        
        return status
    except Exception as e:
        print(type(e))
        print(e)
        msg=f"Error:{e} while performing Generic DQ checks for file {file}"
        logger.error(msg)
        setLog(msg,"Generic DQ")
        return False

def clean_schema(lst):
    """This method cleans the list items so that they can be compared.
       - Strips space
       - Remove trailing/leading spaces
       - convert to lower case

    Args:
        lst (list): List to be cleaned
    
    Returns:
    list : Cleaned list
    """
    schema=[]
    for col in lst:
        col=col.lower().strip()
        col=" ".join(col.split())
        schema.append(col)
    
    return schema


def perform_business_checks(source,file_path):
    """The method performs DQ checks based on specific business rules. These include - 
    - File name check
    - Column check
    - Schema check (data type)
    - Special char check

    Args:
        source (str): Source system name.
        file_path (str): File path on which dq checks are performed.
    """
    try:
        status=True
        file=file_path.split("/")[-1]
        logger.info(f"Starting Business rule DQ Checks for: {file}")
        
        #ADD -> Check if filename in source: col_map -> if not just return False, file will be moved to error location.
        
        # DQ3: File Column Check
        df=pd.read_csv(file_path)
        control_schema=list(config["sources"][source]["col_map"][file].keys())
        curr_schema=list(df.columns)
        if set(clean_schema(control_schema)) != set(clean_schema(curr_schema)):
            msg=f"Column check failed for: {file}"
            logger.warning(msg)
            setLog(msg,"Schema Check")
            status=False
        else:
            msg=f"Column check passed for: {file}"
            logger.info(msg)
            # setLog(msg,"Schema Check")

        return status

    except Exception as e:
        print(type(e))
        print(e)
        msg=f"Error:{e} while performing Business DQ checks for file {file}"
        logger.error(msg)
        setLog(msg,"Business Rule DQ")
        return False


def main():
    """_summary_: Driver function for the DQ script.
    """
    try:
        #Read all sources from config as a list
        source_list=list(config["sources"].keys())
        for source in source_list:
            # -- this try : -> isRequired?
            msg=f"------Starting DQ checks for Source System: {source} ------"
            logger.info(msg)
            s3_uri=config['s3_base_uri']
            root_dir=f"{s3_uri}{config['sources'][source]['root_dir']}"
            dated_dir=eval(f'''f"{config['dated_folder']}"''')
            dated_dir=s3_uri+dated_dir
            create_dir(dated_dir)
            
            # except -> this will loop through all files in source and add failed message for all files in source folder
            # because dated folder creation failed

            #Move all files to dated folder
            for file in listDir(root_dir):
                file_path=f"{s3_uri}/{file}"
                file=file.split('/')[-1]
                # #move file to dated folder
                move_file(file_path,f"{dated_dir}{file}")
                logger.info(f"All files moved to dated folder for:{source}")
            
            for file in listDir(dated_dir):
                #Add try catch here failure of one file shouldnt stop the process.
                file_path=f"{s3_uri}/{file}"
                generic_dq_status=perform_generic_checks(file_path)
                if generic_dq_status == False:
                    logger.warning(f"One or more generic DQ checks failed for file: {file}")
                    err_path=eval(f'''f"{config['error_folder']}"''')
                    err_path=s3_uri+err_path
                    file_name=file.split('/')[-1]
                    
                    file_name=file_name.split('.')
                    curr_ts=dt.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
                    file_name[0]=file_name[0]+'_'+curr_ts
                    file_name=".".join(file_name)
                    
                    create_dir(err_path)
                    err_file_path=err_path+file_name
                    move_file(file_path,err_file_path)
                    setTaskVal(source,file_path.split('/')[-1],config["fail_flag"],err_file_path)
                else:
                    msg=f"All Generic DQ checks passed for {file}"
                    logger.info(msg)
                    business_dq_status=perform_business_checks(source,file_path)
                    if business_dq_status == True:
                        msg=f"Business Rule DQ checks passed for {file}"
                        logger.info(msg)
                        # setTaskVal(source,file,config["success_flag"],"")#write external table...
                    else:
                        logger.warning(f"One or more business rule DQ checks failed for file: {file}")
                        err_path=eval(f'''f"{config['error_folder']}"''')
                        err_path=s3_uri+err_path
                        file_name=file.split('/')[-1]
                        
                        file_name=file_name.split('.')
                        curr_ts=dt.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
                        file_name[0]=file_name[0]+'_'+curr_ts
                        file_name=".".join(file_name)
                    
                        create_dir(err_path)
                        err_file_path=err_path+file_name
                        move_file(file_path,err_file_path)
                        setTaskVal(source,file,config["fail_flag"],err_path) 


    except Exception as e:
        logger.error(e)
        raise e
    
# --------------------Global declarations---------------------

logger=logging.getLogger("DQ Script")
logging.basicConfig(format='%(name)s:%(levelname)s:  %(message)s', level=logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('aiobotocore').setLevel(logging.CRITICAL)
logging.getLogger('charset_normalizer').setLevel(logging.CRITICAL)
logging.getLogger('s3fs').setLevel(logging.CRITICAL)
logging.getLogger('fsspec').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)


config_path="s3://cte-test-bucket/raw/config/config.json"

global err_msgs,config,exit_status,curr_dt,layer,s3_connect
s3_connect = boto3.client('s3')
config=getConfig(config_path)
curr_dt=dt.date.today().strftime("%Y-%m")
layer="DQ Script"
print(type(config))
#Instantiate logging vars
file_status=[]
exit_status=pd.DataFrame(columns=config["status_dict_cols"])


main()
print(exit_status)
