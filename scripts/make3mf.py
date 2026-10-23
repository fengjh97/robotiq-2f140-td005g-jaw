import trimesh, numpy as np, zipfile, uuid, json, re, sys, io
K='/tmp/claude-0/-home-claude/27335561-5a03-5cc1-9d07-f0eace076c34/scratchpad/kin/out6/'
ORCA='/tmp/claude-0/-home-claude/27335561-5a03-5cc1-9d07-f0eace076c34/scratchpad/slicer/job/out_x/x/'
liner_extruder = sys.argv[1] if len(sys.argv)>1 else '2'
out = sys.argv[2] if len(sys.argv)>2 else 'jaw_v6_onepiece_H2DPro.3mf'
MODE=sys.argv[3] if len(sys.argv)>3 else 'jaws'
if MODE=='jaws':
    body=trimesh.load(K+'CP_body_PLA.stl'); liner=trimesh.load(K+'CP_liner_TPU.stl')
    root=trimesh.creation.box(extents=[66,26.5,66]); root.apply_translation([0,50-26.5/2+0.5,31])   # print-Y 24..51 = mount end
    parts=[('jaw_body_PLA',body,'normal_part','1',{}),
           ('liner_TPU_fins',liner,'normal_part',liner_extruder,{}),
           ('root_100pct',root,'modifier_part',None,{'sparse_infill_density':'100%'})]
    objects=[('jaw_A',(175-40,160),parts),('jaw_B',(175+40,160),parts)]
    OBJ_CFG={'wall_loops':'5','sparse_infill_density':'20%','top_shell_layers':'6','bottom_shell_layers':'6'}
else:
    TR='/tmp/claude-0/-home-claude/27335561-5a03-5cc1-9d07-f0eace076c34/scratchpad/kin/trial/'
    objects=[]
    for ci,tag in enumerate(('S','M','L')):
        if MODE=='trial_pla':
            b=trimesh.load(TR+f'{tag}_body.stl'); pp=[(f'ring_{tag}_PLA',b,'normal_part','1',{})]
            for ri in range(2): objects.append((f'ring_{tag}_{ri+1}',(175+(ci-1)*72,140+ri*36),pp))
        else:
            l=trimesh.load(TR+f'{tag}_liner.stl'); l.apply_translation(-np.array([(l.bounds[0][0]+l.bounds[1][0])/2,(l.bounds[0][1]+l.bounds[1][1])/2,0]))
            pp=[(f'liner_{tag}_TPU',l,'normal_part','2',{})]
            for ri in range(2): objects.append((f'liner_{tag}_{ri+1}',(175+(ci-1)*65,135+ri*35),pp))
    OBJ_CFG={'wall_loops':'3','sparse_infill_density':'15%','top_shell_layers':'4','bottom_shell_layers':'4'} if MODE=='trial_pla' else {'wall_loops':'3','sparse_infill_density':'100%'}
U=lambda: str(uuid.uuid4())
HDR='<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
def mesh_xml(oid,m):
    v=''.join(f'<vertex x="{a:.5f}" y="{b:.5f}" z="{c:.5f}"/>' for a,b,c in m.vertices)
    t=''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in m.faces)
    return f'  <object id="{oid}" p:UUID="{U()}" type="model">\n   <mesh>\n    <vertices>{v}</vertices>\n    <triangles>{t}</triangles>\n   </mesh>\n  </object>\n'
files={}
main_objs=[]; items=[]; ms_objs=[]; rels=[]
nid=1
for oi,(oname,(bx,by),parts) in enumerate(objects):
    path=f'/3D/Objects/object_{oi+1}.model'
    sub=''; comps=''; ms_parts=''
    for pname,m,subtype,ext,extra in parts:
        pid=nid; nid+=1
        sub+=mesh_xml(pid,m)
        comps+=f'    <component p:path="{path}" objectid="{pid}" p:UUID="{U()}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>\n'
        md=f'      <metadata key="name" value="{pname}"/>\n      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
        if ext: md+=f'      <metadata key="extruder" value="{ext}"/>\n'
        for k,v in extra.items(): md+=f'      <metadata key="{k}" value="{v}"/>\n'
        ms_parts+=f'    <part id="{pid}" subtype="{subtype}">\n{md}      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>\n    </part>\n'
    files[path[1:]]=HDR+' <resources>\n'+sub+' </resources>\n <build/>\n</model>\n'
    rels.append(path)
    mid=nid; nid+=1
    main_objs.append(f'  <object id="{mid}" p:UUID="{U()}" type="model">\n   <components>\n{comps}   </components>\n  </object>\n')
    items.append(f'  <item objectid="{mid}" p:UUID="{U()}" transform="1 0 0 0 1 0 0 0 1 {bx} {by} 0" printable="1"/>\n')
    cfg=''.join(f'    <metadata key="{k}" value="{v}"/>\n' for k,v in OBJ_CFG.items())
    ms_objs.append(f'  <object id="{mid}">\n    <metadata key="name" value="{oname}"/>\n    <metadata key="extruder" value="1"/>\n'+cfg+'    <metadata key="sparse_infill_pattern" value="gyroid"/>\n'+ms_parts+'  </object>\n')
