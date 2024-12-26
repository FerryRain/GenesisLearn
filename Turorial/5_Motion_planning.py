"""
@FileName：5_Motion_planning.py
@Description：
@Author：Ferry
@Time：2024/12/26 下午4:34
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""
import numpy as np
import genesis as gs

gs.init(backend=gs.gpu, theme='light')

scene = gs.Scene(
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(3, -1, 1.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=30,
        max_FPS=60,
    ),
    sim_options=gs.options.SimOptions(
        dt=0.01,
        substeps=4,  # for more stable grasping contact
    ),
    show_viewer=True,
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
cube = scene.add_entity(
    gs.morphs.Box(
        size=(0.04, 0.04, 0.04),
        pos=(0.65, 0.0, 0.02),
    )
)
franka = scene.add_entity(
    gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"),
)

scene.build()

motors_dof = np.arange(7)
fingers_dof = np.arange(7, 9)

# franka.set_dofs_kp(
#     np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
# )
# franka.set_dofs_kv(
#     np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
# )
# franka.set_dofs_force_range(
#     np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
#     np.array([87, 87, 87, 87, 12, 12, 12, 100, 100]),
# )

end_effector = franka.get_link("hand")

# move to pre-grasp pose
qpos = franka.inverse_kinematics(
    link=end_effector,
    pos=np.array([0.65, 0.0, 0.25]),
    quat=np.array([0, 1, 0, 0]),
)

# gripper open pos
qpos[-2:] = 0.04
path = franka.plan_path(
    qpos_goal=qpos,
    num_waypoints=200,  # 2s duration
)

# execute the planned path
for waypoint in path:
    franka.control_dofs_position(waypoint)
    scene.step()

# allow robot to reach the last waypoint
for i in range(100):
    scene.step()

# reach
qpos = franka.inverse_kinematics(
    link=end_effector,
    pos=np.array([0.65, 0.0, 0.135]),
    quat=np.array([0, 1, 0, 0]),
)
franka.control_dofs_position(qpos[:-2], motors_dof)
for i in range(100):
    scene.step()

# grasp
franka.control_dofs_position(qpos[:-2], motors_dof)
franka.control_dofs_force(np.array([-0.5, -0.5]), fingers_dof)

for i in range(100):
    scene.step()

# lift
qpos = franka.inverse_kinematics(
    link=end_effector,
    pos=np.array([0.65, 0.0, 0.3]),
    quat=np.array([0, 1, 0, 0]),
)
franka.control_dofs_position(qpos[:-2], motors_dof)
for i in range(200):
    scene.step()