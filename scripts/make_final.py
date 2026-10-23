import math, sys, cadquery as cq, trimesh, numpy as np, pymeshfix
sys.path.insert(0,'.')
import tool, jaw6
T0=dict(tool.T)
def fix(m):
    m.merge_vertices()
    if m.is_watertight: return m
    mf=pymeshfix.MeshFix(m.vertices,m.faces); mf.repair(); return trimesh.Trimesh(mf.points,mf.faces)
for tag,d in {'S':-0.6,'M':0.0,'L':+0.6}.items():
    for k in ('grip_d_top','grip_d_bot','grip_w_top','grip_w_bot'): tool.T[k]=T0[k]+2*d
    for clear,suffix in ((0.0,'CP'),(0.15,'SEP')):
        P=dict(jaw6.P); P['pocket_clear']=clear
        body,liner=jaw6.build(P)
        cq.exporters.export(body,f'final_sml/_b.stl',tolerance=0.02,angularTolerance=0.1)
        cq.exporters.export(liner,f'final_sml/_l.stl',tolerance=0.01,angularTolerance=0.1)
        B=fix(trimesh.load('final_sml/_b.stl')); L=fix(trimesh.load('final_sml/_l.stl'))
        R=trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]); B.apply_transform(R); L.apply_transform(R)
        sh=[-(B.bounds[0][0]+B.bounds[1][0])/2,-(B.bounds[0][1]+B.bounds[1][1])/2,-B.bounds[0][2]]
        B.apply_translation(sh); L.apply_translation(sh)
        if suffix=='CP':
            B.export(f'final_sml/{tag}_CP_body.stl'); L.export(f'final_sml/{tag}_CP_liner.stl')
        else:
            B.export(f'final_sml/PRINT_jaw_{tag}_PLA_body_x2.stl')
            # separate liner: flat ends on bed (undo 9 deg)
            l=fix(trimesh.load('final_sml/_l.stl')); best=None
            for s in (1,-1):
                m=l.copy(); m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(s*9.0),[0,1,0]))
                k=np.sum(m.vertices[:,2]<m.vertices[:,2].min()+0.05)
                if best is None or k>best[0]: best=(k,m)
            m=best[1]; m.apply_translation(-m.bounds[0]); m.export(f'final_sml/PRINT_liner_{tag}_TPU_x2.stl')
        print(tag,suffix,'body',B.is_watertight,round(B.volume/1e3,1),'liner',round(L.volume/1e3,2))
    tool.T.update(T0)
