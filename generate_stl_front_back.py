#!/usr/bin/env python3
"""
コイン計算機用シュート STL生成スクリプト（前後分割版・ULTRATHINK設計）

最適設計：
- 前後2分割（プリントエリア制約を満たす）
- 後部215mm（入口側）+ 前部100mm（出口側）
- 前端開放式（壁が低くなる）
- はめ込み式接合（PETG用）

要件:
- 外見：240×315×120mmの直方体（分割前）
- 内側の底面だけ20度傾斜
- 前端が開放（コインが流れ落ちる）
"""

import numpy as np
from stl import mesh
import math

# パラメータ (mm)
TOP_WIDTH = 240
TOP_DEPTH = 315
WALL_THICKNESS = 2
TOTAL_HEIGHT = 120
SLOPE_ANGLE = 20  # 傾斜角度（度）

# 前後分割のパラメータ
BACK_DEPTH = 215  # 後部パーツの奥行き
FRONT_DEPTH = 100  # 前部パーツの奥行き
OPENING_START = 40  # 前端から開放が始まる位置

# 嵌合機構のパラメータ
CLEARANCE = 0.3  # クリアランス（PETG用）
JOINT_DEPTH = 10  # 接合部の深さ
JOINT_HEIGHT = 5  # 接合部の高さ

# 傾斜による高低差
slope_drop = TOP_DEPTH * math.tan(math.radians(SLOPE_ANGLE))

