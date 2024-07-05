import re


WEBSHELL_FEATURE = {
    'PHP':
    {
        '404.php':("<title>404 Not Found</title>", "<input type=password"),
        '2011.php':("input {font:11px Verdana;BACKGROUND: #FFFFFF;height: 18px",
                 '<span style="font:11px Verdana;">Password'),
        'Ani-Shell.php':('<body text="rgb(39,245,10)" bgcolor="black">',"--Ani Shell-")

    },
    'JSP':
    {

    },
    'ASP':
    {

    },
    'ASP.NET':
    {

    }
}

_INPUT_TYPE = re.compile(r"<input[^</>]+?(>|/>)",re.I|re.M)
_IP_PATTERN = re.compile(r"\D(\d{1,3}(?:.\d{1,3}){3})\D")
_INPUT_NAMR = re.compile(r"<input[^</>]+?name\s*=\s*[\'\"\w]",re.I)
_DIR_PATH = re.compile(r"[CDEFG]:|/\w",re.I)
SITETYPES = {'PHP':'.php', 'JSP':'.jsp', 'ASP.NET':'.asp', 'ASP':'.asp'}


def run_plugin(target: str = '') -> None:
    pass

