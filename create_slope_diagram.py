#!/usr/bin/env python3
"""
傾斜説明図生成スクリプト
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np

# 図面作成
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('Coin Chute - Slope Comparison', fontsize=20, fontweight='bold')

# パラメータ
depth = 315
height_upper = 60
height_lower = 60
hole_position_current = 80  # 前端から
hole_position_new = 40      # 前端から（推奨）
slope_angle = 10  # 度

# === 左図：現在の設計（水平） ===
ax1.set_title('CURRENT DESIGN (Horizontal Bottom) - NG', fontsize=16, color='red', pad=20)
ax1.set_aspect('equal')
ax1.set_xlim(-20, depth + 50)
ax1.set_ylim(-30, 180)
ax1.grid(True, alpha=0.3)

# コイン計算機
machine1 = patches.Rectangle((0, 120), 100, 40,
                            linewidth=2, edgecolor='gray', facecolor='lightgray', alpha=0.5)
ax1.add_patch(machine1)
ax1.text(50, 140, 'Coin Machine', ha='center', fontsize=11, fontweight='bold')

# 上部パーツ（水平な底）
upper1 = patches.Rectangle((0, height_lower), 100, height_upper,
                          linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax1.add_patch(upper1)
ax1.text(50, height_lower + height_upper/2, 'Insert Part', ha='center', fontsize=10, color='blue')

upper1_outside = patches.Rectangle((100, height_lower), depth-100, height_upper,
                                   linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.5)
ax1.add_patch(upper1_outside)

# 底面（水平）- 強調
ax1.plot([0, depth], [height_lower, height_lower], 'r-', linewidth=4, label='Horizontal Bottom')
ax1.text(depth/2, height_lower - 10, 'FLAT (Horizontal)', ha='center', fontsize=12,
         color='red', fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# コインが滞留する様子
for i in range(5):
    x = 120 + i * 30
    coin = Circle((x, height_lower + 5), 5, color='orange', alpha=0.8)
    ax1.add_patch(coin)
ax1.text(180, height_lower + 20, 'Coins stuck!', fontsize=11, color='red', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))

# 下部パーツ（穴）
hole_x1 = hole_position_current + 50
lower1_vertices = [
    [hole_x1 - 50, height_lower],
    [hole_x1 + 50, height_lower],
    [hole_x1 + 50, 0],
    [hole_x1 - 50, 0],
]
lower1 = patches.Polygon(lower1_vertices, linewidth=2,
                        edgecolor='green', facecolor='lightgreen', alpha=0.4)
ax1.add_patch(lower1)

# 穴の位置
ax1.plot([hole_x1, hole_x1], [0, -20], 'g-', linewidth=3)
ax1.text(hole_x1, -25, f'Hole\n({hole_position_current}mm from front)', ha='center', fontsize=10, color='green')

# 寸法
ax1.annotate('', xy=(depth, 150), xytext=(0, 150),
            arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax1.text(depth/2, 160, f'{depth}mm', ha='center', fontsize=11, fontweight='bold')

ax1.annotate('', xy=(depth + 20, height_lower + height_upper), xytext=(depth + 20, height_lower),
            arrowprops=dict(arrowstyle='<->', lw=2, color='blue'))
ax1.text(depth + 35, height_lower + height_upper/2, f'{height_upper}mm', rotation=90,
         va='center', fontsize=10, color='blue')

# 機械の境界
ax1.plot([100, 100], [0, 165], 'r--', linewidth=2, alpha=0.7)
ax1.text(105, 165, 'Machine Edge', fontsize=10, color='red')

ax1.set_xlabel('Depth Direction (mm)', fontsize=12)
ax1.set_ylabel('Height (mm)', fontsize=12)

# === 右図：修正後の設計（傾斜） ===
ax2.set_title('NEW DESIGN (Sloped Bottom) - RECOMMENDED', fontsize=16, color='green', pad=20)
ax2.set_aspect('equal')
ax2.set_xlim(-20, depth + 50)
ax2.set_ylim(-30, 180)
ax2.grid(True, alpha=0.3)

# コイン計算機
machine2 = patches.Rectangle((0, 120), 100, 40,
                            linewidth=2, edgecolor='gray', facecolor='lightgray', alpha=0.5)
ax2.add_patch(machine2)
ax2.text(50, 140, 'Coin Machine', ha='center', fontsize=11, fontweight='bold')

# 傾斜計算
slope_drop = depth * np.tan(np.radians(slope_angle))
back_height = height_lower + slope_drop  # 奥側の高さ
front_height = height_lower  # 手前側の高さ

# 上部パーツ（傾斜した底）
# 差し込み部分
insert_vertices = [
    [0, back_height],  # 奥・下
    [0, back_height + height_upper],  # 奥・上
    [100, front_height + height_upper],  # 手前・上
    [100, front_height],  # 手前・下
]
upper2_insert = patches.Polygon(insert_vertices, linewidth=2,
                               edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax2.add_patch(upper2_insert)
ax2.text(50, (back_height + front_height)/2 + height_upper/2, 'Insert Part', ha='center',
         fontsize=10, color='blue')

# 外側部分
outside_vertices = [
    [100, front_height],  # 手前・下
    [100, front_height + height_upper],  # 手前・上
    [depth, height_lower + height_upper],  # 奥・上
    [depth, height_lower],  # 奥・下
]
upper2_outside = patches.Polygon(outside_vertices, linewidth=2,
                                edgecolor='blue', facecolor='lightblue', alpha=0.5)
ax2.add_patch(upper2_outside)

# 底面（傾斜）- 強調
ax2.plot([0, depth], [back_height, height_lower], 'g-', linewidth=4, label='Sloped Bottom')
ax2.text(depth/2, (back_height + height_lower)/2 - 15, f'SLOPED ({slope_angle} degrees)',
         ha='center', fontsize=12, color='green', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# 傾斜の高低差を示す
ax2.annotate('', xy=(depth + 10, back_height), xytext=(depth + 10, height_lower),
            arrowprops=dict(arrowstyle='<->', lw=2, color='green'))
ax2.text(depth + 30, (back_height + height_lower)/2, f'{slope_drop:.1f}mm\ndrop', rotation=90,
         va='center', fontsize=10, color='green', fontweight='bold')

# コインが滑り落ちる様子
coin_positions = [
    (250, back_height + 5),
    (200, (back_height + height_lower)/2 + 3),
    (150, height_lower + 5),
]
for i, (x, y) in enumerate(coin_positions):
    coin = Circle((x, y), 5, color='orange', alpha=0.8)
    ax2.add_patch(coin)
    if i < len(coin_positions) - 1:
        arrow = FancyArrowPatch((x-5, y), (coin_positions[i+1][0]+5, coin_positions[i+1][1]),
                               arrowstyle='->', mutation_scale=15, linewidth=2,
                               color='orange', alpha=0.6)
        ax2.add_patch(arrow)

ax2.text(200, height_lower + 35, 'Coins slide down!', fontsize=11, color='green', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

# 下部パーツ（穴 - より手前に）
hole_x2 = hole_position_new + 50
lower2_vertices = [
    [hole_x2 - 50, height_lower],
    [hole_x2 + 50, height_lower],
    [hole_x2 + 50, 0],
    [hole_x2 - 50, 0],
]
lower2 = patches.Polygon(lower2_vertices, linewidth=2,
                        edgecolor='green', facecolor='lightgreen', alpha=0.4)
ax2.add_patch(lower2)

# 穴の位置
ax2.plot([hole_x2, hole_x2], [0, -20], 'g-', linewidth=3)
ax2.text(hole_x2, -25, f'Hole\n({hole_position_new}mm from front)\nCLOSER!', ha='center',
         fontsize=10, color='green', fontweight='bold')

# 寸法
ax2.annotate('', xy=(depth, 150), xytext=(0, 150),
            arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax2.text(depth/2, 160, f'{depth}mm', ha='center', fontsize=11, fontweight='bold')

# 機械の境界
ax2.plot([100, 100], [0, 165], 'r--', linewidth=2, alpha=0.7)
ax2.text(105, 165, 'Machine Edge', fontsize=10, color='red')

ax2.set_xlabel('Depth Direction (mm)', fontsize=12)
ax2.set_ylabel('Height (mm)', fontsize=12)

# 凡例
ax1.text(depth/2, -10, 'X Problem: Coins get stuck', ha='center', fontsize=13,
         color='red', fontweight='bold', bbox=dict(boxstyle='round', facecolor='pink', alpha=0.7))
ax2.text(depth/2, -10, 'V Solution: Coins slide smoothly', ha='center', fontsize=13,
         color='green', fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig('/Users/minamitakeshi/3d_models/coin_chute/slope_diagram.png', dpi=150, bbox_inches='tight')
print('✅ Slope diagram saved: slope_diagram.png')
plt.close()
