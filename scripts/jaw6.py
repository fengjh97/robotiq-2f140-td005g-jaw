"""
v4 ring jaws — Robotiq 2F-140, Makita TD005G, top-down, ring BELOW the trigger.

Pose found by the kinematic search (search.py):
  gripper axis tilted 9 deg (parallel to the grip axis), gripper centre on the grip axis,
  grasp opening S = 48 mm (screw axis to centre)  -> theta = 0.413 rad, mount face z = 163.5 (G)
  head rises into the V of the inner links; z0 = tool origin (grip axis @ head underside) in G.
Both jaws are the SAME part (second one rotated 180 deg about the gripper axis).
Local frame: origin = M5 screw axis on mount face, +Z fingertip direction, +Y towards centre.
"""
import math, sys
import cadquery as cq
sys.path.insert(0, '.')
from tool import T as TP, grip_axis_x, grip_dims
from gripper import theta_of_S, mount_pose

P = dict(
    S=48.0, beta=9.0, x0=0.0,
    z0_margin=3.0,            # head kept 3 mm below its collision limit (= +-3 mm height tolerance)
    z0_min=193.16,            # from search.py for S=48, beta=9, x0=0 (3 mm clearance)
    ring_t0=33.0, ring_t1=64.0,   # ring span along the grip, below the head underside (tool z)
    liner_t0=35.0, liner_t1=62.0,
    # TPU directional fin liner
    fin_t=0.8, fin_len=3.5, fin_angle=45.0, fin_pitch=3.6, fin_interf=0.8, liner_base_t=1.2,
    pocket_clear=0.15,
    head_clear=3.0, trig_clear=3.0,
    col_y=14.0, half_w=31.0, ring_wall=7.0, H=100.0, back_y=-5.35,
    liner_base=2.0, rib_h=1.0, interference=0.3, lip_clear=1.5,
    rib_w=1.6, rib_pitch=3.2, liner_clear=0.15,
    tongue_w=5.0, tongue_h=2.5, groove_clear=0.3,
    floor=8.0, screw_clear=5.5, head_pocket=12.6,   # PLA: M5x16 + 8 mm floor, OD12 washer
    pin_d=2.25, pin_depth=3.2, pin_x=4.5,
    relief_y=7.0, relief_z=8.0, relief_halfw=8.1,
    back_y2=-12.0,           # thickened back (above the mount face) -> closed tube around the screw channel
)


P["pocket_off"] = None

def pose(p=P):
    th = theta_of_S(p["S"]); mz = mount_pose(th)[1]
    z0 = p["z0_min"] + p["z0_margin"]
    return th, mz, z0


def to_local(shape, p=P, mirror=False):
    """tool frame -> gripper G -> jaw-A local. mirror=True also adds the X-mirrored copy
    (so the same part works as jaw B, rotated 180 deg)."""
    th, mz, z0 = pose(p)
    s = shape.rotate((0, 0, 0), (0, 1, 0), p["beta"]).translate((p["x0"], 0, z0)).translate((0, p["S"], -mz))
    if mirror:
        s = s.union(s.mirror("YZ"))
    return s


def grip_loft(off, t0, t1, n=8):
    secs = []
    for i in range(n + 1):
        z = t0 + (t1 - t0) * i / n
        d, w = grip_dims(z)
        secs.append(cq.Workplane("XY").workplane(offset=z).center(grip_axis_x(z), 0)
                    .ellipse(d / 2 + off, w / 2 + off).val())
    wires = [cq.Wire.assembleEdges(s.Edges()) for s in secs]
    return cq.Workplane("XY").add(cq.Solid.makeLoft(wires, True))


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def teardrop_z(d, length, z0):
    r = d / 2; c45 = r * math.cos(math.radians(45))
    circ = cq.Workplane("XY").workplane(offset=z0).circle(r).extrude(length)
    tip = (cq.Workplane("XY").workplane(offset=z0)
           .polyline([(c45, c45), (0, r * math.sqrt(2)), (-c45, c45)]).close().extrude(length))
    return circ.union(tip)


def tri_prism(xc, y_base, w, h, z0, z1, sign=1):
    pts = [(xc - w / 2, y_base), (xc + w / 2, y_base), (xc, y_base + sign * h)]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(z1 - z0)


def local_z_of_tool_z(tz, p=P):
    th, mz, z0 = pose(p)
    return z0 + tz * math.cos(math.radians(p["beta"])) - mz


