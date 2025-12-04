import os
import subprocess
import time
from datetime import datetime

def run_command(command):
    """运行 shell 命令并返回结果"""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"命令执行失败: {command}")
            print(f"错误: {stderr}")
            return False
            
        return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def push_to_ruleset_branch():
    """推送 cn.srs 和 cn.json 到 rule-set 分支"""
    try:
        # 检查文件是否存在
        if not os.path.exists("cn.srs"):
            print("错误: cn.srs 文件不存在")
            return False
        
        if not os.path.exists("cn.json"):
            print("错误: cn.json 文件不存在")
            return False
        
        # 配置 Git
        print("配置 Git")
        run_command('git config --global user.name "GitHub Actions"')
        run_command('git config --global user.email "actions@github.com"')
        
        # 获取当前分支名
        current_branch = subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True).decode().strip()
        print(f"当前分支: {current_branch}")
        
        # 检查 rule-set 分支是否存在
        remote_branches = subprocess.check_output("git ls-remote --heads origin", shell=True).decode()
        branch_exists = "refs/heads/rule-set" in remote_branches
        
        if branch_exists:
            # 如果分支存在，则删除它
            print("正在删除现有的 rule-set 分支")
            run_command("git push origin --delete rule-set")
            # 等待一些时间确保分支被删除
            time.sleep(2)
        
        # 创建并切换到新的 rule-set 分支
        print("创建 rule-set 分支")
        run_command("git checkout --orphan rule-set")
        
        # 清除工作区
        run_command("git rm -rf --cached .")
        
        # 添加文件
        print("添加 cn.srs 和 cn.json 文件")
        run_command("git add cn.srs -f")
        run_command("git add cn.json -f")
        
        # 提交更改
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Update China IP rule-set - {current_time}"
        run_command(f'git commit -m "{commit_message}"')
        
        # 推送到远程
        print("推送到远程 rule-set 分支")
        run_command("git push -u origin rule-set")
                
        print("成功推送到 rule-set 分支")
        return True
        
    except Exception as e:
        print(f"推送到 rule-set 分支时出错: {e}")
        return False

if __name__ == "__main__":
    push_to_ruleset_branch()
