import re


DOMAIN_PAHT = re.compile(r"^(?P<domain>.+//[^/]+)(?P<path>.*)$")
ROBOTS_ALLOW_PATH = re.compile(r"allow\s*:\s*(?P<path>[^*]+).*$",re.I)
SITEMAP_URL = re.compile(r"(?P<url>http[^<>]+)")


class CrawlerSpider(object):
    def __init__(self, start_url: str, task_id: int = None) -> None:
        self.start_url = start_url
        self.task_id = task_id
        self.visited_urls = set()
        self.url_queue = []
        self.form_params = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.session = None
        self.robots_rules = []
        self.sitemap_urls = []
        self.static_extensions = {'.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx'}
        
    def _init_session(self):
        """初始化请求会话"""
        import requests
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _is_valid_url(self, url: str) -> bool:
        """检查URL是否有效且未被访问过"""
        if not url or not url.startswith('http'):
            return False
        if url in self.visited_urls:
            return False
        return not any(url.endswith(ext) for ext in self.static_extensions)
        
    def _normalize_url(self, url: str, base_url: str) -> str:
        """标准化URL"""
        from urllib.parse import urljoin
        return urljoin(base_url, url)
        
    def _extract_urls(self, html: str, base_url: str) -> set:
        """从HTML中提取URL"""
        from bs4 import BeautifulSoup
        urls = set()
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all(['a', 'link', 'script', 'img']):
            url = link.get('href') or link.get('src')
            if url:
                normalized_url = self._normalize_url(url, base_url)
                if self._is_valid_url(normalized_url):
                    urls.add(normalized_url)
        return urls
        
    def _extract_forms(self, html: str, url: str) -> list:
        """提取表单参数"""
        from bs4 import BeautifulSoup
        forms = []
        soup = BeautifulSoup(html, 'html.parser')
        for form in soup.find_all('form'):
            form_data = {
                'action': self._normalize_url(form.get('action', ''), url),
                'method': form.get('method', 'get').upper(),
                'inputs': []
            }
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_data = {
                    'name': input_tag.get('name', ''),
                    'type': input_tag.get('type', 'text'),
                    'value': input_tag.get('value', '')
                }
                form_data['inputs'].append(input_data)
            forms.append(form_data)
        return forms

    def _parse_robots_txt(self, base_url: str) -> None:
        """解析robots.txt文件"""
        try:
            robots_url = self._normalize_url('/robots.txt', base_url)
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if 'Allow:' in line:
                        match = ROBOTS_ALLOW_PATH.search(line)
                        if match:
                            self.robots_rules.append(match.group('path'))
                    elif 'Sitemap:' in line:
                        match = SITEMAP_URL.search(line)
                        if match:
                            self.sitemap_urls.append(match.group('url'))
        except Exception:
            pass

    def _save_url(self, url: str, method: str = 'GET', params: str = None, post_data: str = None,
                  referer: str = None, req_headers: dict = None, resp_headers: dict = None,
                  status_code: int = None, content_type: str = None, start_time: int = None,
                  end_time: int = None) -> None:
        """保存URL到数据库"""
        from app.models.urls import URLModel
        import json
        import time

        url_model = URLModel()
        url_model.task_id = self.task_id
        url_model.url = url
        url_model.method = method
        url_model.params = params
        url_model.post_data = json.dumps(post_data) if post_data else None
        url_model.referer = referer
        url_model.request_headers = json.dumps(req_headers) if req_headers else None
        url_model.response_headers = json.dumps(resp_headers) if resp_headers else None
        url_model.response_status = status_code
        url_model.content_type = content_type
        url_model.start_time = start_time or int(time.time())
        url_model.end_time = end_time or int(time.time())
        url_model.save()

    def crawl(self) -> None:
        """开始爬取网站"""
        from urllib.parse import urlparse, parse_qs
        import time

        self._init_session()
        self.url_queue.append(self.start_url)
        parsed_url = urlparse(self.start_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # 解析robots.txt
        self._parse_robots_txt(base_url)

        while self.url_queue:
            current_url = self.url_queue.pop(0)
            if current_url in self.visited_urls:
                continue

            try:
                start_time = int(time.time())
                response = self.session.get(current_url, timeout=10)
                end_time = int(time.time())

                # 保存URL信息
                params = parse_qs(urlparse(current_url).query)
                self._save_url(
                    url=current_url,
                    params=json.dumps(params) if params else None,
                    req_headers=dict(response.request.headers),
                    resp_headers=dict(response.headers),
                    status_code=response.status_code,
                    content_type=response.headers.get('content-type'),
                    start_time=start_time,
                    end_time=end_time
                )

                if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
                    # 提取新的URL
                    new_urls = self._extract_urls(response.text, base_url)
                    self.url_queue.extend(url for url in new_urls if url not in self.visited_urls)

                    # 提取表单
                    forms = self._extract_forms(response.text, current_url)
                    for form in forms:
                        self._save_url(
                            url=form['action'],
                            method=form['method'],
                            post_data={input_['name']: input_['value'] for input_ in form['inputs']},
                            referer=current_url
                        )

                self.visited_urls.add(current_url)

            except Exception as e:
                print(f"Error crawling {current_url}: {str(e)}")
                continue
