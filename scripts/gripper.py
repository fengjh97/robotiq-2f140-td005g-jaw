"""Robotiq 2F-140 kinematic model (URDF parameters, Robotiq USD meshes, mm).
Gripper frame G: z = approach axis (towards fingertips), fingers close along y."""
import numpy as np, trimesh
U='usd/'   # Robotiq 2F-140 link meshes (STL, mm) converted from robotiq/isaacsim_assets (see README)
O1=np.array([-30.601,54.905]); O2=np.array([-12.7,61.42])
P1_0=np.array([-95.23,131.22])          # distal pivot at theta=0 (from URDF chain)
MOUNT_OFF=np.array([-84.1,144.0])-P1_0   # screw axis on mount face relative to P1
MESH={k:trimesh.load(U+k+'.stl') for k in ['base','outer_knuckle_left','outer_finger_left','inner_knuckle_left','inner_finger_left']}
def rotx(phi, cy, cz):
    T=trimesh.transformations.rotation_matrix(phi,[1,0,0],[0,cy,cz]); return T
def link_T(theta):
    """4x4 transforms of left links in G for opening angle theta (0=open, 0.7=closed)."""
    Rk=rotx(-theta,O1[0],O1[1]); Ri=rotx(-theta,O2[0],O2[1])
    p1=Rk[:3,:3]@np.array([0,P1_0[0],P1_0[1]])+Rk[:3,3]
    Td=np.eye(4); Td[1,3]=p1[1]-P1_0[0]; Td[2,3]=p1[2]-P1_0[1]
    return {'outer_knuckle_left':Rk,'outer_finger_left':Rk,'inner_knuckle_left':Ri,'inner_finger_left':Td}, Td
def mount_pose(theta):
    """screw-axis point on the mount face (left finger), in G (y,z)."""
    _,Td=link_T(theta); return np.array([-84.1+Td[1,3], 144.0+Td[2,3]])
def S_of(theta): return -mount_pose(theta)[0]
def theta_of_S(S):
    from scipy.optimize import brentq
    return brentq(lambda t: S_of(t)-S, 0.0, 0.75)
MIR=np.diag([1.,-1.,1.,1.]); MIR[1,1]=-1
def meshes(theta, include_base=True, distal=True):
    """list of (name, mesh) in G for both fingers."""
    Ts,_=link_T(theta); out=[]
    if include_base: out.append(('base',MESH['base']))
    for k,T in Ts.items():
        if k=='inner_finger_left' and not distal: continue
        m=MESH[k].copy(); m.apply_transform(T); out.append((k,m))
        r=m.copy(); r.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[0,0,1])); out.append((k.replace('left','right'),r))
    return out
if __name__=='__main__':
    for t in [0,0.2,0.35,0.5,0.7]: print(t, 'S=%.1f'%S_of(t), 'mount z=%.1f'%mount_pose(t)[1])
