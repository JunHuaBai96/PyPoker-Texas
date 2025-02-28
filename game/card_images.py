from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
import os
from treys import Card

class CardImages:
    CARD_WIDTH = 71
    CARD_HEIGHT = 96
    
    def __init__(self):
        self.card_back = self._create_card_back()
        self.card_images = {}
        self._initialize_card_images()
        
    def _create_card_back(self) -> QPixmap:
        """创建一个简单的卡牌背面图像"""
        pixmap = QPixmap(self.CARD_WIDTH, self.CARD_HEIGHT)
        pixmap.fill(Qt.GlobalColor.blue)
        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawRect(2, 2, self.CARD_WIDTH-4, self.CARD_HEIGHT-4)
        painter.end()
        return pixmap
        
    def _initialize_card_images(self):
        """初始化所有扑克牌图像"""
        suits = ['s', 'h', 'd', 'c']  # 黑桃、红心、方块、梅花
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        colors = {
            's': Qt.GlobalColor.black,  # 黑桃
            'h': Qt.GlobalColor.red,    # 红心
            'd': Qt.GlobalColor.red,    # 方块
            'c': Qt.GlobalColor.black   # 梅花
        }
        suit_symbols = {
            's': '♠',  # 黑桃
            'h': '♥',  # 红心
            'd': '♦',  # 方块
            'c': '♣'   # 梅花
        }
        
        for suit in suits:
            for rank in ranks:
                card_str = rank + suit
                card_int = Card.new(card_str)
                
                # 创建卡牌图像
                pixmap = QPixmap(self.CARD_WIDTH, self.CARD_HEIGHT)
                pixmap.fill(Qt.GlobalColor.white)
                
                painter = QPainter(pixmap)
                painter.setPen(colors[suit])
                
                # 绘制边框
                painter.drawRect(0, 0, self.CARD_WIDTH-1, self.CARD_HEIGHT-1)
                
                # 绘制花色和点数
                font = painter.font()
                font.setPointSize(16)
                painter.setFont(font)
                
                # 左上角
                painter.drawText(5, 20, rank)
                font.setPointSize(20)
                painter.setFont(font)
                painter.drawText(5, 45, suit_symbols[suit])
                
                # 中央
                font.setPointSize(32)
                painter.setFont(font)
                painter.drawText(self.CARD_WIDTH//2 - 15, 
                               self.CARD_HEIGHT//2 + 15, 
                               suit_symbols[suit])
                
                # 右下角（倒置）
                painter.translate(self.CARD_WIDTH, self.CARD_HEIGHT)
                painter.rotate(180)
                font.setPointSize(16)
                painter.setFont(font)
                painter.drawText(5, 20, rank)
                font.setPointSize(20)
                painter.setFont(font)
                painter.drawText(5, 45, suit_symbols[suit])
                
                painter.end()
                
                self.card_images[card_int] = pixmap
                
    def get_card_image(self, card_int) -> QPixmap:
        """获取指定卡牌的图像"""
        return self.card_images.get(card_int, self.card_back)
        
    def get_card_back(self) -> QPixmap:
        """获取卡牌背面的图像"""
        return self.card_back 