import requests
import sys
from config import *


class DanbooruAPIClient:
    """
    Danbooru API 客户端，使用 requests 库直接与 API 交互
    """
    
    def __init__(self, username, api_key, base_url="https://danbooru.donmai.us"):
        """
        初始化 Danbooru API 客户端
        :param username: Danbooru 用户名
        :param api_key: Danbooru API 密钥
        :param base_url: Danbooru 基础 URL
        """
        self.username = username
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        
    def _make_request(self, endpoint, params=None):
        """
        发送 HTTP 请求到 Danbooru API
        :param endpoint: API 端点
        :param params: 请求参数
        :return: JSON 响应数据
        """
        url = f"{self.base_url}/{endpoint}"
        
        # 清理空参数
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = self.session.get(
                url,
                params=params,
                auth=(self.username, self.api_key),
                timeout=30
            )
            
            # 检查 HTTP 状态码
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise Exception("认证失败：请检查用户名和 API 密钥")
            elif response.status_code == 403:
                raise Exception("权限不足：无法访问该资源")
            elif response.status_code == 404:
                raise Exception("资源未找到")
            elif response.status_code == 429:
                raise Exception("请求频率过高：请稍后重试")
            else:
                raise Exception(f"HTTP 错误 {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {e}")
    
    def tag_list(self, name_matches=None, category=None, order=None, 
                 page=1, limit=1000, hide_empty=None):
        """
        获取标签列表
        :param name_matches: 标签名匹配模式
        :param category: 标签分类 (0=general, 1=artist, 3=copyright, 4=character)
        :param order: 排序方式 (name, date, count)
        :param page: 页码
        :param limit: 每页限制数量
        :param hide_empty: 是否隐藏空标签
        :return: 标签列表
        """
        params = {
            'search[name_matches]': name_matches,
            'search[category]': category,
            'search[order]': order,
            'page': str(page),
            'limit': str(limit),
            'search[hide_empty]': 'yes' if hide_empty else None
        }
        
        return self._make_request('tags.json', params)
    
    def tag_related(self, query, category=None):
        """
        获取相关标签
        :param query: 查询的标签名
        :param category: 标签分类过滤
        :return: 相关标签数据
        """
        params = {
            'query': query,
            'category': category
        }
        
        return self._make_request('related_tag.json', params)


def create_danbooru_client(username=USERNAME, api_key=API_KEY):
    """
    创建 Danbooru 客户端
    :param username: Danbooru 用户名
    :param api_key: Danbooru API 密钥
    :return: Danbooru 客户端实例
    """
    try:
        client = DanbooruAPIClient(username=username, api_key=api_key)
        return client
    except Exception as e:
        print(f"连接 Danbooru 时出错: {e}")
        sys.exit(1)