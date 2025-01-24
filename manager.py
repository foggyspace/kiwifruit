import os
import sys
import signal
import logging
import argparse
from app import create_app


def setup_logging(log_level):
    """配置日志"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('kiwifruit.log')
        ]
    )


def signal_handler(signum, frame):
    """信号处理函数"""
    logger = logging.getLogger(__name__)
    logger.info(f'收到信号 {signum}, 正在优雅退出...')
    sys.exit(0)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Kiwifruit Web应用服务器')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址')
    parser.add_argument('--port', type=int, default=9527, help='监听端口')
    parser.add_argument('--env', default='development',
                      choices=['development', 'production', 'testing'],
                      help='运行环境')
    parser.add_argument('--debug', action='store_true', help='是否开启调试模式')
    parser.add_argument('--log-level', default='INFO',
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      help='日志级别')
    return parser.parse_args()


def main():
    # 解析命令行参数
    args = parse_args()
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = args.env
    
    # 配置日志
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 创建应用实例
    app = create_app()
    
    # 启动信息
    logger.info(f'Kiwifruit Web服务器启动于 {args.host}:{args.port}')
    logger.info(f'运行环境: {args.env}')
    logger.info(f'调试模式: {args.debug}')
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except Exception as e:
        logger.error(f'服务器启动失败: {str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()

