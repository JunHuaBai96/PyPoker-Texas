# PyPoker-Texas 

一个使用Python和PyQt6开发的德州扑克游戏，支持2-10名玩家对战。

## 功能特点

- 可视化游戏界面
- 支持2-10名玩家
- 可自定义盲注大小
- 真实的德州扑克规则
- 直观的操作界面

## 安装说明

1. 确保你的系统已安装Python 3.8或更高版本
2. 克隆此仓库：
```bash
git clone https://github.com/JunHuaBai96/PyPoker-Texas.git
cd PyPoker-Texas
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行游戏

```bash
python main.py
```

## 游戏规则

德州扑克是一种流行的扑克游戏变体：

1. 每位玩家先获得2张私有牌（底牌）
2. 经过多轮下注后，桌面上会出现5张公共牌
3. 玩家使用自己的2张私有牌和5张公共牌中的任意牌组成最好的5张牌组合
4. 牌型从高到低依次为：皇家同花顺、同花顺、四条、葫芦、同花、顺子、三条、两对、一对、高牌

## 操作说明

1. 启动游戏后，可以设置玩家数量（2-10名）和盲注大小
2. 游戏过程中可以进行：
   - Check（让牌）
   - Call（跟注）
   - Raise（加注）
   - Fold（弃牌）

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

## 许可证

本项目采用 MIT 许可证 