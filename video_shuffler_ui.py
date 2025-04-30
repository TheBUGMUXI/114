import os
import random
import shutil
import uuid
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class VideoShufflerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频打乱工具")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # 初始化变量
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()

        # 创建 UI 元素
        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = tk.Label(
            self.root, 
            text="视频打乱工具", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=20)

        # 输入文件夹选择
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            input_frame, 
            text="输入文件夹:", 
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(side="left", padx=10)

        tk.Entry(
            input_frame, 
            textvariable=self.input_folder,
            width=30,
            font=("Arial", 12)
        ).pack(side="left", padx=10)

        tk.Button(
            input_frame, 
            text="选择", 
            command=self.select_input_folder,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=10
        ).pack(side="left", padx=5)

        # 输出文件夹选择
        output_frame = tk.Frame(self.root, bg="#f0f0f0")
        output_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            output_frame, 
            text="输出文件夹:", 
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(side="left", padx=10)

        tk.Entry(
            output_frame, 
            textvariable=self.output_folder,
            width=30,
            font=("Arial", 12)
        ).pack(side="left", padx=10)

        tk.Button(
            output_frame, 
            text="选择", 
            command=self.select_output_folder,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=10
        ).pack(side="left", padx=5)

        # 操作按钮
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="开始处理",
            command=self.start_processing,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10
        ).pack(pady=10)

        # 进度条
        self.progress_bar = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress_bar.pack(pady=10)

        # 日志区域
        log_frame = tk.Frame(self.root, bg="#f0f0f0")
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            log_frame,
            text="处理日志:",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(anchor="w", pady=5)

        self.log_text = tk.Text(
            log_frame,
            height=8,
            width=60,
            font=("Arial", 10),
            bg="white",
            fg="black"
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)
            self.log("已选择输入文件夹: " + folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)
            self.log("已选择输出文件夹: " + folder)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def start_processing(self):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()

        if not input_folder:
            messagebox.showerror("错误", "请选择输入文件夹！")
            return

        if not output_folder:
            messagebox.showerror("错误", "请选择输出文件夹！")
            return

        # 清空日志
        self.log_text.delete(1.0, tk.END)

        # 开始处理
        self.log("开始处理视频文件...")
        self.process_videos(input_folder, output_folder)
        self.log("处理完成！")

    def process_videos(self, input_folder, output_folder):
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 获取输入文件夹中的所有视频文件
        video_files = []
        for file in os.listdir(input_folder):
            file_path = os.path.join(input_folder, file)
            if os.path.isfile(file_path):
                if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv')):
                    video_files.append(file_path)

        if not video_files:
            self.log("未找到视频文件！")
            return

        # 打乱视频文件顺序
        random.shuffle(video_files)

        # 移动文件并显示进度
        total_files = len(video_files)
        for i, file_path in enumerate(video_files):
            file_name = os.path.basename(file_path)
            new_file_name = f"{uuid.uuid4().hex}_{file_name}"
            new_file_path = os.path.join(output_folder, new_file_name)

            # 更新进度条
            progress = (i + 1) / total_files * 100
            self.progress_bar["value"] = progress
            self.root.update()

            # 移动文件
            shutil.move(file_path, new_file_path)
            self.log(f"已移动: {file_name} -> {new_file_name}")

        # 重置进度条
        self.progress_bar["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoShufflerApp(root)
    root.mainloop()