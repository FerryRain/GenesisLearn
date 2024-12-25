"""
@FileName：3_Control_robot.py
@Description：
@Author：Ferry
@Time：2024/12/25 下午7:31
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""
import numpy as np
import genesis as gs
import torch

gs.init(backend=gs.gpu, theme='light')

scene = gs.Scene(
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(0, -3.5, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=30,
        max_FPS=60,
    ),
    sim_options=gs.options.SimOptions(
        dt=0.01,
    ),
    show_viewer=True,
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    gs.morphs.MJCF(
        file="xml/franka_emika_panda/panda.xml",
    ),
)

num_envs = 20

scene.build(n_envs=num_envs,env_spacing=(1.0,1.0))

jnt_names = [
    "joint1",
    "joint2",
    "joint3",
    "joint4",
    "joint5",
    "joint6",
    "joint7",
    "finger_joint1",
    "finger_joint2",
]
dofs_idx = [franka.get_joint(name).dof_idx_local for name in jnt_names]
dofs_idx = torch.tensor(dofs_idx, device=gs.device)

############ Optional: set control gains ############
# set positional gains
franka.set_dofs_kp(
    kp=np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
    dofs_idx_local=dofs_idx,
)
# set velocity gains
franka.set_dofs_kv(
    kv=np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
    dofs_idx_local=dofs_idx,
)
# set force range for safety
franka.set_dofs_force_range(
    lower=np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    upper=np.array([87, 87, 87, 87, 12, 12, 12, 100, 100]),
    dofs_idx_local=dofs_idx,
)

# Hard reset
for i in range(150):
    if i < 50:
        franka.set_dofs_position(torch.tile(torch.tensor([1, 1, 0, 0, 0, 0, 0, 0.04, 0.04]), (num_envs,1)).to(gs.device), dofs_idx)
    elif i < 100:
        franka.set_dofs_position(torch.tile(torch.tensor([-1, 0.8, 1, -2, 1, 0.5, -0.5, 0.04, 0.04]),(num_envs,1)).to(gs.device), dofs_idx)
    else:
        franka.set_dofs_position(torch.tile(torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0]), (num_envs,1)).to(gs.device), dofs_idx)

    scene.step()

# PD control
for i in range(1500):
    if i == 0:
        franka.control_dofs_position(
            torch.tile(torch.tensor([1, 1, 0, 0, 0, 0, 0, 0.04, 0.04]), (num_envs,1)).to(gs.device),
            # torch.tile(dofs_idx, (num_envs,1)),
            dofs_idx,
        )
    elif i == 250:
        franka.control_dofs_position(
            torch.tile(torch.tensor([-1, 0.8, 1, -2, 1, 0.5, -0.5, 0.04, 0.04]),(num_envs,1)).to(gs.device),
            # torch.tile(dofs_idx, (num_envs,1)),
            dofs_idx,
        )
    elif i == 500:
        franka.control_dofs_position(
            torch.tile(torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0]),(num_envs,1)).to(gs.device),
            # torch.tile(dofs_idx, (num_envs,1)),
            dofs_idx,
        )
    elif i == 750:
        # control first dof with velocity, and the rest with position
        franka.control_dofs_position(
            torch.tile(torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0]),(num_envs,1)).to(gs.device)[:, 1:],
            # torch.tile(dofs_idx, (num_envs,1))[:, 1:],
            dofs_idx[1:],
        )
        franka.control_dofs_velocity(
            torch.tile(torch.tensor([1.0, 0, 0, 0, 0, 0, 0, 0, 0]),(num_envs,1)).to(gs.device)[:, :1],
            # torch.tile(dofs_idx, (num_envs,1))[:, :1],
            dofs_idx[:1],
        )
    elif i == 1000:
        franka.control_dofs_force(
            torch.tile(torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0]),(num_envs,1)).to(gs.device),
            # torch.tile(dofs_idx, (num_envs,1)),
            dofs_idx,
        )
    elif i == 1250:
        # control only 3 environments: 1, 5, and 7. (You also need to comment out the function call above)
        franka.control_dofs_position(
            position=torch.zeros(3, 9, device=gs.device),
            envs_idx=torch.tensor([1, 5, 7], device=gs.device),
        )
    # This is the control force computed based on the given control command
    # If using force control, it's the same as the given control command
    print("control force:", franka.get_dofs_control_force(dofs_idx))

    # This is the actual force experienced by the dof
    print("internal force:", franka.get_dofs_force(dofs_idx))

    scene.step()