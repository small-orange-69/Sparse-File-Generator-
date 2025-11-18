import json
import os
from typing import Dict, Optional


class LanguageManager:
    """多语言管理器"""
    
    def __init__(self, languages_dir: str = "languages"):
        self.languages_dir = languages_dir
        # 优先使用环境变量中的语言设置，否则使用默认语言
        self.current_language = os.environ.get('USER_LANGUAGE', 'zh_CN')
        self.translations = {}
        self.available_languages = {}
        
        # 创建语言目录
        if not os.path.exists(self.languages_dir):
            os.makedirs(self.languages_dir)
            
        self._init_default_languages()
        # 尝试加载用户语言，如果失败则回退到默认语言
        if not self.load_language(self.current_language):
            self.current_language = 'zh_CN'
            self.load_language(self.current_language)
    
    def _init_default_languages(self):
        """初始化默认语言文件"""
        # 中文简体
        zh_cn = {
            "title": "稀疏文件生成器",
            "file_size": "文件大小:",
            "file_name": "文件名:",
            "save_location": "保存位置:",
            "browse": "浏览...",
            "generate": "生成",
            "supported_units": "支持的单位: B, KB, MB, GB, TB, PB, EB, ZB, YB (例如: 1GB, 500MB, 2PB)",
            "error": "错误",
            "success": "成功",
            "warning": "警告",
            "confirm": "确认",
            "cancel": "取消",
            "close": "关闭",
            "language": "语言:",
            "about": "关于",
            "help": "帮助",
            "file": "文件",
            "settings": "设置",
            "invalid_file_size": "无效的文件大小",
            "empty_file_size": "请输入文件大小",
            "empty_file_name": "请输入文件名",
            "empty_save_location": "请选择保存位置",
            "save_location_not_exist": "保存位置 {} 不存在",
            "file_exists_overwrite": "文件 {} 已存在，是否覆盖?",
            "file_created_success": "虚拟大文件创建成功!\n文件路径: {}\n显示大小: {}",
            "file_creation_failed": "创建失败: {}",
            "file_overwrite_warning": "警告: 文件 {} 已存在，将被覆盖",
            "cli_usage_error": "错误: 需要3个参数 - 文件大小, 文件名, 保存路径",
            "cli_usage_example": "示例: python sparse_file_generator.py 1GB ex.bin c:\\",
            "cli_invalid_size": "错误: 无效的文件大小",
            "cli_save_location_not_exist": "错误: 保存位置 {} 不存在",
            "cli_file_created": "成功: 虚拟大文件创建成功!\n文件路径: {}\n显示大小: {}",
            "cli_file_creation_failed": "错误: 创建失败: {}",
            "cli_no_args": "错误: 未提供命令行参数。请提供文件大小、文件名和保存路径。",
            "default_filename": "dummy_file",
            "default_extension": ".bin",
            "select_save_location": "选择保存位置",
            "app_name": "稀疏文件生成器",
            "app_description": "创建显示为大文件但实际上占用空间很小的文件",
            "version": "版本: 2.0",
            "author": "作者: Small Orange",
            "all_rights_reserved": "版权所有",
            "file_operations": "文件操作",
            "exit": "退出",
            "view": "查看",
            "tools": "工具",
            "reset_settings": "重置设置",
            "save_settings": "保存设置",
            "general": "常规",
            "appearance": "外观",
            "advanced": "高级",
            "theme": "主题:",
            "light": "浅色",
            "dark": "深色",
            "auto": "自动",
            "font_size": "字体大小:",
            "small": "小",
            "medium": "中",
            "large": "大",
            "auto_start": "开机自启",
            "minimize_to_tray": "最小化到系统托盘",
            "show_notifications": "显示通知",
            "log_operations": "记录操作日志",
            "clear_log": "清除日志",
            "open_log": "打开日志",
            "log_location": "日志位置:",
            "operation_completed": "操作完成",
            "ready": "就绪",
            "processing": "处理中...",
            "drag_drop_supported": "支持拖拽文件",
            "quick_access": "快速访问",
            "recent_files": "最近文件",
            "clear_recent": "清除最近",
            "no_recent_files": "没有最近文件",
            "file_properties": "文件属性",
            "size": "大小",
            "location": "位置",
            "created": "创建时间",
            "modified": "修改时间",
            "accessed": "访问时间",
            "attributes": "属性",
            "compression": "压缩",
            "encryption": "加密",
            "indexing": "索引",
            "open_source_link": "开源链接",
            "link_opened": "链接已打开",
            "failed_to_open_link": "无法打开链接"
        }
        
        # 英文
        en_us = {
            "title": "Sparse File Generator",
            "file_size": "File Size:",
            "file_name": "File Name:",
            "save_location": "Save Location:",
            "browse": "Browse...",
            "generate": "Generate",
            "supported_units": "Supported units: B, KB, MB, GB, TB, PB, EB, ZB, YB (e.g.: 1GB, 500MB, 2PB)",
            "error": "Error",
            "success": "Success",
            "warning": "Warning",
            "confirm": "Confirm",
            "cancel": "Cancel",
            "close": "Close",
            "language": "Language:",
            "about": "About",
            "help": "Help",
            "file": "File",
            "settings": "Settings",
            "invalid_file_size": "Invalid file size",
            "empty_file_size": "Please enter file size",
            "empty_file_name": "Please enter file name",
            "empty_save_location": "Please select save location",
            "save_location_not_exist": "Save location {} does not exist",
            "file_exists_overwrite": "File {} already exists, overwrite?",
            "file_created_success": "Virtual large file created successfully!\nFile path: {}\nDisplay size: {}",
            "file_creation_failed": "Creation failed: {}",
            "file_overwrite_warning": "Warning: File {} already exists and will be overwritten",
            "cli_usage_error": "Error: 3 arguments required - file size, file name, save path",
            "cli_usage_example": "Example: python sparse_file_generator.py 1GB ex.bin c:\\",
            "cli_invalid_size": "Error: Invalid file size",
            "cli_save_location_not_exist": "Error: Save location {} does not exist",
            "cli_file_created": "Success: Virtual large file created successfully!\nFile path: {}\nDisplay size: {}",
            "cli_file_creation_failed": "Error: Creation failed: {}",
            "cli_no_args": "Error: No command line arguments provided. Please provide file size, file name, and save path.",
            "default_filename": "dummy_file",
            "default_extension": ".bin",
            "select_save_location": "Select Save Location",
            "app_name": "Sparse File Generator",
            "app_description": "Create files that appear large but actually take up very little space",
            "version": "Version: 2.0",
            "author": "Author: Small Orange",
            "all_rights_reserved": "All Rights Reserved",
            "file_operations": "File Operations",
            "exit": "Exit",
            "view": "View",
            "tools": "Tools",
            "reset_settings": "Reset Settings",
            "save_settings": "Save Settings",
            "general": "General",
            "appearance": "Appearance",
            "advanced": "Advanced",
            "theme": "Theme:",
            "light": "Light",
            "dark": "Dark",
            "auto": "Auto",
            "font_size": "Font Size:",
            "small": "Small",
            "medium": "Medium",
            "large": "Large",
            "auto_start": "Start with Windows",
            "minimize_to_tray": "Minimize to System Tray",
            "show_notifications": "Show Notifications",
            "log_operations": "Log Operations",
            "clear_log": "Clear Log",
            "open_log": "Open Log",
            "log_location": "Log Location:",
            "operation_completed": "Operation Completed",
            "ready": "Ready",
            "processing": "Processing...",
            "drag_drop_supported": "Drag & Drop Supported",
            "quick_access": "Quick Access",
            "recent_files": "Recent Files",
            "clear_recent": "Clear Recent",
            "no_recent_files": "No Recent Files",
            "file_properties": "File Properties",
            "size": "Size",
            "location": "Location",
            "created": "Created",
            "modified": "Modified",
            "accessed": "Accessed",
            "attributes": "Attributes",
            "compression": "Compression",
            "encryption": "Encryption",
            "indexing": "Indexing",
            "open_source_link": "Open Source Link",
            "link_opened": "Link opened",
            "failed_to_open_link": "Failed to open link"
        }
        
        # 日文
        ja_jp = {
            "title": "スパースファイル生成器",
            "file_size": "ファイルサイズ:",
            "file_name": "ファイル名:",
            "save_location": "保存場所:",
            "browse": "参照...",
            "generate": "生成",
            "supported_units": "サポート単位: B, KB, MB, GB, TB, PB, EB, ZB, YB (例: 1GB, 500MB, 2PB)",
            "error": "エラー",
            "success": "成功",
            "warning": "警告",
            "confirm": "確認",
            "cancel": "キャンセル",
            "close": "閉じる",
            "language": "言語:",
            "about": "について",
            "help": "ヘルプ",
            "file": "ファイル",
            "settings": "設定",
            "invalid_file_size": "無効なファイルサイズ",
            "empty_file_size": "ファイルサイズを入力してください",
            "empty_file_name": "ファイル名を入力してください",
            "empty_save_location": "保存場所を選択してください",
            "save_location_not_exist": "保存場所 {} は存在しません",
            "file_exists_overwrite": "ファイル {} は既に存在します。上書きしますか？",
            "file_created_success": "仮想大ファイルが正常に作成されました！\nファイルパス: {}\n表示サイズ: {}",
            "file_creation_failed": "作成に失敗しました: {}",
            "file_overwrite_warning": "警告: ファイル {} は既に存在し、上書きされます",
            "cli_usage_error": "エラー: 3つの引数が必要です - ファイルサイズ、ファイル名、保存パス",
            "cli_usage_example": "例: python sparse_file_generator.py 1GB ex.bin c:\\",
            "cli_invalid_size": "エラー: 無効なファイルサイズ",
            "cli_save_location_not_exist": "エラー: 保存場所 {} は存在しません",
            "cli_file_created": "成功: 仮想大ファイルが正常に作成されました！\nファイルパス: {}\n表示サイズ: {}",
            "cli_file_creation_failed": "エラー: 作成に失敗しました: {}",
            "cli_no_args": "エラー: コマンドライン引数が提供されていません。ファイルサイズ、ファイル名、保存パスを提供してください。",
            "default_filename": "dummy_file",
            "default_extension": ".bin",
            "select_save_location": "保存場所を選択",
            "app_name": "スパースファイル生成器",
            "app_description": "実際には非常に少ない容量しか占有しないが、大きなファイルとして表示されるファイルを作成",
            "version": "バージョン: 2.0",
            "author": "作者: Small Orange",
            "all_rights_reserved": "All Rights Reserved",
            "file_operations": "ファイル操作",
            "exit": "終了",
            "view": "表示",
            "tools": "ツール",
            "reset_settings": "設定をリセット",
            "save_settings": "設定を保存",
            "general": "一般",
            "appearance": "外観",
            "advanced": "詳細",
            "theme": "テーマ:",
            "light": "ライト",
            "dark": "ダーク",
            "auto": "自動",
            "font_size": "フォントサイズ:",
            "small": "小",
            "medium": "中",
            "large": "大",
            "auto_start": "Windows起動時に開始",
            "minimize_to_tray": "システムトレイに最小化",
            "show_notifications": "通知を表示",
            "log_operations": "操作ログを記録",
            "clear_log": "ログをクリア",
            "open_log": "ログを開く",
            "log_location": "ログ場所:",
            "operation_completed": "操作完了",
            "ready": "準備完了",
            "processing": "処理中...",
            "drag_drop_supported": "ドラッグ＆ドロップ対応",
            "quick_access": "クイックアクセス",
            "recent_files": "最近のファイル",
            "clear_recent": "最近をクリア",
            "no_recent_files": "最近のファイルなし",
            "file_properties": "ファイルプロパティ",
            "size": "サイズ",
            "location": "場所",
            "created": "作成日時",
            "modified": "更新日時",
            "accessed": "アクセス日時",
            "attributes": "属性",
            "compression": "圧縮",
            "encryption": "暗号化",
            "indexing": "インデックス",
            "open_source_link": "オープンソースリンク",
            "link_opened": "リンクが開かれました",
            "failed_to_open_link": "リンクを開けませんでした"
        }
        
        # 韩文
        ko_kr = {
            "title": "스파스 파일 생성기",
            "file_size": "파일 크기:",
            "file_name": "파일 이름:",
            "save_location": "저장 위치:",
            "browse": "찾아보기...",
            "generate": "생성",
            "supported_units": "지원 단위: B, KB, MB, GB, TB, PB, EB, ZB, YB (예: 1GB, 500MB, 2PB)",
            "error": "오류",
            "success": "성공",
            "warning": "경고",
            "confirm": "확인",
            "cancel": "취소",
            "close": "닫기",
            "language": "언어:",
            "about": "정보",
            "help": "도움말",
            "file": "파일",
            "settings": "설정",
            "invalid_file_size": "잘못된 파일 크기",
            "empty_file_size": "파일 크기를 입력하세요",
            "empty_file_name": "파일 이름을 입력하세요",
            "empty_save_location": "저장 위치를 선택하세요",
            "save_location_not_exist": "저장 위치 {} 가 존재하지 않습니다",
            "file_exists_overwrite": "파일 {} 이(가) 이미 존재합니다. 덮어쓰시겠습니까?",
            "file_created_success": "가상 대용량 파일이 성공적으로 생성되었습니다!\n파일 경로: {}\n표시 크기: {}",
            "file_creation_failed": "생성 실패: {}",
            "file_overwrite_warning": "경고: 파일 {} 이(가) 이미 존재하며 덮어쓰기됩니다",
            "cli_usage_error": "오류: 3개의 인수가 필요합니다 - 파일 크기, 파일 이름, 저장 경로",
            "cli_usage_example": "예: python sparse_file_generator.py 1GB ex.bin c:\\",
            "cli_invalid_size": "오류: 잘못된 파일 크기",
            "cli_save_location_not_exist": "오류: 저장 위치 {} 가 존재하지 않습니다",
            "cli_file_created": "성공: 가상 대용량 파일이 성공적으로 생성되었습니다!\n파일 경로: {}\n표시 크기: {}",
            "cli_file_creation_failed": "오류: 생성 실패: {}",
            "cli_no_args": "오류: 명령줄 인수가 제공되지 않았습니다. 파일 크기, 파일 이름, 저장 경로를 제공하세요.",
            "default_filename": "dummy_file",
            "default_extension": ".bin",
            "select_save_location": "저장 위치 선택",
            "app_name": "스파스 파일 생성기",
            "app_description": "실제로는 매우 적은 공간만 차지하지만 큰 파일로 표시되는 파일 생성",
            "version": "버전: 2.0",
            "author": "작성자: Small Orange",
            "all_rights_reserved": "All Rights Reserved",
            "file_operations": "파일 작업",
            "exit": "종료",
            "view": "보기",
            "tools": "문서",
            "reset_settings": "설정 재설정",
            "save_settings": "설정 저장",
            "general": "일반",
            "appearance": "모양",
            "advanced": "고급",
            "theme": "테마:",
            "light": "라이트",
            "dark": "다크",
            "auto": "자동",
            "font_size": "글꼴 크기:",
            "small": "작음",
            "medium": "중간",
            "large": "큼",
            "auto_start": "Windows 시작 시 시작",
            "minimize_to_tray": "시스템 트레이로 최소화",
            "show_notifications": "알림 표시",
            "log_operations": "작업 로그 기록",
            "clear_log": "로그 지우기",
            "open_log": "로그 열기",
            "log_location": "로그 위치:",
            "operation_completed": "작업 완료",
            "ready": "준비",
            "processing": "처리 중...",
            "drag_drop_supported": "드래그 앤 드롭 지원",
            "quick_access": "빠른 액세스",
            "recent_files": "최근 파일",
            "clear_recent": "최근 항목 지우기",
            "no_recent_files": "최근 파일 없음",
            "file_properties": "파일 속성",
            "size": "크기",
            "location": "위치",
            "created": "생성 시간",
            "modified": "수정 시간",
            "accessed": "액세스 시간",
            "attributes": "속성",
            "compression": "압축",
            "encryption": "암호화",
            "indexing": "인덱싱",
            "open_source_link": "오픈소스 링크",
            "link_opened": "링크가 열렸습니다",
            "failed_to_open_link": "링크를 열 수 없습니다"
        }
        
        # 法文
        fr_fr = {
            "title": "Générateur de Fichiers Éparses",
            "file_size": "Taille du Fichier:",
            "file_name": "Nom du Fichier:",
            "save_location": "Emplacement de Sauvegarde:",
            "browse": "Parcourir...",
            "generate": "Générer",
            "supported_units": "Unités supportées: B, KB, MB, GB, TB, PB, EB, ZB, YB (ex: 1GB, 500MB, 2PB)",
            "error": "Erreur",
            "success": "Succès",
            "warning": "Avertissement",
            "confirm": "Confirmer",
            "cancel": "Annuler",
            "close": "Fermer",
            "language": "Langue:",
            "about": "À propos",
            "help": "Aide",
            "file": "Fichier",
            "settings": "Paramètres",
            "invalid_file_size": "Taille de fichier invalide",
            "empty_file_size": "Veuillez entrer la taille du fichier",
            "empty_file_name": "Veuillez entrer le nom du fichier",
            "empty_save_location": "Veuillez sélectionner l'emplacement de sauvegarde",
            "save_location_not_exist": "L'emplacement de sauvegarde {} n'existe pas",
            "file_exists_overwrite": "Le fichier {} existe déjà, l'écraser?",
            "file_created_success": "Fichier virtuel de grande taille créé avec succès!\nChemin du fichier: {}\nTaille affichée: {}",
            "file_creation_failed": "Échec de la création: {}",
            "file_overwrite_warning": "Avertissement: Le fichier {} existe déjà et sera écrasé",
            "cli_usage_error": "Erreur: 3 arguments requis - taille du fichier, nom du fichier, chemin de sauvegarde",
            "cli_usage_example": "Exemple: python sparse_file_generator.py 1GB ex.bin c:\\",
            "cli_invalid_size": "Erreur: Taille de fichier invalide",
            "cli_save_location_not_exist": "Erreur: L'emplacement de sauvegarde {} n'existe pas",
            "cli_file_created": "Succès: Fichier virtuel de grande taille créé avec succès!\nChemin du fichier: {}\nTaille affichée: {}",
            "cli_file_creation_failed": "Erreur: Échec de la création: {}",
            "cli_no_args": "Erreur: Aucun argument de ligne de commande fourni. Veuillez fournir la taille du fichier, le nom du fichier et le chemin de sauvegarde.",
            "default_filename": "fichier_dummy",
            "default_extension": ".bin",
            "select_save_location": "Sélectionner l'Emplacement de Sauvegarde",
            "app_name": "Générateur de Fichiers Éparses",
            "app_description": "Créer des fichiers qui semblent grands mais occupent en fait très peu d'espace",
            "version": "Version: 2.0",
            "author": "Auteur: Small Orange",
            "all_rights_reserved": "Tous Droits Réservés",
            "file_operations": "Opérations de Fichier",
            "exit": "Quitter",
            "view": "Affichage",
            "tools": "Outils",
            "reset_settings": "Réinitialiser les Paramètres",
            "save_settings": "Enregistrer les Paramètres",
            "general": "Général",
            "appearance": "Apparence",
            "advanced": "Avancé",
            "theme": "Thème:",
            "light": "Clair",
            "dark": "Sombre",
            "auto": "Automatique",
            "font_size": "Taille de Police:",
            "small": "Petit",
            "medium": "Moyen",
            "large": "Grand",
            "auto_start": "Démarrer avec Windows",
            "minimize_to_tray": "Minimiser dans la Barre des Tâches",
            "show_notifications": "Afficher les Notifications",
            "log_operations": "Journal des Opérations",
            "clear_log": "Effacer le Journal",
            "open_log": "Ouvrir le Journal",
            "log_location": "Emplacement du Journal:",
            "operation_completed": "Opération Terminée",
            "ready": "Prêt",
            "processing": "Traitement...",
            "drag_drop_supported": "Glisser-Déposer Supporté",
            "quick_access": "Accès Rapide",
            "recent_files": "Fichiers Récents",
            "clear_recent": "Effacer les Récents",
            "no_recent_files": "Aucun Fichier Récent",
            "file_properties": "Propriétés du Fichier",
            "size": "Taille",
            "location": "Emplacement",
            "created": "Créé",
            "modified": "Modifié",
            "accessed": "Accédé",
            "attributes": "Attributs",
            "compression": "Compression",
            "encryption": "Chiffrement",
            "indexing": "Indexation",
            "open_source_link": "Lien Open Source",
            "link_opened": "Lien ouvert",
            "failed_to_open_link": "Impossible d'ouvrir le lien"
        }
        
        # 德文
        de_de = {
            "title": "Sparse-Datei Generator",
            "file_size": "Dateigröße:",
            "file_name": "Dateiname:",
            "save_location": "Speicherort:",
            "browse": "Durchsuchen...",
            "generate": "Erzeugen",
            "supported_units": "Unterstützte Einheiten: B, KB, MB, GB, TB, PB, EB, ZB, YB (z.B.: 1GB, 500MB, 2PB)",
            "error": "Fehler",
            "success": "Erfolg",
            "warning": "Warnung",
            "confirm": "Bestätigen",
            "cancel": "Abbrechen",
            "close": "Schließen",
            "language": "Sprache:",
            "about": "Über",
            "help": "Hilfe",
            "file": "Datei",
            "settings": "Einstellungen",
            "invalid_file_size": "Ungültige Dateigröße",
            "empty_file_size": "Bitte Dateigröße eingeben",
            "empty_file_name": "Bitte Dateinamen eingeben",
            "empty_save_location": "Bitte Speicherort auswählen",
            "save_location_not_exist": "Speicherort {} existiert nicht",
            "file_exists_overwrite": "Datei {} existiert bereits, überschreiben?",
            "file_created_success": "Virtuelle große Datei erfolgreich erstellt!\nDateipfad: {}\nAnzeigegröße: {}",
            "file_creation_failed": "Erstellung fehlgeschlagen: {}",
            "file_overwrite_warning": "Warnung: Datei {} existiert bereits und wird überschrieben",
            "cli_usage_error": "Fehler: 3 Argumente erforderlich - Dateigröße, Dateiname, Speicherpfad",
            "cli_usage_example": "Beispiel: python sparse_file_generator.py 1GB ex.bin c:\\",
            "cli_invalid_size": "Fehler: Ungültige Dateigröße",
            "cli_save_location_not_exist": "Fehler: Speicherort {} existiert nicht",
            "cli_file_created": "Erfolg: Virtuelle große Datei erfolgreich erstellt!\nDateipfad: {}\nAnzeigegröße: {}",
            "cli_file_creation_failed": "Fehler: Erstellung fehlgeschlagen: {}",
            "cli_no_args": "Fehler: Keine Befehlszeilenargumente angegeben. Bitte Dateigröße, Dateiname und Speicherpfad angeben.",
            "default_filename": "dummy_datei",
            "default_extension": ".bin",
            "select_save_location": "Speicherort Auswählen",
            "app_name": "Sparse-Datei Generator",
            "app_description": "Erstellen Sie Dateien, die groß erscheinen, aber tatsächlich sehr wenig Speicherplatz belegen",
            "version": "Version: 2.0",
            "author": "Autor: Small Orange",
            "all_rights_reserved": "Alle Rechte Vorbehalten",
            "file_operations": "Dateioperationen",
            "exit": "Beenden",
            "view": "Ansicht",
            "tools": "Werkzeuge",
            "reset_settings": "Einstellungen Zurücksetzen",
            "save_settings": "Einstellungen Speichern",
            "general": "Allgemein",
            "appearance": "Erscheinungsbild",
            "advanced": "Erweitert",
            "theme": "Thema:",
            "light": "Hell",
            "dark": "Dunkel",
            "auto": "Automatisch",
            "font_size": "Schriftgröße:",
            "small": "Klein",
            "medium": "Mittel",
            "large": "Groß",
            "auto_start": "Mit Windows Starten",
            "minimize_to_tray": "In Taskleiste Minimieren",
            "show_notifications": "Benachrichtigungen Anzeigen",
            "log_operations": "Vorgänge Protokollieren",
            "clear_log": "Protokoll Löschen",
            "open_log": "Protokoll Öffnen",
            "log_location": "Protokoll Speicherort:",
            "operation_completed": "Vorgang Abgeschlossen",
            "ready": "Bereit",
            "processing": "Verarbeitung...",
            "drag_drop_supported": "Drag & Drop Unterstützt",
            "quick_access": "Schnellzugriff",
            "recent_files": "Neueste Dateien",
            "clear_recent": "Neueste Löschen",
            "no_recent_files": "Keine Neuesten Dateien",
            "file_properties": "Dateieigenschaften",
            "size": "Größe",
            "location": "Speicherort",
            "created": "Erstellt",
            "modified": "Geändert",
            "accessed": "Zugegriffen",
            "attributes": "Attribute",
            "compression": "Kompression",
            "encryption": "Verschlüsselung",
            "indexing": "Indizierung",
            "open_source_link": "Open-Source-Link",
            "link_opened": "Link geöffnet",
            "failed_to_open_link": "Link konnte nicht geöffnet werden"
        }
        
        # 西班牙文
        es_es = {
            "title": "Generador de Archivos Dispersos",
            "file_size": "Tamaño del Archivo:",
            "file_name": "Nombre del Archivo:",
            "save_location": "Ubicación de Guardado:",
            "browse": "Explorar...",
            "generate": "Generar",
            "supported_units": "Unidades soportadas: B, KB, MB, GB, TB, PB, EB, ZB, YB (ej: 1GB, 500MB, 2PB)",
            "error": "Error",
            "success": "Éxito",
            "warning": "Advertencia",
            "confirm": "Confirmar",
            "cancel": "Cancelar",
            "close": "Cerrar",
            "language": "Idioma:",
            "about": "Acerca de",
            "help": "Ayuda",
            "file": "Archivo",
            "settings": "Configuración",
            "invalid_file_size": "Tamaño de archivo inválido",
            "empty_file_size": "Por favor ingrese el tamaño del archivo",
            "empty_file_name": "Por favor ingrese el nombre del archivo",
            "empty_save_location": "Por favor seleccione la ubicación de guardado",
            "save_location_not_exist": "La ubicación de guardado {} no existe",
            "file_exists_overwrite": "El archivo {} ya existe, ¿sobrescribir?",
            "file_created_success": "¡Archivo virtual de gran tamaño creado exitosamente!\nRuta del archivo: {}\nTamaño mostrado: {}",
            "file_creation_failed": "Falló la creación: {}",
            "file_overwrite_warning": "Advertencia: El archivo {} ya existe y será sobrescrito",
            "cli_usage_error": "Error: Se requieren 3 argumentos - tamaño del archivo, nombre del archivo, ruta de guardado",
            "cli_usage_example": "Ejemplo: python sparse_file_generator.py 1GB ex.bin c:\\",
            "cli_invalid_size": "Error: Tamaño de archivo inválido",
            "cli_save_location_not_exist": "Error: La ubicación de guardado {} no existe",
            "cli_file_created": "Éxito: ¡Archivo virtual de gran tamaño creado exitosamente!\nRuta del archivo: {}\nTamaño mostrado: {}",
            "cli_file_creation_failed": "Error: Falló la creación: {}",
            "cli_no_args": "Error: No se proporcionaron argumentos de línea de comandos. Por favor proporcione el tamaño del archivo, el nombre del archivo y la ruta de guardado.",
            "default_filename": "archivo_dummy",
            "default_extension": ".bin",
            "select_save_location": "Seleccionar Ubicación de Guardado",
            "app_name": "Generador de Archivos Dispersos",
            "app_description": "Crear archivos que parecen grandes pero en realidad ocupan muy poco espacio",
            "version": "Versión: 2.0",
            "author": "Autor: Small Orange",
            "all_rights_reserved": "Todos los Derechos Reservados",
            "file_operations": "Operaciones de Archivo",
            "exit": "Salir",
            "view": "Ver",
            "tools": "Herramientas",
            "reset_settings": "Restablecer Configuración",
            "save_settings": "Guardar Configuración",
            "general": "General",
            "appearance": "Apariencia",
            "advanced": "Avanzado",
            "theme": "Tema:",
            "light": "Claro",
            "dark": "Oscuro",
            "auto": "Automático",
            "font_size": "Tamaño de Fuente:",
            "small": "Pequeño",
            "medium": "Mediano",
            "large": "Grande",
            "auto_start": "Iniciar con Windows",
            "minimize_to_tray": "Minimizar a la Bandeja del Sistema",
            "show_notifications": "Mostrar Notificaciones",
            "log_operations": "Registrar Operaciones",
            "clear_log": "Borrar Registro",
            "open_log": "Abrir Registro",
            "log_location": "Ubicación del Registro:",
            "operation_completed": "Operación Completada",
            "ready": "Listo",
            "processing": "Procesando...",
            "drag_drop_supported": "Arrastrar y Soltar Soportado",
            "quick_access": "Acceso Rápido",
            "recent_files": "Archivos Recientes",
            "clear_recent": "Borrar Recientes",
            "no_recent_files": "Sin Archivos Recientes",
            "file_properties": "Propiedades del Archivo",
            "size": "Tamaño",
            "location": "Ubicación",
            "created": "Creado",
            "modified": "Modificado",
            "accessed": "Accedido",
            "attributes": "Atributos",
            "compression": "Compresión",
            "encryption": "Cifrado",
            "indexing": "Indexación",
            "open_source_link": "Enlace de Código Abierto",
            "link_opened": "Enlace abierto",
            "failed_to_open_link": "No se pudo abrir el enlace"
        }
        
        # 保存语言文件
        self._save_language_file("zh_CN", zh_cn)
        self._save_language_file("en_US", en_us)
        self._save_language_file("ja_JP", ja_jp)
        self._save_language_file("ko_KR", ko_kr)
        self._save_language_file("fr_FR", fr_fr)
        self._save_language_file("de_DE", de_de)
        self._save_language_file("es_ES", es_es)
        
        # 更新可用语言列表
        self.available_languages = {
            "zh_CN": "简体中文",
            "en_US": "English",
            "ja_JP": "日本語",
            "ko_KR": "한국어",
            "fr_FR": "Français",
            "de_DE": "Deutsch",
            "es_ES": "Español"
        }
    
    def _save_language_file(self, lang_code: str, translations: Dict):
        """保存语言文件"""
        file_path = os.path.join(self.languages_dir, f"{lang_code}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存语言文件失败 {lang_code}: {e}")
    
    def load_language(self, lang_code: str) -> bool:
        """加载语言文件"""
        file_path = os.path.join(self.languages_dir, f"{lang_code}.json")
        
        if not os.path.exists(file_path):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
                self.current_language = lang_code
                return True
        except Exception as e:
            print(f"加载语言文件失败 {lang_code}: {e}")
            return False
    
    def get(self, key: str, *args) -> str:
        """获取翻译文本"""
        text = self.translations.get(key, key)
        if args:
            try:
                return text.format(*args)
            except:
                return text
        return text
    
    def set_language(self, lang_code: str) -> bool:
        """设置当前语言"""
        if lang_code in self.available_languages:
            return self.load_language(lang_code)
        return False
    
    def get_available_languages(self) -> Dict[str, str]:
        """获取可用语言列表"""
        return self.available_languages.copy()
    
    def get_language_display_name(self, lang_code: str, current_lang_code: str = None) -> str:
        """获取语言的双语显示名称"""
        if current_lang_code is None:
            current_lang_code = self.current_language
            
        # 获取当前语言的名称
        current_lang_name = self.available_languages.get(lang_code, lang_code)
        
        # 获取该语言在本地的名称
        local_name_map = {
            'zh_CN': '简体中文',
            'en_US': 'English',
            'ja_JP': '日本語',
            'ko_KR': '한국어',
            'fr_FR': 'Français',
            'de_DE': 'Deutsch',
            'es_ES': 'Español'
        }
        
        local_name = local_name_map.get(lang_code, lang_code)
        
        # 如果当前语言不是该语言本身，显示双语名称
        if current_lang_code != lang_code:
            return f"{current_lang_name} ({local_name})"
        else:
            return local_name
    
    def get_current_language(self) -> str:
        """获取当前语言代码"""
        return self.current_language
    
    def get_language_name(self, lang_code: str) -> str:
        """获取语言名称"""
        return self.available_languages.get(lang_code, lang_code)


# 全局语言管理器实例
lang = LanguageManager()