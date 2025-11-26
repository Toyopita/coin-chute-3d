#!/usr/bin/env python3
"""
コイン計算機用シュート STL生成スクリプト
2分割設計: 上部パーツ + 下部パーツ
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
    """上部パーツを生成"""
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

    # 下部 - 楕円形の頂点 (z = 0)
    # 楕円のサイズ: 幅180mm, 奥行220mm
    bottom_outer_points = []
    bottom_inner_points = []
    ellipse_width = BOTTOM_DIAMETER * 1.8
    ellipse_depth = BOTTOM_DIAMETER * 2.2

    for i in range(SEGMENTS):
        angle = 2 * math.pi * i / SEGMENTS
        x_outer = (ellipse_width / 2) * math.cos(angle)
        y_outer = (ellipse_depth / 2) * math.sin(angle)
        x_inner = (ellipse_width / 2 - WALL_THICKNESS) * math.cos(angle)
        y_inner = (ellipse_depth / 2 - WALL_THICKNESS) * math.sin(angle)

        bottom_outer_points.append([x_outer, y_outer, 0])
        bottom_inner_points.append([x_inner, y_inner, 0])

    # 頂点リスト構築
    base_idx = 0

    # 外側の面を構築
    # 上部の長方形面
    vertices.extend(top_outer)

    # 上部長方形の外側面（4つの壁）
    for i in range(4):
        next_i = (i + 1) % 4
        # 長方形から楕円への遷移面を複数セグメントで近似
        top_start = np.array(top_outer[i])
        top_end = np.array(top_outer[next_i])

        # 対応する楕円上の点を見つける
        # 長方形の各辺に対応する楕円のセグメントを接続
        segments_per_edge = SEGMENTS // 4

        for j in range(segments_per_edge):
            ellipse_idx = i * segments_per_edge + j
            next_ellipse_idx = (ellipse_idx + 1) % SEGMENTS

            # 上部長方形の補間点
            t1 = j / segments_per_edge
            t2 = (j + 1) / segments_per_edge
            rect_p1 = top_start + t1 * (top_end - top_start)
            rect_p2 = top_start + t2 * (top_end - top_start)

            # 下部楕円の点
            ellipse_p1 = bottom_outer_points[ellipse_idx]
            ellipse_p2 = bottom_outer_points[next_ellipse_idx]

            # 四角形面を2つの三角形に分割
            v_idx = len(vertices)
            vertices.extend([rect_p1.tolist(), rect_p2.tolist(), ellipse_p2, ellipse_p1])
            faces.append([v_idx, v_idx+1, v_idx+2])
            faces.append([v_idx, v_idx+2, v_idx+3])

    # 内側の面を構築（同様の方法）
    vertices.extend(top_inner)

    for i in range(4):
        next_i = (i + 1) % 4
        top_start = np.array(top_inner[i])
        top_end = np.array(top_inner[next_i])

        segments_per_edge = SEGMENTS // 4

        for j in range(segments_per_edge):
            ellipse_idx = i * segments_per_edge + j
            next_ellipse_idx = (ellipse_idx + 1) % SEGMENTS

            t1 = j / segments_per_edge
            t2 = (j + 1) / segments_per_edge
            rect_p1 = top_start + t1 * (top_end - top_start)
            rect_p2 = top_start + t2 * (top_end - top_start)

            ellipse_p1 = bottom_inner_points[ellipse_idx]
            ellipse_p2 = bottom_inner_points[next_ellipse_idx]

            # 内側は法線が逆向き
            v_idx = len(vertices)
            vertices.extend([rect_p1.tolist(), rect_p2.tolist(), ellipse_p2, ellipse_p1])
            faces.append([v_idx, v_idx+2, v_idx+1])
            faces.append([v_idx, v_idx+3, v_idx+2])

    # 上部の蓋（長方形の上面）
    # 外側と内側の間を埋める
    for i in range(4):
        next_i = (i + 1) % 4
        v_idx = len(vertices)
        vertices.extend([top_outer[i], top_outer[next_i], top_inner[next_i], top_inner[i]])
        faces.append([v_idx, v_idx+1, v_idx+2])
        faces.append([v_idx, v_idx+2, v_idx+3])

    # 下部の蓋（楕円のリング）
    for i in range(SEGMENTS):
        next_i = (i + 1) % SEGMENTS
        v_idx = len(vertices)
        vertices.extend([
            bottom_outer_points[i],
            bottom_outer_points[next_i],
            bottom_inner_points[next_i],
            bottom_inner_points[i]
        ])
        faces.append([v_idx, v_idx+2, v_idx+1])
        faces.append([v_idx, v_idx+3, v_idx+2])

    return np.array(vertices), np.array(faces)

def create_lower_part():
    """下部パーツを生成"""
    vertices = []
    faces = []

    # 上部 - 楕円形 (z = HEIGHT_PER_PART)
    ellipse_width = BOTTOM_DIAMETER * 1.8
    ellipse_depth = BOTTOM_DIAMETER * 2.2

    top_outer_points = []
    top_inner_points = []

    for i in range(SEGMENTS):
        angle = 2 * math.pi * i / SEGMENTS
        x_outer = (ellipse_width / 2) * math.cos(angle)
        y_outer = (ellipse_depth / 2) * math.sin(angle)
        x_inner = (ellipse_width / 2 - WALL_THICKNESS) * math.cos(angle)
        y_inner = (ellipse_depth / 2 - WALL_THICKNESS) * math.sin(angle)

        top_outer_points.append([x_outer, y_outer, HEIGHT_PER_PART])
        top_inner_points.append([x_inner, y_inner, HEIGHT_PER_PART])

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

    # 外側の面
    for i in range(SEGMENTS):
        next_i = (i + 1) % SEGMENTS
        v_idx = len(vertices)
        vertices.extend([
            top_outer_points[i],
            top_outer_points[next_i],
            bottom_outer_points[next_i],
            bottom_outer_points[i]
        ])
        faces.append([v_idx, v_idx+1, v_idx+2])
        faces.append([v_idx, v_idx+2, v_idx+3])

    # 内側の面
    for i in range(SEGMENTS):
        next_i = (i + 1) % SEGMENTS
        v_idx = len(vertices)
        vertices.extend([
            top_inner_points[i],
            top_inner_points[next_i],
            bottom_inner_points[next_i],
            bottom_inner_points[i]
        ])
        faces.append([v_idx, v_idx+2, v_idx+1])
        faces.append([v_idx, v_idx+3, v_idx+2])

    # 上部の蓋
    for i in range(SEGMENTS):
        next_i = (i + 1) % SEGMENTS
        v_idx = len(vertices)
        vertices.extend([
            top_outer_points[i],
            top_outer_points[next_i],
            top_inner_points[next_i],
            top_inner_points[i]
        ])
        faces.append([v_idx, v_idx+2, v_idx+1])
        faces.append([v_idx, v_idx+3, v_idx+2])

    # 下部の蓋
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
    # メッシュオブジェクトを作成
    coin_chute = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, face in enumerate(faces):
        for j in range(3):
            coin_chute.vectors[i][j] = vertices[face[j]]

    coin_chute.save(filename)
    print(f"✅ {filename} を生成しました")

if __name__ == "__main__":
    print("コインシュートSTLファイル生成中...")

    # 上部パーツ生成
    print("上部パーツ生成中...")
    upper_vertices, upper_faces = create_upper_part()
    save_stl(upper_vertices, upper_faces, "coin_chute_upper.stl")

    # 下部パーツ生成
    print("下部パーツ生成中...")
    lower_vertices, lower_faces = create_lower_part()
    save_stl(lower_vertices, lower_faces, "coin_chute_lower.stl")

    print("\n完了！以下のファイルが生成されました:")
    print("- coin_chute_upper.stl (上部パーツ)")
    print("- coin_chute_lower.stl (下部パーツ)")
