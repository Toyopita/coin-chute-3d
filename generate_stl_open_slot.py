#!/usr/bin/env python3
"""
コイン計算機用シュート STL生成スクリプト（開口部版）
2分割設計: 上部パーツ + 下部パーツ（前端開口部）

要件:
- 外見：240×315×120mmの普通の箱（直方体）
- 内側の底面だけ20度傾斜
- 前端から約40mmの位置で下に開口部（スロット）
- 円形の穴ではなく、シンプルに開いている
"""

import numpy as np
from stl import mesh
import math

# パラメータ (mm)
TOP_WIDTH = 240
TOP_DEPTH = 315
WALL_THICKNESS = 2
HEIGHT_PER_PART = 60  # 各パーツの基本高さ
SLOPE_ANGLE = 20  # 傾斜角度（度）
SLOT_POSITION = 40  # 前端からスロットまでの距離
SLOT_WIDTH = 100  # スロットの幅

# 傾斜による高低差
slope_drop = TOP_DEPTH * math.tan(math.radians(SLOPE_ANGLE))

def create_upper_part_open():
    """
    上部パーツを生成（開口部版）
    外側：240mm × 315mm × 60mm の直方体
    内側：底面が20度傾斜
    """
    vertices = []
    faces = []

    # 上部 - 長方形の頂点（外側は平行）
    top_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART],  # 手前左
        [TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART],   # 手前右
        [TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART],   # 奥右
        [-TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART],  # 奥左
    ]

    # 内側の上部（外側より少し低い）
    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART - WALL_THICKNESS],
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART - WALL_THICKNESS],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART - WALL_THICKNESS],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART - WALL_THICKNESS],
    ]

    # 下部 - 外側は平行（直方体）
    bottom_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, 0],  # 手前左
        [TOP_WIDTH/2, -TOP_DEPTH/2, 0],   # 手前右
        [TOP_WIDTH/2, TOP_DEPTH/2, 0],   # 奥右
        [-TOP_WIDTH/2, TOP_DEPTH/2, 0],  # 奥左
    ]

    # 内側の底面は傾斜（手前が低く、奥が高い）
    bottom_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), WALL_THICKNESS],  # 手前左
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), WALL_THICKNESS],   # 手前右
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), WALL_THICKNESS + slope_drop],   # 奥右
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), WALL_THICKNESS + slope_drop],  # 奥左
    ]

    # 外側の4つの壁
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([
            top_outer[i],
            top_outer[next_i],
            bottom_outer[next_i],
            bottom_outer[i]
        ])
        faces.append([v_idx, v_idx+1, v_idx+2])
        faces.append([v_idx, v_idx+2, v_idx+3])

    # 内側の4つの壁
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([
            top_inner[i],
            top_inner[next_i],
            bottom_inner[next_i],
            bottom_inner[i]
        ])
        faces.append([v_idx, v_idx+2, v_idx+1])
        faces.append([v_idx, v_idx+3, v_idx+2])

    # 上部の蓋（長方形のリング）
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([top_outer[i], top_outer[next_i], top_inner[next_i], top_inner[i]])
        faces.append([v_idx, v_idx+1, v_idx+2])
        faces.append([v_idx, v_idx+2, v_idx+3])

    return np.array(vertices), np.array(faces)

