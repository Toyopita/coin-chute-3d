#!/usr/bin/env python3
"""
コインシュート簡易図面生成スクリプト
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import numpy as np

# パラメータ
TOP_WIDTH = 240
TOP_DEPTH = 315
BOTTOM_DIAMETER = 100
HEIGHT_PER_PART = 60

# 図面作成
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
fig.suptitle('コインシュート 簡易図面', fontsize=20, fontweight='bold')

# === 上面図 (Top View) ===
ax1.set_title('上面図 (Top View)', fontsize=16, pad=20)
ax1.set_aspect('equal')
ax1.set_xlim(-50, TOP_WIDTH + 50)
ax1.set_ylim(-50, TOP_DEPTH + 50)
ax1.grid(True, alpha=0.3)

# 長方形（シュートの受け口）
rect = Rectangle((0, 0), TOP_WIDTH, TOP_DEPTH,
                 linewidth=3, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax1.add_patch(rect)

# 円形の穴（中央位置）- 現在の設計
circle_center_x = TOP_WIDTH / 2
circle_center_y = TOP_DEPTH / 2
circle_center = Circle((circle_center_x, circle_center_y), BOTTOM_DIAMETER/2,
                       linewidth=2, edgecolor='red', facecolor='pink', alpha=0.5, linestyle='--')
ax1.add_patch(circle_center)
ax1.text(circle_center_x, circle_center_y - BOTTOM_DIAMETER/2 - 20,
         '❌ 中央（NG）\n計算機内部に入る',
         ha='center', fontsize=12, color='red', fontweight='bold')

# 円形の穴（前端寄り位置）- 推奨位置
circle_front_x = TOP_WIDTH / 2
circle_front_y = BOTTOM_DIAMETER / 2 + 30  # 前端から30mm + 半径
circle_front = Circle((circle_front_x, circle_front_y), BOTTOM_DIAMETER/2,
                      linewidth=3, edgecolor='green', facecolor='lightgreen', alpha=0.5)
ax1.add_patch(circle_front)
ax1.text(circle_front_x, circle_front_y + BOTTOM_DIAMETER/2 + 20,
         '✅ 前端寄り（推奨）\n計算機外側に出る',
         ha='center', fontsize=12, color='green', fontweight='bold')

# 寸法線
# 幅
ax1.annotate('', xy=(TOP_WIDTH, -20), xytext=(0, -20),
            arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax1.text(TOP_WIDTH/2, -35, f'{TOP_WIDTH}mm', ha='center', fontsize=12, fontweight='bold')

# 奥行き
ax1.annotate('', xy=(TOP_WIDTH + 20, TOP_DEPTH), xytext=(TOP_WIDTH + 20, 0),
            arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax1.text(TOP_WIDTH + 35, TOP_DEPTH/2, f'{TOP_DEPTH}mm', rotation=90,
         va='center', fontsize=12, fontweight='bold')

# 穴の直径
ax1.annotate('', xy=(circle_front_x + BOTTOM_DIAMETER/2, circle_front_y),
            xytext=(circle_front_x - BOTTOM_DIAMETER/2, circle_front_y),
            arrowprops=dict(arrowstyle='<->', lw=2, color='green'))
ax1.text(circle_front_x, circle_front_y - 15, f'Φ{BOTTOM_DIAMETER}mm',
         ha='center', fontsize=11, color='green', fontweight='bold')

# 前端からの距離
ax1.annotate('', xy=(10, circle_front_y - BOTTOM_DIAMETER/2), xytext=(10, 0),
            arrowprops=dict(arrowstyle='<->', lw=2, color='green'))
distance_from_front = circle_front_y - BOTTOM_DIAMETER/2
ax1.text(25, distance_from_front/2, f'{distance_from_front:.0f}mm',
         rotation=90, va='center', fontsize=10, color='green', fontweight='bold')

# ラベル
ax1.text(TOP_WIDTH/2, TOP_DEPTH + 30, '← コイン計算機排出口の向き →',
         ha='center', fontsize=14, color='blue', fontweight='bold')
ax1.arrow(TOP_WIDTH/2, TOP_DEPTH + 15, 0, -10, head_width=15, head_length=5, fc='blue', ec='blue')

ax1.set_xlabel('幅方向 (mm)', fontsize=12)
ax1.set_ylabel('奥行き方向 (mm)', fontsize=12)

# === 側面図 (Side View) ===
ax2.set_title('側面図 (Side View) - 奥行き方向の断面', fontsize=16, pad=20)
ax2.set_aspect('equal')
ax2.set_xlim(-50, TOP_DEPTH + 150)
ax2.set_ylim(-20, 200)
ax2.grid(True, alpha=0.3)

# コイン計算機（概念図）
machine = Rectangle((0, 120), 150, 50,
                   linewidth=2, edgecolor='gray', facecolor='lightgray', alpha=0.5)
ax2.add_patch(machine)
ax2.text(75, 145, 'コイン計算機', ha='center', va='center', fontsize=12, fontweight='bold')

# シュート上部（ストレート部分）- 差し込み部分
chute_insert_depth = 100  # 差し込み深さ
upper_chute = Rectangle((0, 60), chute_insert_depth, HEIGHT_PER_PART,
                        linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax2.add_patch(upper_chute)
ax2.text(chute_insert_depth/2, 90, '差し込み部分', ha='center', fontsize=11, color='blue')

# シュート上部（外側部分）
upper_chute_outside = Rectangle((chute_insert_depth, 60), TOP_DEPTH - chute_insert_depth, HEIGHT_PER_PART,
                                linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.5)
ax2.add_patch(upper_chute_outside)
ax2.text((chute_insert_depth + TOP_DEPTH)/2, 90, 'ストレート部分', ha='center', fontsize=11, color='blue')

# シュート下部（集約部分）
# 前端から穴の位置までは垂直、そこから斜めに集約
hole_position = circle_front_y  # 前端からの距離
lower_vertices = [
    [hole_position - BOTTOM_DIAMETER/2, 60],  # 左上
    [hole_position + BOTTOM_DIAMETER/2, 60],  # 右上
    [hole_position + BOTTOM_DIAMETER/2, 0],   # 右下
    [hole_position - BOTTOM_DIAMETER/2, 0],   # 左下
]
lower_chute = patches.Polygon(lower_vertices, linewidth=2,
                              edgecolor='green', facecolor='lightgreen', alpha=0.5)
ax2.add_patch(lower_chute)
ax2.text(hole_position, 30, '集約部分', ha='center', fontsize=11, color='green', fontweight='bold')

# 穴の位置マーク
ax2.plot([hole_position, hole_position], [0, -10], 'g-', linewidth=3)
ax2.text(hole_position, -15, '穴の位置\n（前端寄り）', ha='center', fontsize=11,
         color='green', fontweight='bold')

# 寸法線
# 全体の奥行き
ax2.annotate('', xy=(TOP_DEPTH, 140), xytext=(0, 140),
            arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax2.text(TOP_DEPTH/2, 155, f'全長 {TOP_DEPTH}mm', ha='center', fontsize=12, fontweight='bold')

# 差し込み深さ
ax2.annotate('', xy=(chute_insert_depth, 55), xytext=(0, 55),
            arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
ax2.text(chute_insert_depth/2, 45, f'差し込み {chute_insert_depth}mm',
         ha='center', fontsize=11, color='red', fontweight='bold')

# 高さ
ax2.annotate('', xy=(TOP_DEPTH + 20, 120), xytext=(TOP_DEPTH + 20, 0),
            arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax2.text(TOP_DEPTH + 40, 60, f'{HEIGHT_PER_PART * 2}mm', rotation=90,
         va='center', fontsize=12, fontweight='bold')

# 各パーツの高さ
ax2.plot([TOP_DEPTH + 10, TOP_DEPTH + 15], [60, 60], 'b-', linewidth=2)
ax2.text(TOP_DEPTH + 50, 90, f'上部: {HEIGHT_PER_PART}mm', fontsize=10, color='blue')
ax2.text(TOP_DEPTH + 50, 30, f'下部: {HEIGHT_PER_PART}mm', fontsize=10, color='green')

# 計算機の境界線
ax2.plot([chute_insert_depth, chute_insert_depth], [0, 180], 'r--', linewidth=2, label='計算機の境界')
ax2.text(chute_insert_depth + 5, 175, '← 計算機外側', fontsize=11, color='red', fontweight='bold')
ax2.text(chute_insert_depth - 5, 175, '計算機内部 →', ha='right', fontsize=11, color='red', fontweight='bold')

ax2.set_xlabel('奥行き方向 (mm)', fontsize=12)
ax2.set_ylabel('高さ (mm)', fontsize=12)

plt.tight_layout()
plt.savefig('/Users/minamitakeshi/3d_models/coin_chute/diagram.png', dpi=150, bbox_inches='tight')
print('✅ 図面を保存しました: diagram.png')
plt.close()
