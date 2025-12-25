import json
import os

def create_ruleset_json():
    """读取 china.txt 文件并创建 sing-box 规则集 JSON 文件"""
    try:
        # 检查 china.txt 是否存在
        if not os.path.exists("china.txt"):
            print("错误: china.txt 文件不存在")
            return False
        
        # 读取 IP 地址列表
        ip_cidrs = []
        with open("china.txt", 'r') as f:
            for line in f:
                # 去掉首尾空格
                line = line.strip()
                if line:
                    ip_cidrs.append(line)
        
        # 创建规则集 JSON 结构
        ruleset = {
            "version": 2,
            "rules": [
                {
                    "ip_cidr": ip_cidrs
                }
            ]
        }
        
        # 保存到文件
        with open("cn.json", 'w') as f:
            json.dump(ruleset, f, indent=2)
        
        print(f"已创建规则集 JSON 文件: cn.json，包含 {len(ip_cidrs)} 条 IP 规则")
        return True
    
    except Exception as e:
        print(f"创建规则集 JSON 时出错: {e}")
        return False

if __name__ == "__main__":
    create_ruleset_json()
