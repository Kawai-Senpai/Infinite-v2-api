from database.mongo import init_db_structure, check_mongo_structure
from ultraprint.logging import logger
from ultraconfiguration import UltraConfig

#! Initialize ---------------------------------------------------------------
config = UltraConfig('config.json')
log = logger('init_log', 
            filename='debug/init.log', 
            include_extra_info=config.get("logging.include_extra_info", False), 
            write_to_file=config.get("logging.write_to_file", False))

def init():
    log.info("Initializing MongoDB structure...")
    init_db_structure()
    if check_mongo_structure(verbose=True):
        log.success("MongoDB structure initialized successfully.")
    else:
        log.error("MongoDB structure initialization has issues.")

if __name__ == "__main__":
    init()
