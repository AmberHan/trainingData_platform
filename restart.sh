#!/bin/bash

# 定义变量
VENV_PATH="./venv"  # 虚拟环境路径
APP_NAME="router.router:app"
HOST="0.0.0.0"
PORT="9202"
UVICORN_CMD="uvicorn $APP_NAME --host $HOST --port $PORT"

# 激活虚拟环境
source $VENV_PATH/bin/activate

# 停止现有进程
echo "Stopping existing processes..."
PIDS=$(pgrep -f "$UVICORN_CMD")

if [ -z "$PIDS" ]; then
    echo "No running processes found."
else
    for PID in $PIDS; do
        echo "Terminating process $PID..."
        kill -15 $PID
        sleep 1  # 等待1秒，确保进程有时间优雅关闭
        if kill -0 $PID > /dev/null 2>&1; then
            echo "Process $PID is still running, sending SIGKILL..."
            kill -9 $PID
        fi
    done
fi

# 启动新进程
echo "Starting new process..."
$UVICORN_CMD &
NEW_PID=$!
echo "New process started with PID $NEW_PID."

# 可选：检查新进程是否成功启动
sleep 2  # 等待2秒，确保新进程有足够的时间启动
if kill -0 $NEW_PID > /dev/null 2>&1; then
    echo "New process with PID $NEW_PID is running."
else
    echo "Failed to start the new process."
    exit 1
fi

exit 0
