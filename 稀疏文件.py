import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# 在导入语言管理器之前，先加载用户语言偏好
def get_user_language():
    """获取用户配置的语言"""
    try:
        config_file = os.path.join(os.path.expanduser('~'), '.sparse_file_generator', 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('language', 'zh_CN')
    except Exception:
        pass
    return 'zh_CN'

# 设置用户语言环境变量
os.environ['USER_LANGUAGE'] = get_user_language()

from language_manager import lang


def create_dummy_large_file(file_path, apparent_size):
    """
    创建一个显示为大文件但实际上占用空间很小的文件
    :param file_path: 文件路径
    :param apparent_size: 显示的大小（字节）
    """
    with open(file_path, 'wb') as f:
        f.seek(apparent_size - 1)
        f.write(b'\0')


def get_size_in_bytes(size_str):
    """
    将用户输入的大小字符串转换为字节数
    支持的单位: B, KB, MB, GB, TB, PB, EB, ZB, YB
    """
    size_str = size_str.strip().upper()
    if not size_str:
        return 0

    # 定义所有支持的单位及其对应的乘数
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
        'PB': 1024 ** 5,
        'EB': 1024 ** 6,
        'ZB': 1024 ** 7,
        'YB': 1024 ** 8
    }

    # 尝试匹配单位
    unit_found = None
    num = None

    # 从大到小检查单位
    for unit in sorted(units.keys(), key=lambda x: -len(x)):
        if size_str.endswith(unit):
            num_str = size_str[:-len(unit)]
            try:
                num = float(num_str)
                unit_found = unit
                break
            except ValueError:
                continue

    # 如果没有找到匹配的单位，尝试解析整个字符串为数字(默认单位B)
    if unit_found is None:
        try:
            num = float(size_str)
            unit_found = 'B'
        except ValueError:
            return 0

    return int(num * units[unit_found])


def generate_file_from_args(size_str, file_name, save_location):
    """
    根据参数生成文件(命令行方式)
    :param size_str: 文件大小字符串
    :param file_name: 文件名
    :param save_location: 保存位置
    :return: 是否成功
    """
    # 处理文件名和扩展名
    if '.' not in file_name:
        file_name += lang.get('default_extension')  # 默认扩展名

    # 构建完整文件路径
    file_path = os.path.join(save_location, file_name)

    # 转换大小为字节
    apparent_size = get_size_in_bytes(size_str)
    if apparent_size <= 0:
        try:
            print(lang.get('cli_invalid_size'))
        except UnicodeEncodeError:
            print("Error: Invalid file size provided.")
        return False

    # 检查保存位置是否存在
    if not os.path.exists(save_location):
        try:
            print(lang.get('cli_save_location_not_exist', save_location))
        except UnicodeEncodeError:
            print(f"Error: Save location does not exist: {save_location}")
        return False

    # 检查文件是否已存在
    if os.path.exists(file_path):
        try:
            print(lang.get('file_overwrite_warning', file_path))
        except UnicodeEncodeError:
            print(f"Warning: File already exists and will be overwritten: {file_path}")

    try:
        # 创建文件
        create_dummy_large_file(file_path, apparent_size)
        try:
            print(lang.get('cli_file_created', file_path, size_str))
        except UnicodeEncodeError:
            print(f"Success: Virtual large file created successfully!")
            print(f"File path: {file_path}")
            print(f"Display size: {size_str}")
        return True
    except Exception as e:
        try:
            print(lang.get('cli_file_creation_failed', e))
        except UnicodeEncodeError:
            print(f"Error: Failed to create file - {e}")
        return False


