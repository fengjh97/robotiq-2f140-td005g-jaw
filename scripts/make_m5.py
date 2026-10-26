import math, sys, numpy as np, cadquery as cq, trimesh, pymeshfix
sys.path.insert(0,'.')
import tool, jaw7
from jaw7 import local_z_of_tool_z
T0=dict(tool.T); d=+2.5            # radial vs M  -> inner diameter +5 mm
for k in ('grip_d_top','grip_d_bot','grip_w_top','grip_w_bot'): tool.T[k]=T0[k]+2*d
P=dict(jaw7.P); P['half_w']=34.0     # wider jaw so the ring tips keep thick walls
body,_=jaw7.build(P)
print('valid',body.val().isValid())
cq.exporters.export(body,'v7/jaw_v7_Mplus5mm_PLA_only.step')
cq.exporters.export(body,'v7/_b.stl',tolerance=0.02,angularTolerance=0.1)
m=trimesh.load('v7/_b.stl'); m.merge_vertices()
if not m.is_watertight:
    mf=pymeshfix.MeshFix(m.vertices,m.faces); mf.repair(); m=trimesh.Trimesh(mf.points,mf.faces)
# wall check near the ring tips (local frame, before re-orienting)
z=local_z_of_tool_z(48); S=P['S']
for dy in (0.3,1.5,2.6):
    loc,_,_=m.ray.intersects_location([[-80,S-dy,z]],[[1,0,0]]); xs=np.sort(loc[:,0])
    print('  y=S-%.1f material widths:'%dy,[round(xs[i+1]-xs[i],1) for i in range(0,len(xs)-1,2)])
m.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
m.apply_translation([-(m.bounds[0][0]+m.bounds[1][0])/2,-(m.bounds[0][1]+m.bounds[1][1])/2,-m.bounds[0][2]])
m.export('v7/PRINT_jaw_v7_Mplus5mm_PLA_x2.stl'); print('watertight',m.is_watertight,'vol',round(m.volume/1e3,1),'extents',m.extents.round(1))
tool.T.update(T0)
