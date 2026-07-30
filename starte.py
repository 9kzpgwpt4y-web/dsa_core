import subprocess
import time
import webbrowser
import sys
import os

def start_terminal():
    print("="*50)
    print("      DSA CORE INTELLIGENT TERMINAL SYSTEM")
    print("="*50)
    
    # 1. 确保在根目录运行，防止路径报错
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # 2. 启动后端服务 (使用 sys.executable 确保调用当前的 Python)
    print("\n[Step 1/3] Launching Backend Server...")
    # 使用 subprocess.Popen 开启一个新进程
    try:
        # shell=True 增加兼容性，-m src.web.main 调用模块
        backend_proc = subprocess.Popen(
            [sys.executable, "-m", "src.web.main"],
            stdout=None, # 如果想看详细日志，可以改为 None
            stderr=None,
            shell=False 
        )
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return

    # 3. 等待引擎预热
    print("[Step 2/3] Waiting for Engine Warm-up (5s)...")
    time.sleep(5)

    # 4. 自动打开 UI 界面
    print("[Step 3/3] Opening Browser Interface...")
    ui_url = "http://127.0.0.1:8000"
    webbrowser.open(ui_url)

    print("\n✅ ALL SYSTEMS GO!")
    print(f"🔗 UI URL: {ui_url}")
    print("⚠️  Keep this window open to maintain the service.")
    print("="*50)

    try:
        # 保持主程序运行，直到你手动关闭
        backend_proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down DSA CORE...")
        backend_proc.terminate()

if __name__ == "__main__":
    start_terminal()
    