def generate_file_gui():
    """
    图形界面方式生成文件 - 支持多语言的现代化界面
    """

    def on_language_change(event):
        """语言切换事件处理"""
        selected_display = language_var.get()
        lang_code = None
        
        # 从显示名称查找对应的语言代码
        for code in lang.get_available_languages().keys():
            display_name = lang.get_language_display_name(code, lang.get_current_language())
            if display_name == selected_display:
                lang_code = code
                break
        
        if lang_code and lang_code != lang.get_current_language():
            lang.set_language(lang_code)
            update_ui_texts()
            save_language_preference(lang_code)
            # 更新语言选择框的显示
            update_language_combo()

    def update_language_combo():
        """更新语言选择框的显示选项"""
        current_lang = lang.get_current_language()
        display_names = []
        lang_code_map = {}
        
        for code in lang.get_available_languages().keys():
            display_name = lang.get_language_display_name(code, current_lang)
            display_names.append(display_name)
            lang_code_map[display_name] = code
        
        # 更新下拉框选项
        language_combo['values'] = display_names
        
        # 设置当前选中项
        current_display = lang.get_language_display_name(current_lang, current_lang)
        language_var.set(current_display)

    def update_ui_texts():
        """更新界面文本"""
        root.title(lang.get('title'))
        
        # 更新菜单
        menubar.entryconfigure(1, label=lang.get('file'))
        menubar.entryconfigure(2, label=lang.get('view'))
        menubar.entryconfigure(3, label=lang.get('help'))
        
        # 重新创建帮助菜单 - 添加开源链接和关于选项
        help_menu.delete(0, 'end')
        help_menu.add_command(label=lang.get('open_source_link'), command=show_open_source_link)
        help_menu.add_separator()
        help_menu.add_command(label=lang.get('about'), command=show_about)
        
        # 更新语言标签为双语显示
        language_label.config(text=f"{lang.get('language')} (Language):")
        
        # 更新标签
        size_label.config(text=lang.get('file_size'))
        file_name_label.config(text=lang.get('file_name'))
        save_location_label.config(text=lang.get('save_location'))
        language_label.config(text=lang.get('language'))
        
        # 更新按钮
        browse_button.config(text=lang.get('browse'))
        generate_button.config(text=lang.get('generate'))
        
        # 更新说明文本
        note_label.config(text=lang.get('supported_units'))
        
        # 更新状态栏
        status_var.set(lang.get('ready'))

    def on_generate():
        """生成按钮点击事件处理"""
        size_str = size_entry.get()
        file_name = file_name_entry.get()
        save_location = save_location_entry.get()

        # 验证输入
        if not size_str:
            messagebox.showerror(lang.get('error'), lang.get('empty_file_size'))
            return

        if not file_name:
            messagebox.showerror(lang.get('error'), lang.get('empty_file_name'))
            return

        if not save_location:
            messagebox.showerror(lang.get('error'), lang.get('empty_save_location'))
            return

        # 处理文件名和扩展名
        if '.' not in file_name:
            file_name += lang.get('default_extension')  # 默认扩展名

        # 构建完整文件路径
        file_path = os.path.join(save_location, file_name)

        # 转换大小为字节
        apparent_size = get_size_in_bytes(size_str)
        if apparent_size <= 0:
            messagebox.showerror(lang.get('error'), lang.get('invalid_file_size'))
            return

        # 检查保存位置是否存在
        if not os.path.exists(save_location):
            messagebox.showerror(lang.get('error'), lang.get('save_location_not_exist', save_location))
            return

        # 检查文件是否已存在
        if os.path.exists(file_path):
            if not messagebox.askyesno(lang.get('warning'), lang.get('file_exists_overwrite', file_path)):
                return

        try:
            # 更新状态栏
            status_var.set(lang.get('processing'))
            root.update()
            
            # 创建文件
            create_dummy_large_file(file_path, apparent_size)
            messagebox.showinfo(lang.get('success'), lang.get('file_created_success', file_path, size_str))
            status_var.set(lang.get('operation_completed'))
            
            # 添加到最近文件
            add_to_recent_files(file_path)
            
        except Exception as e:
            messagebox.showerror(lang.get('error'), lang.get('file_creation_failed', e))
            status_var.set(lang.get('ready'))

    def browse_save_location():
        """浏览保存位置"""
        directory = filedialog.askdirectory(title=lang.get('select_save_location'))
        if directory:
            save_location_entry.delete(0, tk.END)
            save_location_entry.insert(0, directory)

    def add_to_recent_files(file_path):
        """添加到最近文件列表"""
        # 这里可以实现最近文件功能
        pass

    def show_about():
        """显示关于对话框"""
        about_text = f"{lang.get('app_name')}\n\n{lang.get('app_description')}\n\n{lang.get('version')}\n{lang.get('author')}\n\n© 2024 {lang.get('all_rights_reserved')}"
        messagebox.showinfo(lang.get('about'), about_text)

    def show_open_source_link():
        """显示开源链接"""
        try:
            import webbrowser
            webbrowser.open("https://github.com/small-orange-69/Sparse-File-Generator-")
            status_var.set(lang.get('open_source_link') + " - " + lang.get('link_opened'))
        except Exception as e:
            messagebox.showerror(lang.get('error'), lang.get('failed_to_open_link') + ": " + str(e))
            status_var.set(lang.get('error') + ": " + str(e))

    def save_language_preference(lang_code):
        """保存语言偏好设置"""
        try:
            config_dir = os.path.join(os.path.expanduser('~'), '.sparse_file_generator')
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            config_file = os.path.join(config_dir, 'config.json')
            with open(config_file, 'w', encoding='utf-8') as f:
                import json
                json.dump({'language': lang_code}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_language_preference():
        """加载语言偏好设置"""
        try:
            config_file = os.path.join(os.path.expanduser('~'), '.sparse_file_generator', 'config.json')
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    import json
                    config = json.load(f)
                    lang_code = config.get('language', 'zh_CN')
                    if lang_code in lang.get_available_languages():
                        lang.set_language(lang_code)
                        return lang_code
        except Exception:
            pass
        return 'zh_CN'

    # 创建主窗口
    root = tk.Tk()
    root.title(lang.get('title'))
    root.geometry("700x500")
    root.resizable(True, True)
    root.minsize(600, 400)
    
    # 设置窗口图标
    try:
        if os.path.exists("start.ico"):
            root.iconbitmap("start.ico")
    except:
        pass

    # 创建菜单栏
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # 文件菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=lang.get('file'), menu=file_menu)
    file_menu.add_command(label=lang.get('exit'), command=root.quit)

    # 查看菜单
    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=lang.get('view'), menu=view_menu)
    view_menu.add_command(label=lang.get('language'), command=lambda: language_frame.focus())

    # 帮助菜单 - 添加开源链接和关于选项
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=lang.get('help'), menu=help_menu)
    help_menu.add_command(label=lang.get('open_source_link'), command=show_open_source_link)
    help_menu.add_separator()
    help_menu.add_command(label=lang.get('about'), command=show_about)

    # 创建主框架
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 标题框架
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = ttk.Label(title_frame, text=lang.get('app_name'), font=('Arial', 16, 'bold'))
    title_label.pack(side=tk.LEFT)
    
    desc_label = ttk.Label(title_frame, text=lang.get('app_description'), font=('Arial', 10))
    desc_label.pack(side=tk.LEFT, padx=(10, 0))

    # 输入框架
    input_frame = ttk.LabelFrame(main_frame, text=lang.get('file_operations'), padding="15")
    input_frame.pack(fill=tk.X, pady=(0, 15))

    # 文件大小输入
    size_label = ttk.Label(input_frame, text=lang.get('file_size'))
    size_label.grid(row=0, column=0, sticky=tk.W, pady=8)
    size_entry = ttk.Entry(input_frame, width=25, font=('Arial', 11))
    size_entry.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(10, 0))
    size_entry.insert(0, "1GB")  # 默认值

    # 文件名输入
    file_name_label = ttk.Label(input_frame, text=lang.get('file_name'))
    file_name_label.grid(row=1, column=0, sticky=tk.W, pady=8)
    file_name_entry = ttk.Entry(input_frame, width=40, font=('Arial', 11))
    file_name_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, pady=8, padx=(10, 0))
    file_name_entry.insert(0, lang.get('default_filename'))  # 默认值

    # 保存位置选择
    save_location_label = ttk.Label(input_frame, text=lang.get('save_location'))
    save_location_label.grid(row=2, column=0, sticky=tk.W, pady=8)
    save_location_entry = ttk.Entry(input_frame, width=50, font=('Arial', 11))
    save_location_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=8, padx=(10, 0))
    save_location_entry.insert(0, os.getcwd())  # 默认当前目录

    browse_button = ttk.Button(input_frame, text=lang.get('browse'), command=browse_save_location)
    browse_button.grid(row=2, column=2, sticky=tk.W, pady=8, padx=(10, 0))

    # 语言选择框架
    language_frame = ttk.LabelFrame(main_frame, text=lang.get('settings'), padding="15")
    language_frame.pack(fill=tk.X, pady=(0, 15))
    
    language_label = ttk.Label(language_frame, text=f"{lang.get('language')} (Language):")
    language_label.grid(row=0, column=0, sticky=tk.W)
    
    language_var = tk.StringVar()
    language_combo = ttk.Combobox(language_frame, textvariable=language_var, 
                                 state='readonly', width=25)
    language_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
    language_combo.bind('<<ComboboxSelected>>', on_language_change)
    
    # 初始化语言选择框
    update_language_combo()

    # 按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(0, 15))
    
    generate_button = ttk.Button(button_frame, text=lang.get('generate'), command=on_generate, 
                                style='Accent.TButton')
    generate_button.pack(side=tk.RIGHT, padx=(10, 0))

    # 说明文本
    note_frame = ttk.LabelFrame(main_frame, text=lang.get('help'), padding="10")
    note_frame.pack(fill=tk.BOTH, expand=True)
    
    note_label = ttk.Label(note_frame, text=lang.get('supported_units'), wraplength=600, justify=tk.LEFT)
    note_label.pack(anchor=tk.W)

    # 状态栏
    status_frame = ttk.Frame(root)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0, 10))
    
    status_var = tk.StringVar()
    status_var.set(lang.get('ready'))
    status_label = ttk.Label(status_frame, textvariable=status_var, relief=tk.SUNKEN)
    status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # 配置网格权重
    input_frame.columnconfigure(1, weight=1)
    language_frame.columnconfigure(1, weight=1)

    # 加载用户语言偏好
    user_lang = load_language_preference()
    if user_lang != lang.get_current_language():
        lang.set_language(user_lang)
        update_language_combo()
        update_ui_texts()

    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    # 检查是否通过命令行参数调用
    if len(sys.argv) > 1 and sys.argv[1].upper() != 'GUI':
        # 命令行模式
        if len(sys.argv) != 4:
            print(lang.get('cli_usage_error'))
            print(lang.get('cli_usage_example'))
            sys.exit(1)

        size_str = sys.argv[1]
        file_name = sys.argv[2]
        save_location = sys.argv[3]

        success = generate_file_from_args(size_str, file_name, save_location)
        sys.exit(0 if success else 1)
    else:
        # GUI模式
        generate_file_gui()