def fin_geom(p=P):
    a = math.radians(p["fin_angle"])
    h = p["fin_len"] * math.sin(a)                 # radial height of a fin
    r_tip = -p["fin_interf"]                        # fin tips reach into the grip by fin_interf (free state)
    r0 = r_tip + h                                  # liner base inner surface
    r1 = r0 + p["liner_base_t"]                     # liner base outer surface
    return h, r_tip, r0, r1


def loft2(off_a, za, off_b, zb):
    """solid loft between grip-offset ellipses at two tool-z levels (different offsets)."""
    secs = []
    for z, off in ((za, off_a), (zb, off_b)):
        d, w = grip_dims(z)
        secs.append(cq.Workplane("XY").workplane(offset=z).center(grip_axis_x(z), 0)
                    .ellipse(d / 2 + off, w / 2 + off).val())
    wires = [cq.Wire.assembleEdges(s.Edges()) for s in secs]
    return cq.Workplane("XY").add(cq.Solid.makeLoft(wires, True))


def fin_liner(p=P):
    h, r_tip, r0, r1 = fin_geom(p)
    c = p["pocket_clear"]
    t0, t1 = p["liner_t0"] + c, p["liner_t1"] - c
    base = grip_loft(r1 - c, t0, t1).cut(grip_loft(r0, t0 - 1, t1 + 1))
    dz_t = p["fin_t"] / math.sin(math.radians(p["fin_angle"]))   # axial thickness of a fin
    # fins: base at tool-z zb (radius r0), tip towards the HEAD (smaller tool z) at zb-h (radius r_tip)
    zb = t1 - 0.5
    fins = None
    while zb - h - 0.2 > t0:
        A = loft2(r0 + 0.3, zb + 0.3, r_tip, zb - h)            # solid frustum (slightly into the base)
        B = A.translate((0, 0, dz_t))
        band = grip_loft(r0 + 0.31, zb - h - 1, zb + dz_t + 1).cut(grip_loft(r_tip, zb - h - 2, zb + dz_t + 2))
        f = A.cut(B).intersect(band)
        fins = f if fins is None else fins.union(f)
        zb -= p["fin_pitch"]
    liner = base.union(fins)
    return to_local(liner).intersect(box(-200, 200, -100, P["S"] - 0.3, -100, 300))


