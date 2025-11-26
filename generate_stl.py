#!/usr/bin/env python3
"""
コイン計算機用シュート STL生成スクリプト（改訂版）
2分割設計: 上部パーツ（ストレート）+ 下部パーツ（集約部）

要件:
- 上部240×315mmの受け口
- 最初の60mmくらいはストレート（幅を保つ）
- 下部60mmで急激に直径100mmの円形出口に集約
"""

import numpy as np
from stl import mesh
import math

# パラメータ (mm)
TOP_WIDTH = 240
TOP_DEPTH = 315
BOTTOM_DIAMETER = 100
WALL_THICKNESS = 2
HEIGHT_PER_PART = 60  # 各パーツの高さ
SEGMENTS = 32  # 円周の分割数

def create_upper_part():
    """
    上部パーツを生成（ストレート部分）
    240mm × 315mm の長方形がそのまま下まで続く
    """
    vertices = []
    faces = []

    # 上部 - 長方形の頂点 (z = HEIGHT_PER_PART)
    top_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART],
        [TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART],
        [TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART],
        [-TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART],
    ]

    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
    ]

    # 下部 - 同じサイズの長方形 (z = 0)
    bottom_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, 0],
        [TOP_WIDTH/2, -TOP_DEPTH/2, 0],
        [TOP_WIDTH/2, TOP_DEPTH/2, 0],
        [-TOP_WIDTH/2, TOP_DEPTH/2, 0],
    ]

    bottom_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), 0],
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), 0],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), 0],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), 0],
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
    240mm × 315mm の長方形から直径100mmの円形に急激に集約
    """
    vertices = []
    faces = []

    # 上部 - 長方形 (z = HEIGHT_PER_PART)
    top_outer = [
        [-TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART],
        [TOP_WIDTH/2, -TOP_DEPTH/2, HEIGHT_PER_PART],
        [TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART],
        [-TOP_WIDTH/2, TOP_DEPTH/2, HEIGHT_PER_PART],
    ]

    top_inner = [
        [-(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
        [(TOP_WIDTH/2 - WALL_THICKNESS), -(TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
        [(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
        [-(TOP_WIDTH/2 - WALL_THICKNESS), (TOP_DEPTH/2 - WALL_THICKNESS), HEIGHT_PER_PART],
    ]

    # 下部 - 円形 (z = 0)
    bottom_outer_points = []
    bottom_inner_points = []

    for i in range(SEGMENTS):
        angle = 2 * math.pi * i / SEGMENTS
        x_outer = (BOTTOM_DIAMETER / 2) * math.cos(angle)
        y_outer = (BOTTOM_DIAMETER / 2) * math.sin(angle)
        x_inner = (BOTTOM_DIAMETER / 2 - WALL_THICKNESS) * math.cos(angle)
        y_inner = (BOTTOM_DIAMETER / 2 - WALL_THICKNESS) * math.sin(angle)

        bottom_outer_points.append([x_outer, y_outer, 0])
        bottom_inner_points.append([x_inner, y_inner, 0])

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
    print("コインシュートSTLファイル生成中（改訂版）...")
    print("設計: 上部60mmストレート + 下部60mm集約部")

    # 上部パーツ生成
    print("\n上部パーツ生成中（240×315mm ストレート）...")
    upper_vertices, upper_faces = create_upper_part()
    save_stl(upper_vertices, upper_faces, "coin_chute_upper.stl")

    # 下部パーツ生成
    print("下部パーツ生成中（240×315mm → Φ100mm 集約）...")
    lower_vertices, lower_faces = create_lower_part()
    save_stl(lower_vertices, lower_faces, "coin_chute_lower.stl")

    print("\n✅ 完了！以下のファイルが生成されました:")
    print("- coin_chute_upper.stl (上部パーツ: ストレート部分)")
    print("- coin_chute_lower.stl (下部パーツ: 集約部分)")
    print("\n上部60mm: 幅を保つ")
    print("下部60mm: 急激に円形出口に集約")