def create_back_part():
    """
    後部パーツを生成（入口側、215mm）
    普通の傾斜箱 + 前端に接合部（凹部）
    """
    vertices = []
    faces = []

    # 座標系：後端を原点として、前方向（-y方向）に伸びる
    back_y = 0  # 後端
    front_y = -BACK_DEPTH  # 前端

    # 後端での傾斜の高さ
    back_slope_z = slope_drop * ((TOP_DEPTH/2) / TOP_DEPTH)
    # 前端での傾斜の高さ
    front_slope_z = slope_drop * ((TOP_DEPTH/2 - BACK_DEPTH) / TOP_DEPTH)

    # === 外側の箱 ===
    # 上面（平行）
    top_outer = [
        [-TOP_WIDTH/2, back_y, TOTAL_HEIGHT],   # 後左
        [TOP_WIDTH/2, back_y, TOTAL_HEIGHT],    # 後右
        [TOP_WIDTH/2, front_y, TOTAL_HEIGHT],   # 前右
        [-TOP_WIDTH/2, front_y, TOTAL_HEIGHT],  # 前左
    ]

    # 下面（平行）
    bottom_outer = [
        [-TOP_WIDTH/2, back_y, 0],   # 後左
        [TOP_WIDTH/2, back_y, 0],    # 後右
        [TOP_WIDTH/2, front_y, 0],   # 前右
        [-TOP_WIDTH/2, front_y, 0],  # 前左
    ]

    # === 内側の空間 ===
    # 上面（少し低い）
    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), back_y, TOTAL_HEIGHT - WALL_THICKNESS],
        [(TOP_WIDTH/2 - WALL_THICKNESS), back_y, TOTAL_HEIGHT - WALL_THICKNESS],
        [(TOP_WIDTH/2 - WALL_THICKNESS), front_y, TOTAL_HEIGHT - WALL_THICKNESS],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), front_y, TOTAL_HEIGHT - WALL_THICKNESS],
    ]

    # 底面（傾斜）
    bottom_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), back_y, WALL_THICKNESS + back_slope_z],   # 後左
        [(TOP_WIDTH/2 - WALL_THICKNESS), back_y, WALL_THICKNESS + back_slope_z],    # 後右
        [(TOP_WIDTH/2 - WALL_THICKNESS), front_y, WALL_THICKNESS + front_slope_z],  # 前右
        [-(TOP_WIDTH/2 - WALL_THICKNESS), front_y, WALL_THICKNESS + front_slope_z], # 前左
    ]

    # === 接合部（凹部）- 前端に ===
    # 前端から少し手前（JOINT_DEPTH）に凹部を作る
    joint_y = front_y + JOINT_DEPTH
    joint_slope_z = slope_drop * ((TOP_DEPTH/2 - BACK_DEPTH + JOINT_DEPTH) / TOP_DEPTH)

    joint_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), joint_y, WALL_THICKNESS + joint_slope_z + JOINT_HEIGHT],
        [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), joint_y, WALL_THICKNESS + joint_slope_z + JOINT_HEIGHT],
        [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), front_y, WALL_THICKNESS + front_slope_z + JOINT_HEIGHT],
        [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), front_y, WALL_THICKNESS + front_slope_z + JOINT_HEIGHT],
    ]

    # === 外側の壁 ===
    # 後壁
    v_idx = len(vertices)
    vertices.extend([top_outer[0], top_outer[1], bottom_outer[1], bottom_outer[0]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 左壁
    v_idx = len(vertices)
    vertices.extend([top_outer[0], bottom_outer[0], bottom_outer[3], top_outer[3]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 右壁
    v_idx = len(vertices)
    vertices.extend([top_outer[1], top_outer[2], bottom_outer[2], bottom_outer[1]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 前壁
    v_idx = len(vertices)
    vertices.extend([top_outer[2], top_outer[3], bottom_outer[3], bottom_outer[2]])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # === 内側の壁 ===
    # 後壁
    v_idx = len(vertices)
    vertices.extend([top_inner[1], top_inner[0], bottom_inner[0], bottom_inner[1]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 左壁（後端から接合部まで）
    v_idx = len(vertices)
    vertices.extend([top_inner[0], top_inner[3], joint_inner[3], joint_inner[0]])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # 右壁（後端から接合部まで）
    v_idx = len(vertices)
    vertices.extend([top_inner[1], bottom_inner[1], joint_inner[1], top_inner[2]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # === 上部の蓋（リング） ===
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([top_outer[i], top_outer[next_i], top_inner[next_i], top_inner[i]])
        faces.append([v_idx, v_idx+1, v_idx+2])
        faces.append([v_idx, v_idx+2, v_idx+3])

    # === 接合部の底面と壁 ===
    # 接合部底面
    for i in range(4):
        next_i = (i + 1) % 4
        if i == 2:  # 前壁側はスキップ
            continue
        v_idx = len(vertices)
        bottom_joint = [
            [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), joint_y, WALL_THICKNESS + joint_slope_z],
            [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), joint_y, WALL_THICKNESS + joint_slope_z],
            [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), front_y, WALL_THICKNESS + front_slope_z],
            [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), front_y, WALL_THICKNESS + front_slope_z],
        ]
        vertices.extend([joint_inner[i], joint_inner[next_i], bottom_joint[next_i], bottom_joint[i]])
        faces.append([v_idx, v_idx+2, v_idx+1])
        faces.append([v_idx, v_idx+3, v_idx+2])

    return np.array(vertices), np.array(faces)

def create_front_part():
    """
    前部パーツを生成（出口側、100mm）
    後端に接合部（凸部）+ 前端が開放
    """
    vertices = []
    faces = []

    # 座標系：後端（接合部）を原点として、前方向（-y方向）に伸びる
    back_y = 0  # 後端（接合部）
    front_y = -FRONT_DEPTH  # 前端

    # 後端での傾斜の高さ（後部パーツの前端と一致）
    back_slope_z = slope_drop * ((TOP_DEPTH/2 - BACK_DEPTH) / TOP_DEPTH)
    # 前端での傾斜の高さ
    front_slope_z = slope_drop * ((TOP_DEPTH/2 - TOP_DEPTH) / TOP_DEPTH)
    # 開放開始位置での傾斜
    opening_y = -(FRONT_DEPTH - OPENING_START)
    opening_slope_z = slope_drop * ((TOP_DEPTH/2 - BACK_DEPTH - (FRONT_DEPTH - OPENING_START)) / TOP_DEPTH)

    # === 外側の箱 ===
    # 上面（平行）
    top_outer = [
        [-TOP_WIDTH/2, back_y, TOTAL_HEIGHT],   # 後左
        [TOP_WIDTH/2, back_y, TOTAL_HEIGHT],    # 後右
        [TOP_WIDTH/2, front_y, TOTAL_HEIGHT],   # 前右
        [-TOP_WIDTH/2, front_y, TOTAL_HEIGHT],  # 前左
    ]

    # 下面（平行）
    bottom_outer = [
        [-TOP_WIDTH/2, back_y, 0],   # 後左
        [TOP_WIDTH/2, back_y, 0],    # 後右
        [TOP_WIDTH/2, front_y, 0],   # 前右
        [-TOP_WIDTH/2, front_y, 0],  # 前左
    ]

    # === 内側の空間 ===
    # 上面（少し低い）
    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), back_y, TOTAL_HEIGHT - WALL_THICKNESS],
        [(TOP_WIDTH/2 - WALL_THICKNESS), back_y, TOTAL_HEIGHT - WALL_THICKNESS],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), opening_y, TOTAL_HEIGHT - WALL_THICKNESS],  # 開放開始位置まで
        [(TOP_WIDTH/2 - WALL_THICKNESS), opening_y, TOTAL_HEIGHT - WALL_THICKNESS],
    ]

    # 底面（傾斜）
    bottom_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), back_y, WALL_THICKNESS + back_slope_z],     # 後左
        [(TOP_WIDTH/2 - WALL_THICKNESS), back_y, WALL_THICKNESS + back_slope_z],      # 後右
        [-(TOP_WIDTH/2 - WALL_THICKNESS), opening_y, WALL_THICKNESS + opening_slope_z],  # 開放位置左
        [(TOP_WIDTH/2 - WALL_THICKNESS), opening_y, WALL_THICKNESS + opening_slope_z],   # 開放位置右
    ]

    # === 接合部（凸部）- 後端に ===
    joint_outer = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y, WALL_THICKNESS + back_slope_z + JOINT_HEIGHT],
        [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y, WALL_THICKNESS + back_slope_z + JOINT_HEIGHT],
        [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y - JOINT_DEPTH, WALL_THICKNESS + back_slope_z + JOINT_HEIGHT],
        [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y - JOINT_DEPTH, WALL_THICKNESS + back_slope_z + JOINT_HEIGHT],
    ]

    # === 外側の壁 ===
    # 後壁
    v_idx = len(vertices)
    vertices.extend([top_outer[0], top_outer[1], bottom_outer[1], bottom_outer[0]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 左壁
    v_idx = len(vertices)
    vertices.extend([top_outer[0], bottom_outer[0], bottom_outer[3], top_outer[3]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 右壁
    v_idx = len(vertices)
    vertices.extend([top_outer[1], top_outer[2], bottom_outer[2], bottom_outer[1]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 前壁（低い）
    front_wall_height = 10  # 前壁は低くする
    v_idx = len(vertices)
    vertices.extend([
        [TOP_WIDTH/2, front_y, front_wall_height],
        [-TOP_WIDTH/2, front_y, front_wall_height],
        bottom_outer[3],
        bottom_outer[2]
    ])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # === 内側の壁（開放位置まで） ===
    # 後壁（接合部との接続）
    v_idx = len(vertices)
    vertices.extend([top_inner[1], top_inner[0], joint_outer[0], joint_outer[1]])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # 左壁（後端から開放位置まで）
    v_idx = len(vertices)
    vertices.extend([top_inner[0], top_inner[2], bottom_inner[2], bottom_inner[0]])
    faces.append([v_idx, v_idx+2, v_idx+1])
    faces.append([v_idx, v_idx+3, v_idx+2])

    # 右壁（後端から開放位置まで）
    v_idx = len(vertices)
    vertices.extend([top_inner[1], bottom_inner[1], bottom_inner[3], top_inner[3]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # === 上部の蓋（開放位置まで） ===
    # 後部
    v_idx = len(vertices)
    vertices.extend([top_outer[0], top_outer[1], top_inner[1], top_inner[0]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 左側
    v_idx = len(vertices)
    vertices.extend([top_outer[0], top_inner[0], top_inner[2], top_outer[3]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # 右側
    v_idx = len(vertices)
    vertices.extend([top_outer[1], top_outer[2], top_inner[3], top_inner[1]])
    faces.append([v_idx, v_idx+1, v_idx+2])
    faces.append([v_idx, v_idx+2, v_idx+3])

    # === 接合部（凸部）の壁 ===
    # 凸部の側面
    for i in range(4):
        if i == 0:  # 後壁側はスキップ（すでに作成済み）
            continue
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        joint_bottom = [
            [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y, WALL_THICKNESS + back_slope_z],
            [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y, WALL_THICKNESS + back_slope_z],
            [(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y - JOINT_DEPTH, WALL_THICKNESS + back_slope_z],
            [-(TOP_WIDTH/2 - WALL_THICKNESS - CLEARANCE), back_y - JOINT_DEPTH, WALL_THICKNESS + back_slope_z],
        ]
        vertices.extend([joint_outer[i], joint_outer[next_i], joint_bottom[next_i], joint_bottom[i]])
        faces.append([v_idx, v_idx+1, v_idx+2])
        faces.append([v_idx, v_idx+2, v_idx+3])

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
    print("コインシュートSTLファイル生成中（前後分割版・ULTRATHINK設計）...")
    print(f"設計: 240×315×{TOTAL_HEIGHT}mmを前後2分割")
    print(f"後部: {BACK_DEPTH}mm（入口側）")
    print(f"前部: {FRONT_DEPTH}mm（出口側、前端開放）")
    print(f"内側傾斜: {SLOPE_ANGLE}度（高低差: {slope_drop:.1f}mm）")
    print(f"接合: はめ込み式（クリアランス: {CLEARANCE}mm、PETG用）")

    # 後部パーツ生成
    print("\n後部パーツ生成中（入口側、215mm）...")
    back_vertices, back_faces = create_back_part()
    save_stl(back_vertices, back_faces, "coin_chute_back.stl")

    # 前部パーツ生成
    print(f"前部パーツ生成中（出口側、100mm、前端開放）...")
    front_vertices, front_faces = create_front_part()
    save_stl(front_vertices, front_faces, "coin_chute_front.stl")

    print("\n✅ 完了！以下のファイルが生成されました:")
    print("- coin_chute_back.stl (後部パーツ: 215mm、入口側)")
    print("- coin_chute_front.stl (前部パーツ: 100mm、出口側、前端開放)")
    print(f"\n設計仕様:")
    print(f"- 前後分割（プリントエリア制約を満たす）")
    print(f"- 内側傾斜: {SLOPE_ANGLE}度")
    print(f"- 前端開放式（壁が低い）")
    print(f"- はめ込み式接合（PETG用）")
    print(f"- コインが自然に流れ落ちる設計")
