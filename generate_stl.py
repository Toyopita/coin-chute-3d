#!/usr/bin/env python3
"""
コイン計算機用シュート STL生成スクリプト（外見は箱、内側だけ傾斜）
2分割設計: 上部パーツ + 下部パーツ（集約部）

要件:
- 外見：240×315×120mmの普通の箱（直方体）
- 内側の底面だけ20度傾斜
- 下部で前端から40mmの位置に直径100mmの円形穴に集約
"""

import numpy as np
from stl import mesh
import math

# パラメータ (mm)
TOP_WIDTH = 240
TOP_DEPTH = 315
BOTTOM_DIAMETER = 100
WALL_THICKNESS = 2
HEIGHT_PER_PART = 60  # 各パーツの基本高さ
SEGMENTS = 32  # 円周の分割数
SLOPE_ANGLE = 20  # 傾斜角度（度）
HOLE_POSITION = 40  # 前端から穴の中心までの距離

# 傾斜による高低差
slope_drop = TOP_DEPTH * math.tan(math.radians(SLOPE_ANGLE))

def create_upper_part():
    """
    上部パーツを生成（外見は普通の箱、内側だけ傾斜）
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

    # 下部の蓋（長方形のリング）
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([bottom_outer[i], bottom_outer[next_i], bottom_inner[next_i], bottom_inner[i]])
        faces.append([v_idx, v_idx+2, v_idx+1])
        faces.append([v_idx, v_idx+3, v_idx+2])

    return np.array(vertices), np.array(faces)

def create_lower_part():
    """
    下部パーツを生成（集約部分）
    外側：240mm × 315mm × 60mm の直方体
    内側：底面が傾斜し、前端40mmの位置で直径100mmの円形穴に集約
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

    # 下部 - 円形（前端から40mmの位置、傾斜を考慮）
    hole_center_y = -TOP_DEPTH/2 + HOLE_POSITION

    bottom_outer_points = []
    bottom_inner_points = []

    for i in range(SEGMENTS):
        angle = 2 * math.pi * i / SEGMENTS
        x_outer = (BOTTOM_DIAMETER / 2) * math.cos(angle)
        y_outer = hole_center_y + (BOTTOM_DIAMETER / 2) * math.sin(angle)
        x_inner = (BOTTOM_DIAMETER / 2 - WALL_THICKNESS) * math.cos(angle)
        y_inner = hole_center_y + (BOTTOM_DIAMETER / 2 - WALL_THICKNESS) * math.sin(angle)

        # 円周上の各点での高さ（内側の傾斜に沿う）
        z_outer = (y_outer + TOP_DEPTH/2) / TOP_DEPTH * slope_drop - HEIGHT_PER_PART - WALL_THICKNESS
        z_inner = (y_inner + TOP_DEPTH/2) / TOP_DEPTH * slope_drop - HEIGHT_PER_PART - WALL_THICKNESS * 2

        bottom_outer_points.append([x_outer, y_outer, z_outer])
        bottom_inner_points.append([x_inner, y_inner, z_inner])

    # 外側の面：長方形の各辺から円周への接続
    segments_per_edge = SEGMENTS // 4

    for i in range(4):
        next_i = (i + 1) % 4
        top_start = np.array(top_outer[i])
        top_end = np.array(top_outer[next_i])

        for j in range(segments_per_edge):
            circle_idx = i * segments_per_edge + j
            next_circle_idx = (circle_idx + 1) % SEGMENTS

            # 長方形の辺上の点を補間
            t1 = j / segments_per_edge
            t2 = (j + 1) / segments_per_edge
            rect_p1 = top_start + t1 * (top_end - top_start)
            rect_p2 = top_start + t2 * (top_end - top_start)

            # 円周上の点
            circle_p1 = bottom_outer_points[circle_idx]
            circle_p2 = bottom_outer_points[next_circle_idx]

            # 四角形面を2つの三角形に分割
            v_idx = len(vertices)
            vertices.extend([rect_p1.tolist(), rect_p2.tolist(), circle_p2, circle_p1])
            faces.append([v_idx, v_idx+1, v_idx+2])
            faces.append([v_idx, v_idx+2, v_idx+3])

    # 内側の面：長方形から円への接続
    for i in range(4):
        next_i = (i + 1) % 4
        top_start = np.array(top_inner[i])
        top_end = np.array(top_inner[next_i])

        for j in range(segments_per_edge):
            circle_idx = i * segments_per_edge + j
            next_circle_idx = (circle_idx + 1) % SEGMENTS

            t1 = j / segments_per_edge
            t2 = (j + 1) / segments_per_edge
            rect_p1 = top_start + t1 * (top_end - top_start)
            rect_p2 = top_start + t2 * (top_end - top_start)

            circle_p1 = bottom_inner_points[circle_idx]
            circle_p2 = bottom_inner_points[next_circle_idx]

            # 内側は法線が逆向き
            v_idx = len(vertices)
            vertices.extend([rect_p1.tolist(), rect_p2.tolist(), circle_p2, circle_p1])
            faces.append([v_idx, v_idx+2, v_idx+1])
            faces.append([v_idx, v_idx+3, v_idx+2])

    # 上部の蓋（長方形のリング）
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([top_outer[i], top_outer[next_i], top_inner[next_i], top_inner[i]])
        faces.append([v_idx, v_idx+2, v_idx+1])
        faces.append([v_idx, v_idx+3, v_idx+2])

    # 下部の蓋（円形のリング）
    for i in range(SEGMENTS):
        next_i = (i + 1) % SEGMENTS
        v_idx = len(vertices)
        vertices.extend([
            bottom_outer_points[i],
            bottom_outer_points[next_i],
            bottom_inner_points[next_i],
            bottom_inner_points[i]
        ])
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
    print("コインシュートSTLファイル生成中（外見は箱、内側だけ傾斜）...")
    print(f"設計: 外見は240×315×{HEIGHT_PER_PART * 2}mmの直方体")
    print(f"内側の底面のみ20度傾斜（高低差: {slope_drop:.1f}mm）")
    print(f"穴の位置: 前端から{HOLE_POSITION}mm")

    # 上部パーツ生成
    print("\n上部パーツ生成中（外見は箱、内側だけ傾斜）...")
    upper_vertices, upper_faces = create_upper_part()
    save_stl(upper_vertices, upper_faces, "coin_chute_upper.stl")

    # 下部パーツ生成
    print(f"下部パーツ生成中（内側傾斜 → 前端{HOLE_POSITION}mm地点でΦ100mm）...")
    lower_vertices, lower_faces = create_lower_part()
    save_stl(lower_vertices, lower_faces, "coin_chute_lower.stl")

    print("\n✅ 完了！以下のファイルが生成されました:")
    print("- coin_chute_upper.stl (上部パーツ: 外見は箱、内側傾斜)")
    print("- coin_chute_lower.stl (下部パーツ: 集約部分)")
    print(f"\n外見: 240×315×{HEIGHT_PER_PART * 2}mmの直方体")
    print(f"内側傾斜角度: {SLOPE_ANGLE}度")
    print(f"穴の位置: 前端から{HOLE_POSITION}mm")
