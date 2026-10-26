import math, sys, cadquery as cq, trimesh, pymeshfix
sys.path.insert(0,'.')
import tool, jaw7
T0=dict(tool.T); d=+1.8   # radial vs M  (L = +0.6, XXL = L + 1.2)
for k in ('grip_d_top','grip_d_bot','grip_w_top','grip_w_bot'): tool.T[k]=T0[k]+2*d
body,_=jaw7.build(dict(jaw7.P))
print('valid',body.val().isValid())
cq.exporters.export(body,'v7/jaw_v7_XXL_PLA_only.step')
cq.exporters.export(body,'v7/_b.stl',tolerance=0.02,angularTolerance=0.1)
m=trimesh.load('v7/_b.stl'); m.merge_vertices()
if not m.is_watertight:
    mf=pymeshfix.MeshFix(m.vertices,m.faces); mf.repair(); m=trimesh.Trimesh(mf.points,mf.faces)
m.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
m.apply_translation([-(m.bounds[0][0]+m.bounds[1][0])/2,-(m.bounds[0][1]+m.bounds[1][1])/2,-m.bounds[0][2]])
m.export('v7/PRINT_jaw_v7_XXL_PLA_x2.stl'); print('watertight',m.is_watertight,'vol',round(m.volume/1e3,1),'extents',m.extents.round(1))
tool.T.update(T0)
