"""Fit-trial pieces: 3 size variants (S/M/L) x 2 ring halves, PLA body slice + fused TPU fin liner slice."""
import math, sys, copy, cadquery as cq, trimesh, numpy as np, pymeshfix
sys.path.insert(0,'.')
import tool, jaw6
from jaw6 import P as P0, local_z_of_tool_z
H_SLICE=8.0
import os
variants={'S':-0.6,'M':0.0,'L':+0.6}     # radial change of the assumed grip size (mm)
T0=dict(tool.T)
out={}
for tag,d in variants.items():
    for k in ('grip_d_top','grip_d_bot','grip_w_top','grip_w_bot'):
        tool.T[k]=T0[k]+2*d
    P=dict(P0); P['pocket_clear']=0.15   # separate TPU liner, snap-in
    body,liner=jaw6.build(P)
    z0=local_z_of_tool_z(P['liner_t0'])+6; z1=z0+H_SLICE
    bs=body.intersect(cq.Workplane("XY").box(200,200,z1-z0,centered=False).translate((-100,21,z0)))
    ls=liner.intersect(cq.Workplane("XY").box(200,200,z1-z0,centered=False).translate((-100,-100,z0)))
    # size marks: 1/2/3 small V notches on the outer side face (x = +half_w)
    n={'S':1,'M':2,'L':3}[tag]
    for i in range(n):
        yc=44-3.5*i
        notch=(cq.Workplane("YZ").polyline([(yc-1.2,z1+0.1),(yc+1.2,z1+0.1),(yc,z1-1.5)]).close().extrude(80).translate((-40,0,0)))
        bs=bs.cut(notch)
    lb=ls.val().BoundingBox()
    for i in range(n):
        xc=-3+3*i
        ln=(cq.Workplane("XZ").polyline([(xc-0.9,z1+0.1),(xc+0.9,z1+0.1),(xc,z1-1.2)]).close().extrude(-200).translate((0,-100,0)))
        ls=ls.cut(ln)
    for nm,s in (('body',bs),('liner',ls)):
        cq.exporters.export(s,f'trial/_{tag}_{nm}.stl',tolerance=0.01 if nm=='liner' else 0.02,angularTolerance=0.1)
        m=trimesh.load(f'trial/_{tag}_{nm}.stl'); m.merge_vertices()
        if not m.is_watertight:
            mf=pymeshfix.MeshFix(m.vertices,m.faces); mf.repair(); m=trimesh.Trimesh(mf.points,mf.faces)
        out[(tag,nm)]=m
    print(tag,'z',round(z0,1),round(z1,1),'body vol',round(out[(tag,'body')].volume/1e3,1),'liner vol',round(out[(tag,'liner')].volume/1e3,2))
tool.T.update(T0)
# common frame per piece: shift so that body min corner at origin-ish, keep body+liner together
for tag in variants:
    b=out[(tag,'body')]; l=out[(tag,'liner')]
    sh=-np.array([(b.bounds[0][0]+b.bounds[1][0])/2,(b.bounds[0][1]+b.bounds[1][1])/2,b.bounds[0][2]])
    b.apply_translation(sh); l.apply_translation(sh)
    b.export(f'trial/{tag}_body.stl')
    l.apply_translation(-l.bounds[0]); l.export(f'trial/{tag}_liner.stl')
    print(tag,'piece extents',b.extents.round(1))