def create_lower_part_open():
    """
    下部パーツを生成（開口部版）
    外側：240mm × 315mm × 60mm の直方体
    内側：底面が傾斜し、前端から約40mmの位置で下に開口部（スロット）
    """
    vertices = []
    faces = []

    # 上部 - 外側は平行（直方体）
    top_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, 0],  # 手前左
        [TOP_WIDTH/2, -TOP_DEPTH/2, 0],   # 手前右
        [TOP_WIDTH/2, TOP_DEPTH/2, 0],   # 奥右
        [-TOP_WIDTH/2, TOP_DEPTH/2, 0],  # 奥左
    ]

    # 内側の上部は傾斜
    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS],  # 手前左
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS],   # 手前右
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop],   # 奥右
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop],  # 奥左
    ]

    # スロット位置のy座標
    slot_y = -TOP_DEPTH/2 + SLOT_POSITION
    # スロット位置での傾斜の高さ
    slot_z = (slot_y + TOP_DEPTH/2) / TOP_DEPTH * slope_drop - WALL_THICKNESS

    # スロットの端点（開口部）
    slot_left = [-(SLOT_WIDTH/2), slot_y, slot_z]
    slot_right = [(SLOT_WIDTH/2), slot_y, slot_z]

    # 外壁を底まで延長
    bottom_outer_base = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, -HEIGHT_PER_PART],
        [TOP_WIDTH/2, -TOP_DEPTH/2, -HEIGHT_PER_PART],
        [TOP_WIDTH/2, TOP_DEPTH/2, -HEIGHT_PER_PART],
        [-TOP_WIDTH/2, TOP_DEPTH/2, -HEIGHT_PER_PART],
    ]

    # 外側の4つの壁
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([
            top_outer[i],
            top_outer[next_i],
            bottom_outer_base[next_i],
            bottom_outer_base[i]
        ])
        faces.append([v_idx, v_idx+1, v_idx+2])
        faces.append([v_idx, v_idx+2, v_idx+3])

    # === 内側の傾斜面（スロットまで） ===
    # 手前側：スロットまで
    # 左壁（手前からスロットまで）
    v_idx = len(vertices)
    vertices.extend([
        top_inner[0],  # 手前左上
        [-(TOP_WIDTH/2 - WALL_THICKNESS), slot_y, slot_z],  # スロット位置左上
        slot_left,  # スロット開口部左
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS]  # 手前左底
    ])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # 右壁（手前からスロットまで）
    v_idx = len(vertices)
    vertices.extend([
        top_inner[1],  # 手前右上
        [(TOP_WIDTH/2 - WALL_THICKNESS), slot_y, slot_z],  # スロット位置右上
        slot_right,  # スロット開口部右
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS]  # 手前右底
    ])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 底面（手前からスロットまで、中央に開口部）
    # 左側の底面
    v_idx = len(vertices)
    vertices.extend([
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS],  # 手前左
        slot_left,  # スロット左
        [-(SLOT_WIDTH/2), slot_y, slot_z - WALL_THICKNESS],  # スロット左下
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS * 2]  # 手前左下
    ])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 右側の底面
    v_idx = len(vertices)
    vertices.extend([
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS],  # 手前右
        slot_right,  # スロット右
        [(SLOT_WIDTH/2), slot_y, slot_z - WALL_THICKNESS],  # スロット右下
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS * 2]  # 手前右下
    ])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # === スロットから奥側の面 ===
    # 左壁（スロットから奥まで）
    v_idx = len(vertices)
    vertices.extend([
        [-(TOP_WIDTH/2 - WALL_THICKNESS), slot_y, slot_z],  # スロット位置左上
        top_inner[3],  # 奥左上
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop - WALL_THICKNESS],  # 奥左下
        slot_left  # スロット開口部左
    ])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # 右壁（スロットから奥まで）
    v_idx = len(vertices)
    vertices.extend([
        [(TOP_WIDTH/2 - WALL_THICKNESS), slot_y, slot_z],  # スロット位置右上
        top_inner[2],  # 奥右上
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop - WALL_THICKNESS],  # 奥右下
        slot_right  # スロット開口部右
    ])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 奥の壁
    v_idx = len(vertices)
    vertices.extend([
        top_inner[2],  # 奥右上
        top_inner[3],  # 奥左上
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop - WALL_THICKNESS],  # 奥左下
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop - WALL_THICKNESS]  # 奥右下
    ])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # 奥側の底面（スロットから奥まで）
    # 左側
    v_idx = len(vertices)
    vertices.extend([
        slot_left,
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop - WALL_THICKNESS],
        [-(SLOT_WIDTH/2), slot_y, slot_z - WALL_THICKNESS]
    ])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 右側
    v_idx = len(vertices)
    vertices.extend([
        slot_right,
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), -WALL_THICKNESS + slope_drop - WALL_THICKNESS],
        [(SLOT_WIDTH/2), slot_y, slot_z - WALL_THICKNESS]
    ])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    return np.array(vertices), np.array(faces)

def save_stl(vertices, faces, filename):
    """STLファイルに保存"""
    coin_chute = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, face in enumerate(faces):
        for j in range(3):
            coin_chute.vectors[i][j] = vertices[face[j]]

    coin_chute.save(filename)
    print(f"✅ {filename} を生成しました")

if __name__ == "__main__":
    print("コインシュートSTLファイル生成中（開口部版）...")
    print(f"設計: 外見は240×315×{HEIGHT_PER_PART * 2}mmの直方体")
    print(f"内側の底面のみ20度傾斜（高低差: {slope_drop:.1f}mm）")
    print(f"前端から約{SLOT_POSITION}mmの位置に幅{SLOT_WIDTH}mmの開口部（スロット）")

    # 上部パーツ生成
    print("\n上部パーツ生成中（開口部版）...")
    upper_vertices, upper_faces = create_upper_part_open()
    save_stl(upper_vertices, upper_faces, "coin_chute_upper_open.stl")

    # 下部パーツ生成
    print(f"下部パーツ生成中（開口部版・スロット付き）...")
    lower_vertices, lower_faces = create_lower_part_open()
    save_stl(lower_vertices, lower_faces, "coin_chute_lower_open.stl")

    print("\n✅ 完了！以下のファイルが生成されました:")
    print("- coin_chute_upper_open.stl (上部パーツ)")
    print("- coin_chute_lower_open.stl (下部パーツ: 開口部付き)")
    print(f"\n外見: 240×315×{HEIGHT_PER_PART * 2}mmの直方体")
    print(f"内側傾斜角度: {SLOPE_ANGLE}度")
    print(f"開口部: 前端から{SLOT_POSITION}mm、幅{SLOT_WIDTH}mm")
    print("円形の穴ではなく、シンプルに下に開いたスロット")