def build(p=P):
    p["pocket_off"] = fin_geom(p)[3]
    S, H, y0, W = p["S"], p["H"], p["back_y"], p["half_w"]
    zr0 = local_z_of_tool_z(p["ring_t0"]) - 6      # ring block start (local)
    # --- envelope: column + ring block ---
    body = box(-W, W, y0, p["col_y"], 0, H).union(box(-W, W, y0, S, zr0, H))
    yb2 = p["back_y2"]
    back = (cq.Workplane("YZ").polyline([(y0 + 0.01, 0.0), (y0 + 0.01, H), (yb2, H), (yb2, (y0 - yb2))]).close()
            .extrude(W, both=True))
    body = body.union(back)
    # --- head clearance (head swept over the height tolerance, + X-mirror) ---
    hh, hw = TP["head_h"], TP["head_w"]
    hc_ = p["head_clear"]
    head = (cq.Workplane("YZ").center(0, -hh / 2).ellipse(hw / 2 + hc_, hh / 2 + hc_)
            .extrude(TP["head_back"] + TP["head_front"] + 40).translate((-TP["head_back"] - 20, 0, 0)))
    head = head.union(head.translate((0, 0, p["z0_margin"]))).union(head.translate((0, 0, -p["z0_margin"])))
    body = body.cut(to_local(head, mirror=True))
    # --- trigger clearance (+ mirror) ---
    d0, _ = grip_dims(10)
    tc = p["trig_clear"]
    trig = box(d0 / 2 - 8, d0 / 2 + TP["trig_protrude"] + tc, -TP["trig_half_w"] - tc, TP["trig_half_w"] + tc,
               TP["trig_z0"] - tc - p["z0_margin"], TP["trig_z1"] + tc + p["z0_margin"])
    body = body.cut(to_local(trig, mirror=True))
    # --- grip cavity: lips through, liner pocket, everything past the parting plane ---
    off = p["liner_base"] + p["rib_h"] - p["interference"]
    body = body.cut(to_local(grip_loft(p["lip_clear"], -30, p["liner_t0"])))
    body = body.cut(to_local(grip_loft(p["pocket_off"], p["liner_t0"] - 0.01, p["liner_t1"] + 0.01)))
    body = body.cut(to_local(grip_loft(p["lip_clear"], p["liner_t1"], 140)))
    body = body.cut(box(-200, 200, S, S + 200, -50, 300))
    # lead-in chamfer at the bottom of the ring
    lead = grip_loft(p["lip_clear"] + 0.01, p["ring_t1"], p["ring_t1"] + 0.1, n=1)
    zb = local_z_of_tool_z(p["ring_t1"])
    # (simple 45deg chamfer: cone-ish loft between lip ellipse and +4 mm ellipse over 4 mm)
    d1, w1 = grip_dims(p["ring_t1"]); xa = grip_axis_x(p["ring_t1"])
    ch = (cq.Workplane("XY").workplane(offset=p["ring_t1"] + 0.5).center(xa, 0)
          .ellipse(d1 / 2 + p["lip_clear"], w1 / 2 + p["lip_clear"])
          .workplane(offset=40).ellipse(d1 / 2 + 44, w1 / 2 + 44).loft())
    body = body.cut(to_local(ch))
    # --- tongue / groove at the two ring tips ---
    th, mz, z0 = pose(p)
    zt0, zt1 = local_z_of_tool_z(p["ring_t0"]) + 2, local_z_of_tool_z(p["ring_t1"]) - 2
    dA, _ = grip_dims((p["ring_t0"] + p["ring_t1"]) / 2)
    arm_c = dA / 2 + p["lip_clear"] + (W - dA / 2 - p["lip_clear"]) / 2
    body = body.union(tri_prism(+arm_c, S - 0.01, p["tongue_w"], p["tongue_h"], zt0, zt1, +1))
    c = p["groove_clear"]
    body = body.cut(tri_prism(-arm_c, S + 0.01, p["tongue_w"] + 2 * c, p["tongue_h"] + c, zt0 - 1, zt1 + 1, -1))
    # --- 45deg back-corner relief + mounting interface ---
    ry, rz = p["relief_y"], p["relief_z"]
    for sx in (1, -1):
        r = (cq.Workplane("YZ").polyline([(p["back_y2"] - 1, -0.01), (ry, -0.01), (ry - rz, rz), (p["back_y2"] - 1, rz)]).close()
             .extrude(60).translate((p["relief_halfw"] if sx > 0 else -p["relief_halfw"] - 60, 0, 0)))
        body = body.cut(r)
        # extra 2 mm under-base relief: clearance to the inner-knuckle boss (stock tip has only 0.5 mm)
        r2 = (cq.Workplane("YZ").polyline([(p["back_y2"] - 1, -0.01), (17.0, -0.01), (15.0, 2.0), (p["back_y2"] - 1, 2.0)]).close()
              .extrude(60).translate((p["relief_halfw"] if sx > 0 else -p["relief_halfw"] - 60, 0, 0)))
        body = body.cut(r2)
    body = body.cut(teardrop_z(p["screw_clear"], p["floor"] + 1, -0.5))
    body = body.cut(teardrop_z(p["head_pocket"], H + 1, p["floor"]))
    hp = p["head_pocket"] / 2
    groove = (cq.Workplane("XY").workplane(offset=p["floor"])
              .polyline([(-hp, 0.5), (hp, 0.5), (hp - y0 + 1, y0 - 1), (-hp + y0 - 1, y0 - 1)]).close()
              .extrude(H + 1))
    # (v4.1) back groove NOT cut: channel stays closed -> screw driven from the jaw's far end
    for sx in (1, -1):
        body = body.cut(cq.Workplane("XY").center(sx * p["pin_x"], 0).circle(p["pin_d"] / 2)
                        .extrude(p["pin_depth"]).translate((0, 0, -0.01)))
    # --- TPU directional fin liner ---
    liner = fin_liner(p)
    return body, liner


if __name__ == "__main__":
    import os, trimesh, numpy as np
    out = sys.argv[1] if len(sys.argv) > 1 else "out6"
    os.makedirs(out, exist_ok=True)
    body, liner = build()
    cq.exporters.export(body, f"{out}/jaw_v6_PLA_body.step"); cq.exporters.export(liner, f"{out}/liner_v6_TPU_fins.step")
    cq.exporters.export(body, f"{out}/_body.stl", tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(liner, f"{out}/_liner.stl", tolerance=0.02, angularTolerance=0.1)
    th, mz, z0 = pose()
    bb = body.val().BoundingBox()
    print("theta=%.4f mount_z=%.2f z0=%.2f" % (th, mz, z0))
    print("ring local z: %.1f .. %.1f" % (local_z_of_tool_z(P['ring_t0']), local_z_of_tool_z(P['ring_t1'])))
    print("bbox", round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1), "vol cm3", round(body.val().Volume() / 1000, 1),
          "liner cm3", round(liner.val().Volume() / 1000, 2))
