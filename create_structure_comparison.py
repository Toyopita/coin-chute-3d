#!/usr/bin/env python3
"""
箱構造の比較図生成スクリプト
現在の設計 vs 修正後の設計
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 日本語フォント設定
plt.rcParams['font.family'] = 'Hiragino Sans'

# 図面作成
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('箱構造の比較 - 現在の設計 vs 修正後の設計', fontsize=20, fontweight='bold')

# パラメータ
depth = 315
height_per_part = 60
total_height = 120
slope_angle = 20
slope_drop = depth * np.tan(np.radians(slope_angle))  # 114.7mm
machine_insert_depth = 100

# === 左図：現在の設計（問題あり） ===
ax1.set_title('【現在の設計】問題あり\n（内側だけ傾斜、外側の箱は平行）',
              fontsize=14, color='red', pad=20)
ax1.set_aspect('equal')
ax1.set_xlim(-20, depth + 80)
ax1.set_ylim(-50, 200)
ax1.grid(True, alpha=0.3)

# コイン計算機（差し込み部分）
machine1 = patches.Rectangle((0, 0), machine_insert_depth, 150,
                            linewidth=2, edgecolor='gray', facecolor='lightgray', alpha=0.3)
ax1.add_patch(machine1)
ax1.text(machine_insert_depth/2, 160, 'コイン計算機\n（差し込み100mm）', ha='center', fontsize=10)

# 外側の箱（平行）- 問題点を強調
outer_box = patches.Rectangle((0, 0), depth, total_height,
                              linewidth=3, edgecolor='blue', facecolor='none')
ax1.add_patch(outer_box)

# 内側の傾斜底面
inner_slope_x = [10, depth-10, depth-10, 10]
inner_slope_y = [total_height - slope_drop, total_height, 10, 10 + slope_drop]
inner_slope = patches.Polygon(list(zip(inner_slope_x, inner_slope_y)),
                             linewidth=2, edgecolor='orange', facecolor='yellow', alpha=0.5)
ax1.add_patch(inner_slope)
ax1.text(depth/2, 70, '内側の傾斜', ha='center', fontsize=10, color='orange')

# 外壁の高さを示す
ax1.plot([0, 0], [0, total_height], 'b-', linewidth=4)
ax1.plot([depth, depth], [0, total_height], 'b-', linewidth=4)
ax1.text(-15, total_height/2, f'{total_height}mm', rotation=90, va='center',
         fontsize=11, color='blue', fontweight='bold')
ax1.text(depth + 15, total_height/2, f'{total_height}mm', rotation=90, va='center',
         fontsize=11, color='blue', fontweight='bold')

# 問題点：垂れ下がる様子
arrow_props = dict(arrowstyle='->', lw=3, color='red')
ax1.annotate('', xy=(depth/2+50, -30), xytext=(depth/2+50, 60),
            arrowprops=arrow_props)
ax1.text(depth/2+50, -40, '垂れ下がる！\n（支えがない）', ha='center', fontsize=12,
         color='red', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='pink', alpha=0.7))

# 機械の境界線
ax1.plot([machine_insert_depth, machine_insert_depth], [-10, 170], 'r--', linewidth=2)
ax1.text(machine_insert_depth + 5, 170, '機械の端', fontsize=9, color='red')

# 支えがない部分を示す
no_support_length = depth - machine_insert_depth
ax1.annotate('', xy=(depth, -15), xytext=(machine_insert_depth, -15),
            arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
ax1.text((machine_insert_depth + depth)/2, -22, f'支えなし: {no_support_length}mm',
         ha='center', fontsize=10, color='red', fontweight='bold')

ax1.set_xlabel('奥行き (mm)', fontsize=12)
ax1.set_ylabel('高さ (mm)', fontsize=12)

# === 右図：修正後の設計（OK） ===
ax2.set_title('【修正後の設計】OK\n（箱全体が傾斜、角度を維持）',
              fontsize=14, color='green', pad=20)
ax2.set_aspect('equal')
ax2.set_xlim(-20, depth + 80)
ax2.set_ylim(-50, 200)
ax2.grid(True, alpha=0.3)

# コイン計算機
machine2 = patches.Rectangle((0, 0), machine_insert_depth, 150,
                            linewidth=2, edgecolor='gray', facecolor='lightgray', alpha=0.3)
ax2.add_patch(machine2)
ax2.text(machine_insert_depth/2, 160, 'コイン計算機\n（差し込み100mm）', ha='center', fontsize=10)

# 外側の箱（傾斜） - 台形
back_height = total_height + slope_drop  # 奥側: 120 + 114.7 = 234.7mm
front_height = total_height  # 手前側: 120mm

outer_box_vertices = [
    [0, 0],  # 手前下
    [depth, 0],  # 奥下
    [depth, back_height],  # 奥上
    [0, front_height],  # 手前上
]
outer_box2 = patches.Polygon(outer_box_vertices,
                            linewidth=3, edgecolor='green', facecolor='lightgreen', alpha=0.3)
ax2.add_patch(outer_box2)

# 内側の傾斜底面
inner_vertices = [
    [10, height_per_part],  # 手前下
    [depth-10, height_per_part + slope_drop],  # 奥下
    [depth-10, back_height - 10],  # 奥上
    [10, front_height - 10],  # 手前上
]
inner_box = patches.Polygon(inner_vertices,
                           linewidth=2, edgecolor='darkgreen', facecolor='lightgreen', alpha=0.5)
ax2.add_patch(inner_box)

# 外壁の高さを示す
ax2.plot([0, 0], [0, front_height], 'g-', linewidth=4)
ax2.plot([depth, depth], [0, back_height], 'g-', linewidth=4)
ax2.text(-15, front_height/2, f'{front_height:.0f}mm\n（手前側）', rotation=90, va='center',
         fontsize=11, color='green', fontweight='bold')
ax2.text(depth + 15, back_height/2, f'{back_height:.0f}mm\n（奥側）', rotation=90, va='center',
         fontsize=11, color='green', fontweight='bold')

# 高低差を示す
ax2.annotate('', xy=(depth + 35, back_height), xytext=(depth + 35, front_height),
            arrowprops=dict(arrowstyle='<->', lw=2, color='green'))
ax2.text(depth + 55, (back_height + front_height)/2,
         f'{slope_drop:.1f}mm\n高低差', rotation=90, va='center',
         fontsize=10, color='green', fontweight='bold')

# OK：傾斜が維持される
ax2.text(depth/2+50, -40, '傾斜を維持！\n（自立する）', ha='center', fontsize=12,
         color='green', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

# 機械の境界線
ax2.plot([machine_insert_depth, machine_insert_depth], [-10, 170], 'r--', linewidth=2)
ax2.text(machine_insert_depth + 5, 170, '機械の端', fontsize=9, color='red')

# 傾斜角度を示す
angle_arc = patches.Arc((0, front_height), 80, 80, angle=0, theta1=0,
                       theta2=np.degrees(np.arctan(slope_drop/depth)),
                       linewidth=2, color='green')
ax2.add_patch(angle_arc)
ax2.text(50, front_height + 30, f'{slope_angle}°', fontsize=11, color='green', fontweight='bold')

ax2.set_xlabel('奥行き (mm)', fontsize=12)
ax2.set_ylabel('高さ (mm)', fontsize=12)

# 凡例
fig.text(0.25, 0.02, '× 問題点: 内側だけ傾斜 → 箱が垂れ下がる',
         ha='center', fontsize=13, color='red', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='pink', alpha=0.5))
fig.text(0.75, 0.02, '○ 解決策: 箱全体が傾斜 → 自立する',
         ha='center', fontsize=13, color='green', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.tight_layout()
plt.savefig('/Users/minamitakeshi/3d_models/coin_chute/structure_comparison.png',
            dpi=150, bbox_inches='tight')
print('✅ 構造比較図を保存しました: structure_comparison.png')
plt.close()
