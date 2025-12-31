import requests

def download_file(url, output_file):
    """下载文件并保存到指定路径"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"成功下载: {output_file}")
        return True
    except Exception as e:
        print(f"下载失败: {url}, 错误: {e}")
        return False

def main():
    # 直接下载合并好的列表
    china_url = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china46.txt"
    output_file = "cn.txt"
    
    download_file(china_url, output_file)

if __name__ == "__main__":
    main()
