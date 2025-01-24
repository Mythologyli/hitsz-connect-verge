from qfluentwidgets import (LineEdit, SwitchButton, BodyLabel,
                          PushButton, FluentIcon)
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout
from .config_utils import save_config
from .startup_utils import set_launch_at_login, get_launch_at_login

class AdvancedSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('高级设置')
        self.setFixedWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Server settings
        layout.addWidget(BodyLabel('SSL VPN 服务端地址'))
        self.server_input = LineEdit(self)
        self.server_input.setPlaceholderText('vpn.hitsz.edu.cn')
        layout.addWidget(self.server_input)

        # DNS settings
        layout.addWidget(BodyLabel('DNS 服务器地址'))
        self.dns_input = LineEdit(self)
        self.dns_input.setPlaceholderText('10.248.98.30')
        layout.addWidget(self.dns_input)
        
        # Proxy Control
        layout.addWidget(BodyLabel('自动配置代理'))
        self.proxy_switch = SwitchButton(self)
        self.proxy_switch.setChecked(self.proxy_switch)
        layout.addWidget(self.proxy_switch)

        # Login option
        layout.addWidget(BodyLabel('开机启动'))
        self.startup_switch = SwitchButton(self)
        self.startup_switch.setChecked(get_launch_at_login())
        layout.addWidget(self.startup_switch)

        # Connect on startup
        layout.addWidget(BodyLabel('启动时自动连接'))
        self.connect_startup = SwitchButton(self)
        self.connect_startup.setChecked(self.connect_startup)
        layout.addWidget(self.connect_startup)
        
        # Add stretch to push buttons to bottom
        layout.addStretch()
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_button = PushButton('保存', self)
        save_button.setIcon(FluentIcon.SAVE)
        save_button.clicked.connect(self.accept)
        
        cancel_button = PushButton('取消', self)
        cancel_button.setIcon(FluentIcon.CLOSE)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def get_settings(self):
        return {
            'server': self.server_input.text() or self.server_input.placeholderText(),
            'dns': self.dns_input.text() or self.dns_input.placeholderText(),
            'proxy': self.proxy_switch.isChecked(),
            'connect_startup': self.connect_startup.isChecked()
        }

    def set_settings(self, server, dns, proxy, connect_startup=False):
        """Set dialog values from main window values"""
        self.server_input.setText(server)
        self.dns_input.setText(dns)
        self.proxy_switch.setChecked(proxy)
        self.connect_startup.setChecked(connect_startup)

    def accept(self):
        """Save settings before closing"""
        settings = self.get_settings()
        save_config(settings)
        set_launch_at_login(self.startup_switch.isChecked())
        super().accept()
