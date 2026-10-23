import numpy as np, trimesh, math, fcl
from gripper import meshes, mount_pose, S_of
from jaw6 import P, pose
th_g, mz_g, z0 = pose(); O='out6/'
J=trimesh.load(O+'_body.stl'); tool=trimesh.load('TD005G_model.stl')
def bvh(m):
    b=fcl.BVHModel(); b.beginModel(len(m.vertices),len(m.faces)); b.addSubModel(m.vertices.astype(float),m.faces.astype(np.int32)); b.endModel(); return b
JB=bvh(J); TB=bvh(tool)
Rz=np.array([[-1,0,0],[0,-1,0],[0,0,1.]])
def jaw_objs(th):
    S=S_of(th); mz=mount_pose(th)[1]
    a=fcl.CollisionObject(JB,fcl.Transform(np.eye(3),[0,-S,mz]))
    b=fcl.CollisionObject(JB,fcl.Transform(Rz,Rz@np.array([0,-S,mz])))
    return a,b
def tool_obj(dz=0,dx=0,dbeta=0):
    R=trimesh.transformations.rotation_matrix(math.radians(P['beta']+dbeta),[0,1,0])
    return fcl.CollisionObject(TB,fcl.Transform(R[:3,:3],[P['x0']+dx,0,z0+dz]))
def dist(o1,o2):
    r=fcl.DistanceResult(); return fcl.distance(o1,o2,fcl.DistanceRequest(),r)
LB={}
def links(th):
    return [(n,fcl.CollisionObject(bvh(m),fcl.Transform())) for n,m in meshes(th) if n!='base']
a,b=jaw_objs(th_g)
print('GRASP: jawA-tool %.2f  jawB-tool %.2f  jawA-jawB %.2f'%(dist(a,tool_obj()),dist(b,tool_obj()),dist(a,b)))
print('--- closing sweep (jaw-tool min clearance, mm) / jaw-links ---')
for th in np.linspace(0,th_g,9):
    a,b=jaw_objs(th)
    s=' '.join('dz%+d:%.1f'%(dz,min(dist(a,tool_obj(dz)),dist(b,tool_obj(dz)))) for dz in (-3,0,3))
    lk=min(min(dist(a,o),dist(b,o)) for n,o in links(th))
    print('theta=%.3f S=%5.1f  %s   jaw-links %.1f'%(th,S_of(th),s,lk))
for dx in (-3,3):
    for db in (-4,4):
        a,b=jaw_objs(th_g); print('grasp dx=%+d dbeta=%+d: %.2f %.2f'%(dx,db,dist(a,tool_obj(0,dx,db)),dist(b,tool_obj(0,dx,db))))
print('--- descent at full open ---')
a,b=jaw_objs(0.0)
for dz in (150,80,40,20,10,0,-3):
    print('dz %4d  jaw-tool %.1f'%(dz,min(dist(a,tool_obj(dz)),dist(b,tool_obj(dz)))))
