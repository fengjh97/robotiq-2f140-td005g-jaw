import numpy as np, sys, time
from skfem import MeshTet, ElementVector, ElementTetP1, ElementTetP2, Basis, FacetBasis, asm, solve, condense, LinearForm, BilinearForm
from skfem.models.elasticity import linear_elasticity, lame_parameters
from skfem.helpers import dot
import scipy.sparse.linalg as spla
nodes=np.load('fea/nodes.npy'); elems=np.load('fea/elems.npy')
m=MeshTet(nodes.T.copy(), elems.T.copy())
E,nu=2680.0,0.35   # MPa (PETG-CF printed, conservative)
lam,mu=lame_parameters(E,nu)
order=sys.argv[1] if len(sys.argv)>1 else 'P1'
e=ElementVector(ElementTetP2() if order=='P2' else ElementTetP1())
ib=Basis(m,e)
K=asm(linear_elasticity(lam,mu),ib)
# --- boundary: mount patch on z=0 (bonded) ---
fc=m.facets; P=m.p
cent=P[:,fc].mean(axis=1)
bf=m.boundary_facets()
c=cent[:,bf]
mount=bf[(np.abs(c[2])<0.05)&(np.abs(c[0])<=8.1)&(c[1]>=-5.4)&(c[1]<=12.5)]
dofs=ib.get_dofs(mount).all()
# --- load surfaces: ring cavity (back half) ---
def facet_normals(fs):
    t=P[:,fc[:,fs]]
    n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0],axis=0); a=np.linalg.norm(n,axis=0); return n/a, a/2
nb,ab=facet_normals(bf)
# orient normals outward: compare with vector from element centroid
f2t=m.f2t[0,bf]; tc=P[:,m.t[:,f2t]].mean(axis=1)
sgn=np.sign(np.sum(nb*(c-tc),axis=0)); nb=nb*sgn
# cavity surface facets: outward normal of the solid points INTO the cavity (toward grip centre, +y-ish)
ring=(c[2]>66)&(c[2]<95)&(c[1]>18)&(c[1]<48.5)&(nb[1]>0.25)
rf=bf[ring]; print('ring load facets',ring.sum(),'area mm2',round(ab[ring].sum(),1))
def load_case(F):
    """F: total force vector (N) applied uniformly over the ring cavity facets (traction)."""
    A=ab[ring].sum(); tr=np.array(F)/A
    fb=FacetBasis(m,e,facets=rf)
    @LinearForm
    def lf(v,w): return tr[0]*v[0]+tr[1]*v[1]+tr[2]*v[2]
    return asm(lf,fb)
cases={'LC1 grip 125N (-Y) [reference]':[0,-125,0],'LC1b grip 30N (-Y)':[0,-30,0],
       'LC2 hang 3g 22N (+Z) + grip 30N':[0,-30,22],'LC3 lateral 30N (X) + grip 30N':[30,-30,0],'LC4 wedge spread 35N + hang 22N':[0,-35,22]}
def stresses(u):
    from skfem.helpers import sym_grad
    # element-wise stress at centroid (P1: constant) using P1 projection
    ibp=Basis(m,ElementVector(ElementTetP1())) if order=='P2' else ib
    up=ibp.project(ib.interpolate(u)) if order=='P2' else u
    U=up.reshape(-1,3) if False else None
    # compute gradient per element from nodal P1 displacements
    nd=ib.nodal_dofs; ux=up[nd[0]]; uy=up[nd[1]]; uz=up[nd[2]]
    X=P[:,m.t]  # 3x4xne
    ne=m.t.shape[1]
    Mmat=np.ones((ne,4,4)); Mmat[:,:,1:]=np.transpose(X,(2,1,0))
    Minv=np.linalg.inv(Mmat)            # rows: coeffs for (1,x,y,z)
    G=Minv[:,1:,:]                      # ne x 3 x 4 : d(shape)/dx_j
    Ue=np.stack([ux[m.t],uy[m.t],uz[m.t]],axis=0)  # 3 x 4 x ne
    grad=np.einsum('ike,ejk->eij',Ue,G)
    eps=0.5*(grad+np.transpose(grad,(0,2,1)))
    tr=np.trace(eps,axis1=1,axis2=2)
    sig=2*mu*eps+lam*tr[:,None,None]*np.eye(3)
    s=sig
    vm=np.sqrt(0.5*((s[:,0,0]-s[:,1,1])**2+(s[:,1,1]-s[:,2,2])**2+(s[:,2,2]-s[:,0,0])**2)+3*(s[:,0,1]**2+s[:,1,2]**2+s[:,0,2]**2))
    return sig,vm
res={}
for name,F in cases.items():
    t0=time.time()
    f=load_case(F)
    u=solve(*condense(K,f,D=dofs))
    sig,vm=stresses(u)
    nd=ib.nodal_dofs; disp=np.linalg.norm(np.stack([u[nd[0]],u[nd[1]],u[nd[2]]]),axis=0)
    ec=P[:,m.t].mean(axis=1)
    # exclude elements touching the fixed patch edges (singular corners) for reporting: z>1.5
    ok=ec[2]>1.5
    syy=sig[:,1,1]; szz=sig[:,2,2]
    i=np.argmax(vm*ok); j=np.argmax(syy*ok)
    pctl=lambda a: np.percentile(a[ok],99.9)
    print(f'{name}: max|u|={disp.max():.3f} mm  VM max={vm[ok].max():.2f} (99.9%={pctl(vm):.2f}) MPa at {ec[:,i].round(1)}  '
          f'sigma_yy(cross-layer) max tension={syy[ok].max():.2f} MPa at {ec[:,j].round(1)}  sigma_zz max={szz[ok].max():.2f}  [{time.time()-t0:.0f}s]')
    res[name]=dict(u=u,vm=vm,syy=syy)
    np.save(f'fea/vm_{len(res)}.npy',vm); np.save(f'fea/syy_{len(res)}.npy',syy); np.save(f'fea/u_{len(res)}.npy',u)
# reaction moment at the mount for LC1 (about X axis through the mount face centre)
