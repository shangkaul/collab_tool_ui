from distutils.log import error
import pandas as pd
import datetime as dt
import coloredlogs,logging
import json
import os
import shutil
import copy

# ----------------------------------Imports End--------------------------------

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


def getConfig(config_path: str):
    """Read application configuration file into json

    Parameters
    ----------
    config_path : str
        path of application configuration file
    Returns
    -------
    json
        return a json dictionary contain application configuration
    """
    try:
        logger.info(f'Reading config from {config_path}')
        file=open(config_path)
        config=json.load(file)
        file.close()
        logger.info("Config file read successfully!")
        return config
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
    """Method to move file between directories.

    Args:
        src (str): Source path with filename
        dest (str): Destination path with file name
    """
    shutil.move(src,dest)
    logger.info(f"{src.split('/')[-1]} moved to : {dest}")

def create_dir(path):
    """Create a new directory, do nothing if directory exists.

    Args:
        path (string): directory path
    """
    os.makedirs(path, exist_ok=True) #Create dated folder
    logger.info(f"Directory created at: {path}")

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
    - Schema check
    - 

    Args:
        source (str): Source system name.
        file_path (str): File path on which dq checks are performed.
    """
    try:
        status=True
        file=file_path.split("/")[-1]
        logger.info(f"Starting Business rule DQ Checks for: {file}")
        
        # DQ3: File Schema Check
        df=pd.read_csv(file_path)
        control_schema=config["sources"][source]["col_map"][file]
        curr_schema=list(df.columns)
        if set(clean_schema(control_schema)) != set(clean_schema(curr_schema)):
            msg=f"Schema check failed for: {file}"
            logger.warning(msg)
            setLog(msg,"Schema Check")
            status=False
        else:
            msg=f"Schema check passed for: {file}"
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

def sum(a,b):
    return a+b


def main():
    """_summary_: Driver function for the DQ script.
    """
    try:
        #Read all sources from config as a list
        source_list=list(config["sources"].keys())
        for source in source_list:
            msg=f"------Staring DQ checks for Source System: {source} ------"
            logger.info(msg)
            root_dir=config["sources"][source]["root_dir"]
            curr_dir=root_dir+"/current"
            create_dir(f"{root_dir}/{curr_dt}") #Create dated directory
            dated_dir=f"{root_dir}/{curr_dt}"

            #Move all files to dated folder
            for file in os.listdir(curr_dir):
                file_path=os.path.join(curr_dir,file).replace("\\","/")
                #move file to dated folder
                move_file(file_path,f"{dated_dir}/{file}")
                logger.info(f"All files moved to dated folder for:{source}")
            
            for file in os.listdir(dated_dir):
                if file=="error":
                    continue
                dated_file_path=os.path.join(dated_dir,file).replace("\\","/")                
                generic_dq_status=perform_generic_checks(dated_file_path)
                if generic_dq_status == False:
                    logger.warning(f"One or more generic DQ checks failed for file: {file}")
                    create_dir(f"{dated_dir}/error/")
                    err_path=f"{dated_dir}/error/{file}"
                    move_file(dated_file_path,err_path)
                    setTaskVal(source,file,config["fail_flag"],err_path)
                else:
                    msg=f"All Generic DQ checks passed for {file}"
                    logger.info(msg)
                    business_dq_status=perform_business_checks(source,dated_file_path)
                    if business_dq_status == True:
                        msg=f"Business Rule DQ checks passed for {file}"
                        logger.info(msg)
                        setTaskVal(source,file,config["success_flag"],"")
                    else:
                        logger.warning(f"One or more business rule DQ checks failed for file: {file}")
                        create_dir(f"{dated_dir}/error/")
                        err_path=f"{dated_dir}/error/{file}"
                        move_file(dated_file_path,err_path)
                        setTaskVal(source,file,config["fail_flag"],err_path) 


    except Exception as e:
        logger.error(e)
    


# -------------------------------------Global Main-------------------------------------------------------

logger=logging.getLogger("DQ Script")
logging.basicConfig(format='%(name)s:%(levelname)s:  %(message)s', level=logging.DEBUG)
coloredlogs.install(level=logging.DEBUG, logger=logger)

config_path="./config/config.json"

global err_msgs,config,exit_status,curr_dt,layer
config=getConfig(config_path)
curr_dt=dt.date.today().strftime("%d-%m-%Y")
layer="DQ Script"

#Instantiate logging vars
file_status=[]
exit_status=pd.DataFrame(columns=config["status_dict_cols"])

main()
exit_status.to_csv("./result.csv")
