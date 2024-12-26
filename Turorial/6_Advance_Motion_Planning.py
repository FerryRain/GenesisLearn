"""
@FileName：6_Advance_Motion_Planning.py
@Description：
@Author：Ferry
@Time：2024/12/26 下午5:16
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""
import numpy as np
import genesis as gs

gs.init(seed=0, precision='32', backend=gs.gpu)

scene = gs.Scene(
    viewer_options= gs.options.ViewerOptions(
        camera_pos=(2.0, -2, 1.5),
        camera_lookat=(0.0, 0.0, 0.0),
        camera_fov=40,
    ),
    rigid_options=gs.options.RigidOptions(
        # enable_joint_limit=False,
        enable_collision=False,
    ),
    # sim_options=gs.options.SimOptions(
    #     dt=0.01,
    #     substeps=4,  # for more stable grasping contact
    # ),
    # show_viewer=True,
)

scene.add_entity(
    gs.morphs.Plane()
)
robot = scene.add_entity(
   gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml')
)

# two target links for visualization
target_left = scene.add_entity(
    gs.morphs.Mesh(
        file='meshes/axis.obj',
        scale=0.1,
    ),
    surface=gs.surfaces.Default(color=(1, 0.9, 0.9, 1)),
)
target_right = scene.add_entity(
    gs.morphs.Mesh(
        file='meshes/axis.obj',
        scale=0.1,
    ),
    surface=gs.surfaces.Default(color=(0.5, 1.0, 0.5, 1)),
)

scene.build()

target_quat = np.array([0, 1, 0, 0])
center = np.array([0.4, -0.2, 0.25])
r = 0.1

left_finger = robot.get_link("left_finger")
right_finger = robot.get_link("right_finger")


for i in range(0, 2000):
    target_pos_left = center + np.array([np.cos(i / 360 * np.pi), np.sin(i / 360 * np.pi), 0]) * r
    target_pos_right = target_pos_left + np.array([0.0, 0.03, 0])

    target_left.set_qpos(np.concatenate([target_pos_left, target_quat]))
    target_right.set_qpos(np.concatenate([target_pos_right, target_quat]))

    q = robot.inverse_kinematics_multilink(
        links=[left_finger, right_finger],
        poss=[target_pos_left, target_pos_right],
        quats=[target_quat, target_quat],
        rot_mask=[False, False, True],  # only restrict direction of z-axis
    )
    # path = robot.plan_path(
    #     qpos_goal=q,
    #     num_waypoints=200,  # 2s duration
    # )
    # for waypoint in path:
    #     robot.control_dofs_position(waypoint)
    #     scene.step()

    # Note that this IK is for visualization purposes, so here we do not call scene.step(), but only update the state and the visualizer
    # In actual control applications, you should instead use robot.control_dofs_position() and scene.step()
    robot.set_dofs_position(q)
    scene.visualizer.update()
    # robot.control_dofs_position(q)
    # scene.step()