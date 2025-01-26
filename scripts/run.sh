#!/bin/bash

# 设置错误处理
set -e

# 定义颜色输出
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# 打印信息函数
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# 检查必要的环境变量
if [ -z "$FLASK_ENV" ]; then
    export FLASK_ENV="development"
    warn "FLASK_ENV not set, using default: development"
fi

# 检查Python虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    warn "未检测到Python虚拟环境，建议在虚拟环境中运行"
fi

# 启动函数
start_flask() {
    info "启动Flask应用..."
    if [ "$FLASK_ENV" = "production" ]; then
        gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
    else
        python3 -m flask run --host=0.0.0.0 --port=5000
    fi
}

start_celery() {
    info "启动Celery worker..."
    celery -A make_celery worker --loglevel=info
}

start_frontend() {
    if [ -d "web" ]; then
        info "启动前端开发服务器..."
        cd web && yarn dev
    else
        warn "未找到web目录，跳过启动前端服务"
    fi
}

# 主函数
main() {
    local mode=$1

    case $mode in
        "all")
            # 使用后台进程启动所有服务
            start_flask &
            start_celery &
            start_frontend &
            # 等待所有后台进程
            wait
            ;;
        "flask")
            start_flask
            ;;
        "celery")
            start_celery
            ;;
        "frontend")
            start_frontend
            ;;
        *)
            echo "使用方法: $0 [all|flask|celery|frontend]"
            echo "  all      - 启动所有服务"
            echo "  flask    - 只启动Flask应用"
            echo "  celery   - 只启动Celery worker"
            echo "  frontend - 只启动前端开发服务器"
            exit 1
            ;;
    esac
}

# 设置执行权限
chmod +x "$0"

# 执行主函数
main "$@"