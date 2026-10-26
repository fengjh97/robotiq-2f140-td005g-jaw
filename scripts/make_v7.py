import math, sys, cadquery as cq, trimesh, numpy as np, pymeshfix
sys.path.insert(0,'.')
import tool, jaw7
from jaw7 import local_z_of_tool_z
T0=dict(tool.T)
def fix(m):
    m.merge_vertices()
    if m.is_watertight: return m
    mf=pymeshfix.MeshFix(m.vertices,m.faces); mf.repair(); return trimesh.Trimesh(mf.points,mf.faces)
for tag,d in {'S':-0.6,'M':0.0,'L':+0.6}.items():
    for k in ('grip_d_top','grip_d_bot','grip_w_top','grip_w_bot'): tool.T[k]=T0[k]+2*d
    P=dict(jaw7.P); body,_=jaw7.build(P)
    # final body, print orientation (back face on bed)
    cq.exporters.export(body,'v7/_b.stl',tolerance=0.02,angularTolerance=0.1)
    B=fix(trimesh.load('v7/_b.stl')); R=trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]); B.apply_transform(R)
    B.apply_translation([-(B.bounds[0][0]+B.bounds[1][0])/2,-(B.bounds[0][1]+B.bounds[1][1])/2,-B.bounds[0][2]])
    B.export(f'v7/PRINT_jaw_v7_{tag}_PLA_x2.stl')
    if tag=='M': cq.exporters.export(body,'v7/jaw_v7_M_PLA_only.step')
    # trial slice: 9 mm through the ridge zone, ring only
    z0=local_z_of_tool_z(P["liner_t0"])+6; z1=z0+7
    ts=body.intersect(cq.Workplane("XY").box(200,200,z1-z0,centered=False).translate((-100,21,z0)))
    n={'S':1,'M':2,'L':3}[tag]
    for i in range(n):
        yc=44-3.5*i
        ts=ts.cut(cq.Workplane("YZ").polyline([(yc-1.2,z1+0.1),(yc+1.2,z1+0.1),(yc,z1-1.5)]).close().extrude(80).translate((-40,0,0)))
    cq.exporters.export(ts,'v7/_t.stl',tolerance=0.02,angularTolerance=0.1)
    t=fix(trimesh.load('v7/_t.stl')); t.apply_translation([-(t.bounds[0][0]+t.bounds[1][0])/2,-(t.bounds[0][1]+t.bounds[1][1])/2,-t.bounds[0][2]])
    t.export(f'v7/trial_v7_{tag}.stl')
    print(tag,'body',B.is_watertight,round(B.volume/1e3,1),'trial',t.is_watertight,t.extents.round(1))
tool.T.update(T0)