main=HDR.replace(' <metadata name="BambuStudio:3mfVersion">1</metadata>\n',' <metadata name="Application">BambuStudio-02.06.00.51</metadata>\n <metadata name="OrcaSlicer">2.4.2</metadata>\n <metadata name="BambuStudio:3mfVersion">1</metadata>\n <metadata name="Title">Robotiq 2F-140 TD005G ring jaw v6</metadata>\n')
main+=' <resources>\n'+''.join(main_objs)+' </resources>\n <build p:UUID="'+U()+'">\n'+''.join(items)+' </build>\n</model>\n'
files['3D/3dmodel.model']=main
files['3D/_rels/3dmodel.model.rels']='<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'+''.join(f' <Relationship Target="{p}" Id="rel-{i+1}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n' for i,p in enumerate(rels))+'</Relationships>\n'
files['Metadata/model_settings.config']='<?xml version="1.0" encoding="UTF-8"?>\n<config>\n'+''.join(ms_objs)+'  <plate>\n    <metadata key="plater_id" value="1"/>\n    <metadata key="plater_name" value="jaws_onepiece"/>\n    <metadata key="locked" value="false"/>\n    <metadata key="filament_map_mode" value="Manual"/>\n'+'  </plate>\n  <assemble>\n  </assemble>\n</config>\n'
# project settings from the Orca export, with presets names set to Bambu system presets and manual filament map (PLA->right, TPU->left)
ps=json.load(open(ORCA+'Metadata/project_settings.config'))
ps['print_settings_id']='0.20mm Standard @BBL H2DP'
ps['different_settings_to_system']=['bottom_shell_layers;enable_prime_tower;enable_support;sparse_infill_density;sparse_infill_pattern;top_shell_layers;wall_loops','','','']
ps['inherits_group']=['','','','']
ps['filament_settings_id']=['Bambu PLA Basic @BBL H2DP','Bambu TPU 95A HF @BBL H2DP']
ps['printer_settings_id']='Bambu Lab H2D Pro 0.4 nozzle'
ps['filament_map_mode']='Manual'; ps['filament_map']=['1','2']
ps['enable_prime_tower']='1' if MODE=='jaws' else '0'
ps['wipe_tower_x']=['145']; ps['wipe_tower_y']=['240']
for k,v in list(ps.items()):
    if isinstance(v,list) and len(v)==1 and (k.startswith('filament') or k=='default_filament_colour'):
        ps[k]=v*2
ps['filament_colour']=['#F0F0F0','#F2754E']; ps['default_filament_colour']=['','']
ps['wall_loops']='5'; ps['sparse_infill_density']='20%'; ps['sparse_infill_pattern']='gyroid'; ps['top_shell_layers']='6'; ps['bottom_shell_layers']='6'; ps['enable_support']='0'
files['Metadata/project_settings.config']=json.dumps(ps,indent=4)
for f in ('[Content_Types].xml','_rels/.rels','Metadata/slice_info.config','Metadata/filament_sequence.json'):
    files[f]=open(ORCA+f).read()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for k in ['[Content_Types].xml','_rels/.rels','3D/3dmodel.model','3D/_rels/3dmodel.model.rels']+[k for k in files if k.startswith('3D/Objects')]+['Metadata/project_settings.config','Metadata/model_settings.config','Metadata/slice_info.config','Metadata/filament_sequence.json']:
        z.writestr(k,files[k])
print('wrote',out)
