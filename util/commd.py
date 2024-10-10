import subprocess


def exec_work(command: str):
    try:
        # 执行命令
        result = subprocess.run(
            command,  # 需要执行的命令
            shell=True,  # 如果设置为True，命令将通过shell执行
            # cwd=conf_path,  # 设置工作目录
            check=True,  # 如果命令执行失败，将抛出异常
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.PIPE  # 捕获错误输出
        )
        # 捕获并记录命令的输出和错误
        print(f"Command executed successfully: {command}")
        print(f"Output: {result.stdout.decode('utf-8')}")
        print(f"Errors: {result.stderr.decode('utf-8')}")
    except subprocess.CalledProcessError as e:  # 捕获subprocess调用错误
        print(f"Command failed with error: {e.stderr.decode('utf-8')}")
    except Exception as e:  # 捕获其他所有异常
        print(f"An error occurred: {str(e)}")


def exec_work2(command: str):
    try:
        # 执行命令
        result = subprocess.run(
            command,  # 需要执行的命令
            shell=True,  # 如果设置为True，命令将通过shell执行
            check=True,  # 如果命令执行失败，将抛出异常
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.PIPE  # 捕获错误输出
        )

        # 捕获并记录命令的输出
        output = result.stdout.decode('utf-8').strip()  # 获取输出并去掉首尾空格
        errors = result.stderr.decode('utf-8').strip()  # 获取错误输出

        # 输出命令的最后一行
        if output:
            last_line = output.splitlines()[-1]  # 按行分割并获取最后一行
            return last_line  # 返回最后一行
        else:
            return None  # 如果没有输出，返回None

    except subprocess.CalledProcessError as e:
        # 捕获subprocess调用错误并返回错误信息
        return f"Command failed with error: {e.stderr.decode('utf-8')}"
    except Exception as e:
        # 捕获其他所有异常并返回错误信息
        return f"An error occurred: {str(e)}"
