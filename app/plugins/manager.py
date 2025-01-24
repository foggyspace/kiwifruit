from typing import Dict, List, Optional, Type
from pathlib import Path
import importlib.util
import inspect

from app.plugins.base import PluginABC, VulnerabilityInfo


class PluginManager:
    """插件管理器"""
    _instance = None
    _plugins: Dict[str, Type[PluginABC]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register_plugin(self, plugin_class: Type[PluginABC]) -> None:
        """注册插件"""
        if not inspect.isclass(plugin_class) or not issubclass(plugin_class, PluginABC):
            raise TypeError(f"{plugin_class.__name__} 不是有效的插件类")
        self._plugins[plugin_class.__name__] = plugin_class

    def load_plugins(self, plugins_dir: str) -> None:
        """从指定目录加载插件"""
        plugin_path = Path(plugins_dir)
        if not plugin_path.exists() or not plugin_path.is_dir():
            raise ValueError(f"插件目录 {plugins_dir} 不存在")

        for file_path in plugin_path.glob("*.py"):
            if file_path.name.startswith("_") or file_path.name == "base.py":
                continue

            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, str(file_path))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 查找并注册插件类
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and issubclass(obj, PluginABC)
                            and obj != PluginABC):
                        self.register_plugin(obj)

    def get_plugin(self, plugin_name: str) -> Optional[Type[PluginABC]]:
        """获取指定名称的插件"""
        return self._plugins.get(plugin_name)

    def get_all_plugins(self) -> List[Type[PluginABC]]:
        """获取所有已注册的插件"""
        return list(self._plugins.values())

    def run_plugin(self, plugin_name: str, target: str) -> Optional[VulnerabilityInfo]:
        """运行指定插件"""
        plugin_class = self.get_plugin(plugin_name)
        if not plugin_class:
            raise ValueError(f"插件 {plugin_name} 不存在")

        plugin = plugin_class()
        if not plugin.enabled:
            return None

        return plugin.run(target)

    def run_all_plugins(self, target: str) -> List[VulnerabilityInfo]:
        """运行所有已启用的插件"""
        results = []
        for plugin_class in sorted(self._plugins.values(), key=lambda p: p().priority, reverse=True):
            plugin = plugin_class()
            if plugin.enabled:
                result = plugin.run(target)
                if result:
                    results.append(result)
        return results