// コイン計算機用シュート - 2分割設計
// 上部: 240mm x 315mm → 下部: 直径100mm
// 傾斜角度: 40度
// Bambu Lab A1対応 (256x256x256mm)

// パラメータ
top_width = 240;      // 上部幅 (mm)
top_depth = 315;      // 上部奥行き (mm)
bottom_diameter = 100; // 下部出口直径 (mm)
wall_thickness = 2;    // 壁厚 (mm)
height = 60;          // 各パーツの高さ (mm)
slope_angle = 40;     // 傾斜角度 (度)

// 上部パーツ (Part 1)
module upper_part() {
    difference() {
        // 外側の形状
        hull() {
            // 上部 - 長方形
            translate([0, 0, height])
                cube([top_width, top_depth, 0.1], center=true);

            // 下部 - 楕円形（中間形状）
            translate([0, 0, 0])
                scale([1.8, 2.2, 1])
                cylinder(h=0.1, d=bottom_diameter*2, center=true);
        }

        // 内側をくり抜く
        hull() {
            // 上部内側
            translate([0, 0, height + 0.1])
                cube([top_width - wall_thickness*2, top_depth - wall_thickness*2, 0.1], center=true);

            // 下部内側
            translate([0, 0, -0.1])
                scale([1.8, 2.2, 1])
                cylinder(h=0.1, d=bottom_diameter*2 - wall_thickness*2, center=true);
        }
    }

    // 組み立て用のスナップフィット突起（4箇所）
    for (angle = [0, 90, 180, 270]) {
        rotate([0, 0, angle])
            translate([bottom_diameter*0.9, 0, -2])
                cylinder(h=5, d=4, $fn=20);
    }
}

// 下部パーツ (Part 2)
module lower_part() {
    difference() {
        // 外側の形状
        hull() {
            // 上部 - 楕円形（上部パーツの下部と同じ）
            translate([0, 0, height])
                scale([1.8, 2.2, 1])
                cylinder(h=0.1, d=bottom_diameter*2, center=true);

            // 下部 - 円形（出口）
            translate([0, 0, 0])
                cylinder(h=0.1, d=bottom_diameter, center=true);
        }

        // 内側をくり抜く
        hull() {
            // 上部内側
            translate([0, 0, height + 0.1])
                scale([1.8, 2.2, 1])
                cylinder(h=0.1, d=bottom_diameter*2 - wall_thickness*2, center=true);

            // 下部内側
            translate([0, 0, -0.1])
                cylinder(h=0.1, d=bottom_diameter - wall_thickness*2, center=true);
        }

        // スナップフィット用の穴（4箇所）
        for (angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
                translate([bottom_diameter*0.9, 0, height - 3])
                    cylinder(h=6, d=4.2, $fn=20);
        }
    }
}

// レンダリング選択
// "upper" = 上部パーツ, "lower" = 下部パーツ, "both" = 両方表示
part = "both"; // "upper", "lower", "both"

if (part == "upper") {
    upper_part();
} else if (part == "lower") {
    lower_part();
} else if (part == "both") {
    upper_part();
    translate([0, 0, -height - 10])
        lower_part();
}
