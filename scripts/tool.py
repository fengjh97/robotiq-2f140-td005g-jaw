"""Approximate Makita TD005G (from side-photo measurements).
Tool frame: origin = grip axis at head underside, X forward (bit), Z DOWN, Y left-right."""
import cadquery as cq, math
T=dict(head_h=66.0, head_w=62.0, head_back=34.0, head_front=54.0, grip_tilt=9.0,
       grip_d_top=46.0, grip_d_bot=38.0, grip_w_top=36.0, grip_w_bot=33.0, grip_len=96.0,
       trig_z0=3.0, trig_z1=29.0, trig_protrude=16.0, trig_half_w=7.0)
def grip_axis_x(z, t=T): return -math.tan(math.radians(t['grip_tilt']))*z
def grip_dims(z, t=T):
    f=min(max(z/t['grip_len'],0),1)
    return t['grip_d_top']+(t['grip_d_bot']-t['grip_d_top'])*f, t['grip_w_top']+(t['grip_w_bot']-t['grip_w_top'])*f
def build(t=T):
    hh,hw=t['head_h'],t['head_w']
    head=(cq.Workplane("YZ").center(0,-hh/2).ellipse(hw/2,hh/2).extrude(t['head_back']+t['head_front'])
          .translate((-t['head_back'],0,0)))
    nose=cq.Workplane("YZ").center(0,-hh*0.55).circle(16).extrude(14).translate((t['head_front'],0,0))
    bit=cq.Workplane("YZ").center(0,-hh*0.55).polygon(6,7.3).extrude(32).translate((t['head_front']+14,0,0))
    # grip: lofted ellipses following the tilted axis (sections are horizontal)
    zs=[-10,0,20,40,60,80,t['grip_len']]
    w=cq.Workplane("XY")
    secs=[]
    for z in zs:
        d,wd=grip_dims(z,t)
        secs.append(cq.Workplane("XY").workplane(offset=z).center(grip_axis_x(z,t),0).ellipse(d/2,wd/2).val())
    grip=cq.Workplane("XY").add(cq.Solid.makeLoft([cq.Wire.assembleEdges(s.Edges()) if hasattr(s,'Edges') else s for s in secs],True))
    d0,_=grip_dims(10,t)
    trig=(cq.Workplane("XY").box(t['trig_protrude']+6,2*t['trig_half_w'],t['trig_z1']-t['trig_z0'],centered=False)
          .translate((d0/2-6,-t['trig_half_w'],t['trig_z0'])))
    foot=cq.Workplane("XY").box(112,82,18).edges("|Z").fillet(6).translate((-10,0,t['grip_len']+4))
    batt=cq.Workplane("XY").box(116,86,70).edges("|Z").fillet(8).translate((-8,0,t['grip_len']+48))
    return head.union(nose).union(bit).union(grip).union(trig).union(foot).union(batt)
if __name__=='__main__':
    s=build(); cq.exporters.export(s,'TD005G_model.stl',tolerance=0.05,angularTolerance=0.2); cq.exporters.export(s,'TD005G_model.step')
    import trimesh; m=trimesh.load('TD005G_model.stl'); print(m.bounds.round(1).tolist(), m.is_watertight)
