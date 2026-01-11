import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QLinearGradient, QPainter, QPen, QFont
from PyQt5.QtWidgets import QLabel


class LogSyntaxHighlighter(QSyntaxHighlighter):
    """日志语法高亮器，用于为不同级别的日志着色"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlighting_rules = []

        # 信息级别 - 青色
        info_format = QTextCharFormat()
        info_format.setForeground(QColor("#00E5FF"))  # 青色
        info_pattern = r"\[INFO\]|信息|ℹ️"
        self.highlighting_rules.append((info_pattern, info_format))

        # 成功级别 - 绿色
        success_format = QTextCharFormat()
        success_format.setForeground(QColor("#4CAF50"))  # 绿色
        success_pattern = r"\[SUCCESS\]|成功|✅|完成|✓|Succeed"
        self.highlighting_rules.append((success_pattern, success_format))

        # 警告级别 - 黄色
        warning_format = QTextCharFormat()
        warning_format.setForeground(QColor("#FFC107"))  # 黄色
        warning_pattern = r"\[WARNING\]|警告|⚠️|注意|Warning"
        self.highlighting_rules.append((warning_pattern, warning_format))

        # 错误级别 - 红色
        error_format = QTextCharFormat()
        error_format.setForeground(QColor("#FF5252"))  # 红色
        error_pattern = r"\[ERROR\]|错误|❌|失败|错误:|Error|Failed|失败"
        self.highlighting_rules.append((error_pattern, error_format))

        # 进度级别 - 蓝色
        progress_format = QTextCharFormat()
        progress_format.setForeground(QColor("#2196F3"))  # 蓝色
        progress_pattern = r"\[PROGRESS\]|进度|⏳|下载中|Processing|下载进度"
        self.highlighting_rules.append((progress_pattern, progress_format))

        # 时间戳 - 灰色
        time_format = QTextCharFormat()
        time_format.setForeground(QColor("#90A4AE"))  # 灰色
        time_pattern = r"\d{2}:\d{2}:\d{2}|\d{4}-\d{2}-\d{2}"
        self.highlighting_rules.append((time_pattern, time_format))

        # URL链接 - 紫色
        url_format = QTextCharFormat()
        url_format.setForeground(QColor("#E040FB"))  # 紫色
        url_format.setFontUnderline(True)
        url_pattern = r"https?://[^\s]+|www\.[^\s]+"
        self.highlighting_rules.append((url_pattern, url_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = re.compile(pattern, re.IGNORECASE)
            for match in expression.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)


class GradientLabel(QLabel):
    """渐变文字标签"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.gradient = QLinearGradient(0, 0, 0, 1)
        self.gradient.setColorAt(0, QColor("#00E5FF"))  # 顶部颜色
        self.gradient.setColorAt(0.5, QColor("#4FC3F7"))  # 中间颜色
        self.gradient.setColorAt(1, QColor("#00B0FF"))  # 底部颜色

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置渐变画笔
        pen = QPen()
        pen.setBrush(self.gradient)
        pen.setWidth(1)
        painter.setPen(pen)

        # 绘制渐变文字
        rect = self.rect()
        self.gradient.setFinalStop(0, rect.height())

        # 获取字体并应用
        font = QFont("Source Code Pro", 14, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        painter.setFont(font)

        # 绘制文本
        painter.drawText(rect, Qt.AlignCenter, self.text())