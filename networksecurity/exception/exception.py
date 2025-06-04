from networksecurity.logging import logger
import sys

class NetworkSecurityException(Exception):
    def __init__(self, error_msg:str, error_details:sys):
        self.error_msg= error_msg
        _,_,exe_tb = error_details.exc_info()

        self.filename = exe_tb.tb_frame.f_code.co_filename
        self.lineno = exe_tb.tb_lineno

    def str(self):
        return "error occured in lineno {0} in filename {1} error : {2}".format(self.lineno, self.filename,self.error_msg)
    
if __name__ == "main":
    try:
        logger.logging.INFO("log runs sucessful")
        b = 19/0
    except Exception as e:
        raise NetworkSecurityException(e,sys)