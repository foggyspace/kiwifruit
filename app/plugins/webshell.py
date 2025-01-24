import re
from typing import Optional
from bs4 import BeautifulSoup

from app.plugins.base import PluginABC, VulnerabilityInfo, RiskLevel


class WebShellPlugin(PluginABC):
    """WebShell检测插件"""
    def __init__(self):
        super().__init__()
        self.name = "WebShell检测"
        self.description = "检测网站中是否存在WebShell文件"
        self.priority = 10

        self._input_type = re.compile(r"<input[^</>]+?(>|/>)", re.I|re.M)
        self._ip_pattern = re.compile(r"\D(\d{1,3}(?:.\d{1,3}){3})\D")
        self._input_name = re.compile(r"<input[^</>]+?name\s*=\s*[\'\"w]", re.I)
        self._dir_path = re.compile(r"[CDEFG]:|/\w", re.I)

        self.webshell_features = {
            'PHP': {
                '404.php': ("<title>404 Not Found</title>", "<input type=password"),
                '2011.php': ("input {font:11px Verdana;BACKGROUND: #FFFFFF;height: 18px",
                         '<span style="font:11px Verdana;">Password'),
                'Ani-Shell.php': ('<body text="rgb(39,245,10)" bgcolor="black">',"--Ani Shell-")
            },
            'JSP': {},
            'ASP': {},
            'ASP.NET': {}
        }

        self.site_types = {'PHP': '.php', 'JSP': '.jsp', 'ASP.NET': '.asp', 'ASP': '.asp'}

    def _check_webshell_features(self, content: str, url: str) -> Optional[dict]:
        """检查页面内容是否包含WebShell特征"""
        for lang, features in self.webshell_features.items():
            if not url.endswith(self.site_types.get(lang, '')):
                continue

            for shell_name, patterns in features.items():
                matches = all(pattern in content for pattern in patterns)
                if matches:
                    return {
                        'shell_type': lang,
                        'shell_name': shell_name,
                        'patterns': patterns
                    }
        return None

    def _check_suspicious_inputs(self, content: str) -> bool:
        """检查是否存在可疑的输入框"""
        soup = BeautifulSoup(content, 'html.parser')
        for input_tag in soup.find_all('input'):
            input_type = input_tag.get('type', '').lower()
            if input_type == 'password' and not input_tag.get('name'):
                return True
        return False

    def run(self, target: str) -> Optional[VulnerabilityInfo]:
        try:
            response = self.send_request(target)
            if response.status_code != 200:
                return None

            content = response.text
            shell_info = self._check_webshell_features(content, target)
            has_suspicious_inputs = self._check_suspicious_inputs(content)

            if shell_info or has_suspicious_inputs:
                return VulnerabilityInfo(
                    name="WebShell检测",
                    description=f"在URL {target} 中发现疑似WebShell",
                    risk_level=RiskLevel.CRITICAL,
                    solution="立即删除WebShell文件，检查服务器安全性，修改管理员密码，更新网站程序",
                    references=[
                        "https://owasp.org/www-community/vulnerabilities/Web_Shell",
                        "https://www.acunetix.com/blog/articles/web-shells-101-using-php-web-shells-to-execute-commands/"
                    ],
                    details={
                        'url': target,
                        'shell_info': shell_info,
                        'has_suspicious_inputs': has_suspicious_inputs
                    }
                )

        except Exception as e:
            print(f"Error scanning {target}: {str(e)}")
            return None

        return None

