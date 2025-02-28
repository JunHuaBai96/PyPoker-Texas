from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSpinBox, QMessageBox,
                             QInputDialog, QLineEdit, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPalette
from typing import List, Optional
import math
from .poker_game import PokerGame, Player
from .card_images import CardImages

class PokerTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPoker-Texas")
        self.setMinimumSize(1200, 800)
        
        # 初始化卡牌图像
        self.card_images = CardImages()
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout(self.central_widget)
        
        # 游戏设置部件
        self.setup_widget = QWidget()
        self.setup_layout = QHBoxLayout(self.setup_widget)
        
        # 玩家数量选择
        self.player_count_label = QLabel("玩家数量:")
        self.player_count_spin = QSpinBox()
        self.player_count_spin.setRange(2, 10)
        self.player_count_spin.setValue(6)
        
        # 盲注设置
        self.blind_label = QLabel("小盲注:")
        self.blind_spin = QSpinBox()
        self.blind_spin.setRange(1, 1000)
        self.blind_spin.setValue(10)
        
        # 开始游戏按钮
        self.start_button = QPushButton("开始游戏")
        self.start_button.clicked.connect(self.start_game)
        
        # 添加设置部件
        self.setup_layout.addWidget(self.player_count_label)
        self.setup_layout.addWidget(self.player_count_spin)
        self.setup_layout.addWidget(self.blind_label)
        self.setup_layout.addWidget(self.blind_spin)
        self.setup_layout.addWidget(self.start_button)
        
        # 游戏信息显示
        self.info_widget = QWidget()
        self.info_layout = QHBoxLayout(self.info_widget)
        self.pot_label = QLabel("底池: 0")
        self.current_bet_label = QLabel("当前下注: 0")
        self.info_layout.addWidget(self.pot_label)
        self.info_layout.addWidget(self.current_bet_label)
        
        # 公共牌区域
        self.community_cards_widget = QWidget()
        self.community_cards_layout = QHBoxLayout(self.community_cards_widget)
        self.community_cards_labels: List[QLabel] = []
        for _ in range(5):
            label = QLabel()
            label.setFixedSize(71, 96)
            self.community_cards_labels.append(label)
            self.community_cards_layout.addWidget(label)
            
        # 玩家操作区域
        self.action_widget = QWidget()
        self.action_layout = QHBoxLayout(self.action_widget)
        
        self.check_button = QPushButton("让牌")
        self.call_button = QPushButton("跟注")
        self.raise_button = QPushButton("加注")
        self.fold_button = QPushButton("弃牌")
        
        self.check_button.clicked.connect(lambda: self.player_action('check'))
        self.call_button.clicked.connect(lambda: self.player_action('call'))
        self.raise_button.clicked.connect(lambda: self.player_action('raise'))
        self.fold_button.clicked.connect(lambda: self.player_action('fold'))
        
        self.action_layout.addWidget(self.check_button)
        self.action_layout.addWidget(self.call_button)
        self.action_layout.addWidget(self.raise_button)
        self.action_layout.addWidget(self.fold_button)
        
        # 添加所有部件到主布局
        self.main_layout.addWidget(self.setup_widget, 0, 0, 1, 3)
        self.main_layout.addWidget(self.info_widget, 1, 0, 1, 3)
        self.main_layout.addWidget(self.community_cards_widget, 2, 1)
        self.main_layout.addWidget(self.action_widget, 4, 0, 1, 3)
        
        # 玩家区域容器
        self.players_container = QWidget()
        self.players_container.setMinimumSize(800, 600)
        self.main_layout.addWidget(self.players_container, 3, 0, 1, 3)
        
        # 初始化游戏相关变量
        self.game: Optional[PokerGame] = None
        self.player_widgets: List[dict] = []
        
    def start_game(self):
        num_players = self.player_count_spin.value()
        small_blind = self.blind_spin.value()
        
        # 获取玩家名称
        player_names = []
        for i in range(num_players):
            name, ok = QInputDialog.getText(self, f"玩家 {i+1}", "输入玩家名称:",
                                         QLineEdit.EchoMode.Normal, f"玩家 {i+1}")
            if ok and name:
                player_names.append(name)
            else:
                return
                
        # 初始化游戏
        self.game = PokerGame(num_players, small_blind)
        self.game.initialize_game(player_names, 1000)  # 初始筹码1000
        
        # 禁用设置控件
        self.setup_widget.setEnabled(False)
        
        # 创建玩家区域
        self.create_player_widgets()
        
        # 开始第一手牌
        self.start_new_hand()
        
    def create_player_widgets(self):
        # 清除现有的玩家部件
        for widget_info in self.player_widgets:
            widget_info['widget'].setParent(None)
            widget_info['widget'].deleteLater()
        self.player_widgets.clear()
        
        if not self.game:
            return
            
        # 计算玩家位置
        center = QPoint(self.players_container.width() // 2,
                       self.players_container.height() // 2)
        radius = min(center.x(), center.y()) - 100
        num_players = len(self.game.players)
        
        # 创建新的玩家部件
        for i, player in enumerate(self.game.players):
            # 计算玩家位置
            angle = (2 * math.pi * i / num_players) - math.pi / 2
            x = center.x() + radius * math.cos(angle) - 100
            y = center.y() + radius * math.sin(angle) - 50
            
            player_widget = QWidget(self.players_container)
            player_widget.setFixedSize(200, 150)
            player_widget.move(int(x), int(y))
            
            player_layout = QVBoxLayout(player_widget)
            
            # 玩家信息
            info_widget = QWidget()
            info_layout = QHBoxLayout(info_widget)
            name_label = QLabel(player.name)
            chips_label = QLabel(f"筹码: {player.chips}")
            bet_label = QLabel(f"下注: {player.current_bet}")
            
            # 当前玩家标记
            if i == self.game.current_player_idx:
                name_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")
                
            info_layout.addWidget(name_label)
            info_layout.addWidget(chips_label)
            info_layout.addWidget(bet_label)
            
            # 玩家手牌
            cards_widget = QWidget()
            cards_layout = QHBoxLayout(cards_widget)
            
            card_labels = []
            for _ in range(2):
                label = QLabel()
                label.setFixedSize(71, 96)
                card_labels.append(label)
                cards_layout.addWidget(label)
                
            player_layout.addWidget(info_widget)
            player_layout.addWidget(cards_widget)
            
            self.player_widgets.append({
                'widget': player_widget,
                'name_label': name_label,
                'chips_label': chips_label,
                'bet_label': bet_label,
                'card_labels': card_labels
            })
            player_widget.show()
            
    def start_new_hand(self):
        if self.game:
            self.game.start_new_hand()
            self.update_display()
            
    def update_display(self):
        if not self.game:
            return
            
        # 更新底池和当前下注
        self.pot_label.setText(f"底池: {self.game.pot}")
        self.current_bet_label.setText(f"当前下注: {self.game.current_bet}")
            
        # 更新公共牌显示
        for i, label in enumerate(self.community_cards_labels):
            if i < len(self.game.community_cards):
                card = self.game.community_cards[i]
                label.setPixmap(self.card_images.get_card_image(card))
            else:
                label.clear()
                
        # 更新玩家信息
        current_player_idx = self.game.current_player_idx
        for i, (widget_info, player) in enumerate(zip(self.player_widgets, self.game.players)):
            # 更新筹码信息和下注
            widget_info['chips_label'].setText(f"筹码: {player.chips}")
            widget_info['bet_label'].setText(f"下注: {player.current_bet}")
            
            # 更新当前玩家标记
            if i == current_player_idx:
                widget_info['name_label'].setStyleSheet("QLabel { color: red; font-weight: bold; }")
            else:
                widget_info['name_label'].setStyleSheet("")
            
            # 更新玩家手牌
            for j, label in enumerate(widget_info['card_labels']):
                if i == current_player_idx and j < len(player.cards):
                    # 当前玩家显示真实牌面
                    label.setPixmap(self.card_images.get_card_image(player.cards[j]))
                else:
                    # 其他玩家显示牌背
                    label.setPixmap(self.card_images.get_card_back())
                    
        # 更新按钮状态
        current_player = self.game.players[self.game.current_player_idx]
        valid_actions = self.game.get_valid_actions(current_player)
        
        self.check_button.setEnabled(valid_actions['check'])
        self.call_button.setEnabled(valid_actions['call'])
        self.raise_button.setEnabled(valid_actions['raise'])
        self.fold_button.setEnabled(valid_actions['fold'])
        
    def player_action(self, action: str):
        if not self.game:
            return
            
        amount = None
        if action == 'raise':
            amount, ok = QInputDialog.getInt(self, "加注", "输入加注金额:",
                                          self.game.current_bet + self.game.big_blind,
                                          self.game.current_bet + 1,
                                          self.game.players[self.game.current_player_idx].chips)
            if not ok:
                return
                
        if self.game.process_action(action, amount):
            self.update_display()
            
            if self.game.is_round_complete():
                if self.game.round_state == 'river':
                    self.show_winner()
                else:
                    self.game.deal_next_street()
                    self.update_display()
                    
    def show_winner(self):
        if not self.game:
            return
            
        results = self.game.evaluate_hands()
        if results:
            winner = results[0][0]
            QMessageBox.information(self, "游戏结束",
                                 f"{winner.name} 赢得了 {self.game.pot} 筹码!")
            
        # 开始新的一手牌
        QTimer.singleShot(2000, self.start_new_hand) 