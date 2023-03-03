import sys

from lib.core.envinit import envinit
envinit(__file__)

from lib.core.logs import ERROR,INFO,WARN
from lib.core.options import parseCmdline,init
from lib.core.errors import ScannerTopException,DestinationUnReachable
from lib.core.engine import run
from lib.core.common import task_finsh_clean


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
