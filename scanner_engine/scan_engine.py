import os
import sys

from libs.core.initenv import envinit
envinit(__file__)

from libs.core.logs import ERROR,INFO,WARN
from libs.core.options import parseCmdline,init
from libs.core.errors import ScannerTopException,DestinationUnReachable
from libs.core.engine import run
from libs.core.tools import task_finsh_clean

def main():
    try:
        parseCmdline()
        init()
        run()
    except KeyboardInterrupt:
        INFO("User aborted,scan stop")
    except DestinationUnReachable as e:
        WARN("Destination:%s not reachable,please check" % e.dest)
    except ScannerTopException:
        ERROR("User define exception")
    except Exception as e:
        ERROR("Exception occur,scan stop")
    finally:
        task_finsh_clean()
        INFO("Scan finished!")

def test():
    sys.argv = ['python','topscan.py','-t','1','-u','http://127.0.0.1/vul/file_upload.php','-b','/vul/']
    main()


if __name__ == "__main__":
    main()
