import numpy as np, trimesh, fcl, math, json, sys
from gripper import meshes, mount_pose, S_of, theta_of_S
from tool import T as TP, grip_axis_x
tool=trimesh.load('TD005G_model.stl')
def bvh(m):
    b=fcl.BVHModel(); b.beginModel(len(m.vertices),len(m.faces)); b.addSubModel(m.vertices.astype(float),m.faces.astype(np.int32)); b.endModel(); return b
tool_bvh=bvh(tool)
def tool_tf(x0,z0,beta):
    """tool frame -> G. beta: rotate tool about Y (deg) around the tool origin, then translate."""
    R=trimesh.transformations.rotation_matrix(math.radians(beta),[0,1,0])
    R[:3,3]=[x0,0,z0]; return R
def min_dist(gms, Tt):
    to=fcl.CollisionObject(tool_bvh, fcl.Transform(Tt[:3,:3],Tt[:3,3]))
    best=1e9; who=None
    for n,(o) in gms:
        req=fcl.DistanceRequest(); res=fcl.DistanceResult()
        d=fcl.distance(o,to,req,res)
        if d<best: best,who=d,n
    return best,who
cache={}
def gripper_objs(theta):
    k=round(theta,4)
    if k not in cache:
        cache[k]=[(n,fcl.CollisionObject(bvh(m),fcl.Transform())) for n,m in meshes(theta)]
    return cache[k]
def max_rise(theta,beta,x0,margin=3.0):
    """smallest z0 (tool origin z in G => head as high as possible) with clearance>=margin."""
    g=gripper_objs(theta)
    lo,hi=0.0,400.0   # lo: deep inside (collide), hi: far away
    d,_=min_dist(g,tool_tf(x0,hi,beta))
    if d<margin: return None,None
    for _ in range(22):
        mid=(lo+hi)/2; d,who=min_dist(g,tool_tf(x0,mid,beta))
        if d>=margin: hi=mid
        else: lo=mid
    d,who=min_dist(g,tool_tf(x0,hi-0.3,beta))
    return hi,who
if __name__=='__main__':
    rows=[]
    for S in [44,47,50,53,56,60]:
        th=theta_of_S(S); mz=mount_pose(th)[1]
        for beta in [0,5,9,13]:
            for x0 in [-10,0,10]:
                z0,who=max_rise(th,beta,x0)
                if z0 is None: continue
                head_top=z0-TP['head_h']            # G z of head top (approx, beta small)
                rise=mz-head_top                     # head top above the mount face
                # deepest grip point (tool z along axis) reachable with a 100 mm jaw:
                reach=(mz+100)-z0
                rows.append(dict(S=S,beta=beta,x0=x0,mount_z=round(mz,1),z0=round(z0,1),rise=round(rise,1),
                                 reach_tool_z=round(reach,1),limit=who))
                print(rows[-1]); sys.stdout.flush()
    json.dump(rows,open('search.json','w'),indent=1)
