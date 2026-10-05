"""
Vector 3D Geometry Writer for SVG-Native Glass Meshes.
Features:
- Icosahedron, Dodecahedron, Triangular Prism, Crystal Shard.
- Perspective projection (f ≈ 3.2).
- Key light (top-left) & Crimson fill light (bottom-right).
- Fresnel rim light, Lambert crimson shading, and Blinn-Phong specular highlights.
- Dual-layer (back/front) depth ordering with SMIL path & opacity morphing.
- Deterministic keyframe generation for seamless loops.
"""

import numpy as np
from .tokens import CRIMSON

def rotation_matrix(axis: np.ndarray, theta: float) -> np.ndarray:
    """Return Rodrigues rotation matrix for rotation about given axis by theta radians."""
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([
        [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
        [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
        [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]
    ])

def get_mesh_data(mesh_type: str = "icosahedron"):
    """Returns vertices and triangular face indices for specified mesh."""
    if mesh_type == "icosahedron":
        phi = (1.0 + np.sqrt(5.0)) / 2.0
        vertices = np.array([
            [-1,  phi,  0], [ 1,  phi,  0], [-1, -phi,  0], [ 1, -phi,  0],
            [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
            [ phi,  0, -1], [ phi,  0,  1], [-phi,  0, -1], [-phi,  0,  1]
        ], dtype=float)
        faces = [
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
        ]
    elif mesh_type == "prism":
        # Triangular prism
        h = 1.2
        r = 1.0
        angles = np.array([0, 2 * np.pi / 3, 4 * np.pi / 3])
        top = np.column_stack([r * np.cos(angles), r * np.sin(angles), np.full(3, h / 2)])
        bot = np.column_stack([r * np.cos(angles), r * np.sin(angles), np.full(3, -h / 2)])
        vertices = np.vstack([top, bot])
        faces = [
            [0, 1, 2],      # top cap
            [3, 5, 4],      # bottom cap
            [0, 3, 4], [0, 4, 1], # side 1
            [1, 4, 5], [1, 5, 2], # side 2
            [2, 5, 3], [2, 3, 0], # side 3
        ]
    elif mesh_type == "crystal":
        # Octahedral crystal shard (elongated bipyramid)
        vertices = np.array([
            [ 0.0,  0.0,  1.7],  # top tip
            [ 0.0,  0.0, -1.7],  # bottom tip
            [ 0.9,  0.0,  0.0],
            [ 0.0,  0.9,  0.0],
            [-0.9,  0.0,  0.0],
            [ 0.0, -0.9,  0.0],
        ], dtype=float)
        faces = [
            [0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 2], # top cone
            [1, 3, 2], [1, 4, 3], [1, 5, 4], [1, 2, 5], # bottom cone
        ]
    else:  # Dodecahedron-inspired gem / truncated cube
        vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1],
            [0, -1.4, 0], [0, 1.4, 0], [1.4, 0, 0], [-1.4, 0, 0],
            [0, 0, 1.4], [0, 0, -1.4]
        ], dtype=float)
        # normalize to unit sphere
        vertices = vertices / np.linalg.norm(vertices, axis=1, keepdims=True)
        faces = [
            [0, 1, 8], [1, 5, 8], [5, 4, 8], [4, 0, 8],
            [3, 9, 2], [2, 9, 6], [6, 9, 7], [7, 9, 3],
            [4, 12, 5], [5, 12, 6], [6, 12, 7], [7, 12, 4],
            [0, 13, 3], [3, 13, 2], [2, 13, 1], [1, 13, 0],
            [1, 10, 2], [2, 10, 6], [6, 10, 5], [5, 10, 1],
            [0, 11, 4], [4, 11, 7], [7, 11, 3], [3, 11, 0]
        ]
        
    # Scale to unit sphere
    max_r = np.max(np.linalg.norm(vertices, axis=1))
    vertices = vertices / max_r
    return vertices, np.array(faces, dtype=int)

