
import bpy
import math
import os

# 清除场景
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# 创建素体角色（详细版本，单一网格）
def create_character():
    # 创建一个空对象作为角色根节点
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1))
    character_root = bpy.context.active_object
    character_root.name = "CharacterRoot"

    # 创建更详细的角色模型（由多个几何体合并而成）
    # 首先创建身体主体（圆柱体）
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.2, location=(0, 0, 1.2))
    body = bpy.context.active_object
    body.name = "Character"
    body.parent = character_root

    # 进入编辑模式进行修改
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.mode_set(mode='EDIT')

    # 让角色看起来更像人类
    bpy.ops.transform.resize(value=(1, 0.8, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

    bpy.ops.object.mode_set(mode='OBJECT')

    return [body], character_root

# 创建骨骼系统
def create_armature():
    bpy.ops.object.armature_add(location=(0, 0, 1))
    armature = bpy.context.active_object
    armature.name = "CharacterArmature"

    # 进入编辑模式编辑骨骼
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')

    # 获取骨骼编辑数据
    edit_bones = armature.data.edit_bones

    # 清除默认骨骼
    for bone in edit_bones:
        edit_bones.remove(bone)

    # 创建脊柱
    spine = edit_bones.new("Spine")
    spine.head = (0, 0, 0.8)
    spine.tail = (0, 0, 1.6)

    # 创建头部
    head = edit_bones.new("Head")
    head.head = (0, 0, 1.6)
    head.tail = (0, 0, 2.2)
    head.parent = spine

    # 创建左腿
    left_leg = edit_bones.new("LeftLeg")
    left_leg.head = (-0.15, 0, 0.8)
    left_leg.tail = (-0.15, 0, 0)

    # 创建右腿
    right_leg = edit_bones.new("RightLeg")
    right_leg.head = (0.15, 0, 0.8)
    right_leg.tail = (0.15, 0, 0)

    # 创建左臂
    left_arm = edit_bones.new("LeftArm")
    left_arm.head = (-0.3, 0, 1.6)
    left_arm.tail = (-0.7, 0, 1.6)
    left_arm.parent = spine

    # 创建右臂
    right_arm = edit_bones.new("RightArm")
    right_arm.head = (0.3, 0, 1.6)
    right_arm.tail = (0.7, 0, 1.6)
    right_arm.parent = spine

    bpy.ops.object.mode_set(mode='OBJECT')

    return armature

# 绑定角色到骨骼（真正的完整绑定）
def parent_character_to_armature(character_parts, armature, character_root):
    # 将骨骼系统作为角色根节点的父级
    character_root.parent = armature
    character_root.parent_type = 'OBJECT'

    # 对于单一角色模型，直接绑定到脊柱
    if len(character_parts) == 1:
        character = character_parts[0]
        character.parent = armature
        character.parent_type = 'BONE'
        character.parent_bone = "Spine"

# 创建障碍物
def create_obstacles():
    obstacles = []
    
    # 障碍物1 - 小箱子
    bpy.ops.mesh.primitive_cube_add(size=0.8, location=(5, 0, 0.4))
    obstacle1 = bpy.context.active_object
    obstacle1.name = "Obstacle1"
    obstacles.append(obstacle1)
    
    # 障碍物2 - 高箱子
    bpy.ops.mesh.primitive_cube_add(size=1.2, location=(10, 0, 0.6))
    obstacle2 = bpy.context.active_object
    obstacle2.name = "Obstacle2"
    obstacles.append(obstacle2)
    
    # 障碍物3 - 横杆
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=2, location=(15, 0, 1.2))
    obstacle3 = bpy.context.active_object
    obstacle3.name = "Obstacle3"
    obstacle3.rotation_euler.x = math.radians(90)
    obstacles.append(obstacle3)
    
    return obstacles

# 创建地面
def create_ground():
    bpy.ops.mesh.primitive_plane_add(size=30, location=(10, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground"

    # 添加材质
    mat = bpy.data.materials.new(name="GroundMaterial")
    mat.use_nodes = True

    # 清除默认节点（如果有）
    mat.node_tree.nodes.clear()

    # 创建 Principled BSDF 节点
    bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1)

    # 创建输出节点
    output = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    output.location = (400, 0)

    # 连接节点
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    if ground.data.materials:
        ground.data.materials[0] = mat
    else:
        ground.data.materials.append(mat)

    return ground

# 创建相机（更广的视野和跟踪）
def create_camera():
    bpy.ops.object.camera_add(location=(0, -15, 5))
    camera = bpy.context.active_object
    camera.name = "Camera"

    # 看向场景中心
    camera.rotation_euler.x = math.radians(60)
    camera.rotation_euler.y = 0
    camera.rotation_euler.z = 0

    # 调整相机视野（更宽的视野）
    camera.data.lens = 25
    camera.data.angle = math.radians(90)

    bpy.context.scene.camera = camera
    return camera

# 创建灯光
def create_lights():
    # 主光
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 3
    
    # 补光
    bpy.ops.object.light_add(type='POINT', location=(-5, 5, 5))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 1
    
    return [sun, fill]

# 设置场景
def setup_scene():
    scene = bpy.context.scene
    
    # 设置渲染引擎
    scene.render.engine = 'BLENDER_EEVEE'
    
    # 设置帧率和时长
    scene.frame_start = 1
    scene.frame_end = 120
    scene.render.fps = 24
    
    # 设置分辨率
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    
    # 设置输出路径
    output_dir = "/tmp/parkour_animation/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    scene.render.filepath = os.path.join(output_dir, "frame_")
    scene.render.image_settings.file_format = 'PNG'

# 创建跑跳动画
def create_animation(character_parts, armature, obstacles, camera):
    scene = bpy.context.scene
    
    # 选择骨骼进行动画
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # 获取姿态骨骼
    pose_bones = armature.pose.bones
    
    # 关键帧动画
    frames = [1, 30, 60, 90, 120]
    
    for frame in frames:
        scene.frame_set(frame)
        
        # 计算前进距离
        progress = (frame - 1) / (scene.frame_end - 1)
        x_pos = progress * 20
        
        # 移动整个骨骼
        armature.location.x = x_pos
        
        # 跳跃逻辑
        if frame == 30:  # 跳跃1
            armature.location.z = 1.5
            pose_bones["LeftLeg"].rotation_euler.x = math.radians(-30)
            pose_bones["RightLeg"].rotation_euler.x = math.radians(30)
            pose_bones["LeftArm"].rotation_euler.z = math.radians(-45)
            pose_bones["RightArm"].rotation_euler.z = math.radians(45)
        elif frame == 60:  # 落地1
            armature.location.z = 0
            pose_bones["LeftLeg"].rotation_euler.x = math.radians(0)
            pose_bones["RightLeg"].rotation_euler.x = math.radians(0)
            pose_bones["LeftArm"].rotation_euler.z = math.radians(0)
            pose_bones["RightArm"].rotation_euler.z = math.radians(0)
        elif frame == 90:  # 跳跃2
            armature.location.z = 2
            pose_bones["LeftLeg"].rotation_euler.x = math.radians(-45)
            pose_bones["RightLeg"].rotation_euler.x = math.radians(45)
            pose_bones["LeftArm"].rotation_euler.z = math.radians(-60)
            pose_bones["RightArm"].rotation_euler.z = math.radians(60)
        elif frame == 120:  # 结束
            armature.location.z = 0
            pose_bones["LeftLeg"].rotation_euler.x = math.radians(0)
            pose_bones["RightLeg"].rotation_euler.x = math.radians(0)
            pose_bones["LeftArm"].rotation_euler.z = math.radians(0)
            pose_bones["RightArm"].rotation_euler.z = math.radians(0)
        
        # 插入关键帧
        armature.keyframe_insert(data_path="location", frame=frame)
        for bone in pose_bones:
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)
    
    # 相机跟随（更广的视野）
    for frame in range(scene.frame_start, scene.frame_end + 1, 10):
        scene.frame_set(frame)
        progress = (frame - 1) / (scene.frame_end - 1)
        camera.location.x = progress * 20
        camera.location.y = -15 + progress * 5  # 更宽的视野
        camera.keyframe_insert(data_path="location", frame=frame)
    
    bpy.ops.object.mode_set(mode='OBJECT')

# 渲染动画
def render_animation():
    print("开始渲染动画...")
    bpy.ops.render.render(animation=True)
    print("渲染完成！")

# 主函数
def main():
    print("开始创建跑酷动画项目...")

    # 清除场景
    clear_scene()

    # 创建场景元素
    character_parts, character_root = create_character()
    armature = create_armature()
    obstacles = create_obstacles()
    ground = create_ground()
    camera = create_camera()
    lights = create_lights()

    # 绑定角色到骨骼
    parent_character_to_armature(character_parts, armature, character_root)

    # 设置场景
    setup_scene()

    # 创建动画
    create_animation(character_parts, armature, obstacles, camera)

    # 保存项目文件
    project_path = "/Users/mac/Desktop/parkour_animation/parkour_project.blend"
    bpy.ops.wm.save_as_mainfile(filepath=project_path)
    print(f"项目已保存到: {project_path}")

    print("项目创建完成！")
    print(f"输出路径: {bpy.context.scene.render.filepath}")
    print(f"帧数: {bpy.context.scene.frame_start} - {bpy.context.scene.frame_end}")
    print(f"分辨率: {bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}")

    # 询问是否渲染
    print("\n你可以:")
    print("1. 在 Blender 中预览动画")
    print("2. 运行 render_animation() 来渲染序列帧")

if __name__ == "__main__":
    main()

