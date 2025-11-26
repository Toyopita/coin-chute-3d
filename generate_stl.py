#!/usr/bin/env python3
"""
コイン計算機用シュート STL生成スクリプト（箱全体が傾斜版）
2分割設計: 上部パーツ（傾斜）+ 下部パーツ（集約部）

要件:
- 上部240×315mmの受け口
- 箱全体が20度傾斜（手前側120mm、奥側235mm）
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
    上部パーツを生成（箱全体が傾斜）
    240mm × 315mm の長方形、箱全体が20度傾斜
    手前側: 60mm、奥側: 60mm + 57.4mm = 117.4mm
    """
    vertices = []
    faces = []

    # 各パーツの傾斜による高低差（半分）
    half_slope_drop = slope_drop / 2  # 57.4mm

    # 上部 - 長方形の頂点（箱全体が傾斜）
    # 手前側: HEIGHT_PER_PART、奥側: HEIGHT_PER_PART + half_slope_drop
    top_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART + half_slope_drop],  # 手前左
        [TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART + half_slope_drop],   # 手前右
        [TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART + slope_drop],   # 奥右
        [-TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART + slope_drop],  # 奥左
    ]

    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART + half_slope_drop],
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART + half_slope_drop],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART + slope_drop],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART + slope_drop],
    ]

    # 下部 - 箱全体が傾斜
    # 手前側: half_slope_drop、奥側: slope_drop
    bottom_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, half_slope_drop],  # 手前左
        [TOP_WIDTH/2, -TOP_DEPTH/2, half_slope_drop],   # 手前右
        [TOP_WIDTH/2, TOP_DEPTH/2, slope_drop],   # 奥右
        [-TOP_WIDTH/2, TOP_DEPTH/2, slope_drop],  # 奥左
    ]

    bottom_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), half_slope_drop],
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), half_slope_drop],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), slope_drop],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), slope_drop],
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
    240mm × 315mm の長方形から前端40mmの位置に直径100mmの円形に集約
    箱全体が傾斜している
    手前側: 0mm、奥側: 57.4mm
    """
    vertices = []
    faces = []

    # 各パーツの傾斜による高低差（半分）
    half_slope_drop = slope_drop / 2  # 57.4mm

    # 上部 - 長方形（箱全体が傾斜）
    # 手前側: half_slope_drop、奥側: slope_drop
    top_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, half_slope_drop],  # 手前左
        [TOP_WIDTH/2, -TOP_DEPTH/2, half_slope_drop],   # 手前右
        [TOP_WIDTH/2, TOP_DEPTH/2, slope_drop],   # 奥右
        [-TOP_WIDTH/2, TOP_DEPTH/2, slope_drop],  # 奥左
    ]

    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), half_slope_drop],
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), half_slope_drop],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), slope_drop],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), slope_drop],
    ]

    # 下部 - 円形（前端から40mmの位置、箱全体の傾斜を考慮）
    # 穴の中心のy座標
    hole_center_y = -TOP_DEPTH/2 + HOLE_POSITION

    # 各パーツの傾斜による高低差（半分）
    half_slope_drop = slope_drop / 2  # 57.4mm

    bottom_outer_points = []
    bottom_inner_points = []

    for i in range(SEGMENTS):
        angle = 2 * math.pi * i / SEGMENTS
        x_outer = (BOTTOM_DIAMETER / 2) * math.cos(angle)
        y_outer = hole_center_y + (BOTTOM_DIAMETER / 2) * math.sin(angle)
        x_inner = (BOTTOM_DIAMETER / 2 - WALL_THICKNESS) * math.cos(angle)
        y_inner = hole_center_y + (BOTTOM_DIAMETER / 2 - WALL_THICKNESS) * math.sin(angle)

        # 円周上の各点での高さ（箱全体の傾斜に沿う）
        # 下部パーツの底面は手前側で0mm、奥側でhalf_slope_dropの高さ
        z_outer = (y_outer + TOP_DEPTH/2) / TOP_DEPTH * half_slope_drop - HEIGHT_PER_PART
        z_inner = (y_inner + TOP_DEPTH/2) / TOP_DEPTH * half_slope_drop - HEIGHT_PER_PART

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
    print("コインシュートSTLファイル生成中（箱全体が傾斜版）...")
    print(f"設計: 20度傾斜（箱全体） + 穴を前端から{HOLE_POSITION}mmに配置")
    print(f"傾斜による高低差: {slope_drop:.1f}mm")
    print(f"手前側の高さ: {HEIGHT_PER_PART * 2:.0f}mm、奥側の高さ: {HEIGHT_PER_PART * 2 + slope_drop:.1f}mm")

    # 上部パーツ生成
    print("\n上部パーツ生成中（240×315mm 箱全体が傾斜）...")
    upper_vertices, upper_faces = create_upper_part()
    save_stl(upper_vertices, upper_faces, "coin_chute_upper.stl")

    # 下部パーツ生成
    print(f"下部パーツ生成中（240×315mm → 前端{HOLE_POSITION}mm地点でΦ100mm）...")
    lower_vertices, lower_faces = create_lower_part()
    save_stl(lower_vertices, lower_faces, "coin_chute_lower.stl")

    print("\n✅ 完了！以下のファイルが生成されました:")
    print("- coin_chute_upper.stl (上部パーツ: 箱全体が傾斜)")
    print("- coin_chute_lower.stl (下部パーツ: 集約部分)")
    print(f"\n傾斜角度: {SLOPE_ANGLE}度")
    print(f"穴の位置: 前端から{HOLE_POSITION}mm")
    print(f"箱全体の高さ: 手前側 {HEIGHT_PER_PART * 2:.0f}mm、奥側 {HEIGHT_PER_PART * 2 + slope_drop:.1f}mm")