def render_3d_glass_mesh(
    mesh_type: str = "icosahedron",
    cx: float = 200,
    cy: float = 200,
    scale: float = 140,
    num_frames: int = 36,
    duration_s: float = 18.0,
    axis: tuple[float, float, float] = (0.7, 1.0, 0.4),
    prefix: str = "mesh"
) -> str:
    """
    Generate an SVG group with animated SMIL paths for a rotating 3D glass mesh.
    Includes perspective projection, dual-depth layering, Fresnel rim, and Blinn-Phong highlights.
    """
    vertices, faces = get_mesh_data(mesh_type)
    num_faces = len(faces)
    
    # Lighting setup
    focal = 3.2
    cam_dist = 3.4
    cam_pos = np.array([0.0, 0.0, -cam_dist])
    
    key_light = np.array([-0.6, -0.8, 1.0])
    key_light /= np.linalg.norm(key_light)
    
    fill_light = np.array([0.8, 0.6, -0.5])
    fill_light /= np.linalg.norm(fill_light)
    
    rot_axis = np.array(axis, dtype=float)
    rot_axis /= np.linalg.norm(rot_axis)
    
    # Precompute per-face frames
    face_d_frames = [[] for _ in range(num_faces)]
    face_front_opacity = [[] for _ in range(num_faces)]
    face_back_opacity = [[] for _ in range(num_faces)]
    face_fill_colors = [[] for _ in range(num_faces)]
    face_edge_opacity = [[] for _ in range(num_faces)]
    
    thetas = np.linspace(0, 2 * np.pi, num_frames, endpoint=False)
    
    for theta in thetas:
        R = rotation_matrix(rot_axis, theta)
        v_rot = vertices @ R.T
        
        # Perspective projection
        z_cam = v_rot[:, 2] + cam_dist
        z_cam = np.maximum(z_cam, 0.1)
        proj_x = cx + (focal * v_rot[:, 0] / z_cam) * scale
        proj_y = cy + (focal * v_rot[:, 1] / z_cam) * scale
        
        for fi, face in enumerate(faces):
            p0, p1, p2 = v_rot[face[0]], v_rot[face[1]], v_rot[face[2]]
            
            # Normal calculation
            normal = np.cross(p1 - p0, p2 - p0)
            norm_len = np.linalg.norm(normal)
            if norm_len > 1e-6:
                normal /= norm_len
            else:
                normal = np.array([0.0, 0.0, 1.0])
                
            centroid = (p0 + p1 + p2) / 3.0
            view_dir = centroid - cam_pos
            view_dir /= np.linalg.norm(view_dir)
            
            ndotv = np.dot(normal, view_dir)
            is_front = ndotv < 0  # Points towards camera
            abs_ndotv = np.clip(np.abs(ndotv), 0.0, 1.0)
            
            # Fresnel rim
            fresnel = (1.0 - abs_ndotv) ** 3.0
            
            # Lambert shading with fill
            lambert = np.clip(np.dot(normal, -key_light), 0.0, 1.0)
            crimson_intensity = np.clip(0.25 + 0.65 * lambert, 0.0, 1.0)
            
            # Blinn-Phong specular highlight
            half_vec = key_light - view_dir
            half_vec /= np.linalg.norm(half_vec)
            spec = np.clip(np.dot(normal, half_vec), 0.0, 1.0) ** 32.0
            
            # 2D coordinates rounded to 1 decimal
            x0, y0 = round(proj_x[face[0]], 1), round(proj_y[face[0]], 1)
            x1, y1 = round(proj_x[face[1]], 1), round(proj_y[face[1]], 1)
            x2, y2 = round(proj_x[face[2]], 1), round(proj_y[face[2]], 1)
            d_str = f"M {x0} {y0} L {x1} {y1} L {x2} {y2} Z"
            face_d_frames[fi].append(d_str)
            
            # Opacities
            if is_front:
                front_op = round(0.18 + 0.28 * abs_ndotv + 0.35 * spec, 2)
                back_op = 0.0
            else:
                front_op = 0.0
                back_op = round(0.08 + 0.15 * abs_ndotv, 2)
                
            edge_op = round(0.25 + 0.50 * fresnel, 2)
            
            face_front_opacity[fi].append(front_op)
            face_back_opacity[fi].append(back_op)
            face_edge_opacity[fi].append(edge_op)
            
            # Fill color interpolating crimson
            if spec > 0.4:
                fill_col = "#FFFFFF"
            elif crimson_intensity > 0.6:
                fill_col = CRIMSON[400]
            elif crimson_intensity > 0.3:
                fill_col = CRIMSON[600]
            else:
                fill_col = CRIMSON[800]
            face_fill_colors[fi].append(fill_col)
            
    # Build SMIL animated paths
    key_times = ";".join([f"{i / num_frames:.3f}" for i in range(num_frames)] + ["1.000"])
    
    back_paths = []
    front_paths = []
    
    for fi in range(num_faces):
        d_vals = ";".join(face_d_frames[fi] + [face_d_frames[fi][0]])
        front_op_vals = ";".join([str(v) for v in face_front_opacity[fi]] + [str(face_front_opacity[fi][0])])
        back_op_vals = ";".join([str(v) for v in face_back_opacity[fi]] + [str(face_back_opacity[fi][0])])
        edge_op_vals = ";".join([str(v) for v in face_edge_opacity[fi]] + [str(face_edge_opacity[fi][0])])
        fill_col_vals = ";".join(face_fill_colors[fi] + [face_fill_colors[fi][0]])
        
        init_d = face_d_frames[fi][0]
        init_back_op = face_back_opacity[fi][0]
        init_front_op = face_front_opacity[fi][0]
        init_edge_op = face_edge_opacity[fi][0]
        init_fill = face_fill_colors[fi][0]
        
        # Back face element
        back_elem = f"""
      <path id="{prefix}-b-{fi}" d="{init_d}" fill="{CRIMSON[950]}" fill-opacity="{init_back_op}"
            stroke="{CRIMSON[700]}" stroke-width="0.75" stroke-opacity="{init_edge_op * 0.5:.2f}">
        <animate attributeName="d" values="{d_vals}" keyTimes="{key_times}" dur="{duration_s}s" repeatCount="indefinite"/>
        <animate attributeName="fill-opacity" values="{back_op_vals}" keyTimes="{key_times}" dur="{duration_s}s" repeatCount="indefinite"/>
      </path>"""
        back_paths.append(back_elem)
        
        # Front face element
        front_elem = f"""
      <path id="{prefix}-f-{fi}" d="{init_d}" fill="{init_fill}" fill-opacity="{init_front_op}"
            stroke="#FFFFFF" stroke-width="1.0" stroke-opacity="{init_edge_op}">
        <animate attributeName="d" values="{d_vals}" keyTimes="{key_times}" dur="{duration_s}s" repeatCount="indefinite"/>
        <animate attributeName="fill-opacity" values="{front_op_vals}" keyTimes="{key_times}" dur="{duration_s}s" repeatCount="indefinite"/>
        <animate attributeName="fill" values="{fill_col_vals}" keyTimes="{key_times}" dur="{duration_s}s" repeatCount="indefinite"/>
        <animate attributeName="stroke-opacity" values="{edge_op_vals}" keyTimes="{key_times}" dur="{duration_s}s" repeatCount="indefinite"/>
      </path>"""
        front_paths.append(front_elem)

    svg = f"""
  <!-- 3D Glass Mesh ({mesh_type}) at ({cx}, {cy}) -->
  <g id="{prefix}-container">
    <!-- Back faces layer (depth background) -->
    <g id="{prefix}-back-layer">
      {''.join(back_paths)}
    </g>

    <!-- Front faces layer (depth foreground with white rim edges) -->
    <g id="{prefix}-front-layer">
      {''.join(front_paths)}
    </g>
  </g>
"""
    return svg
