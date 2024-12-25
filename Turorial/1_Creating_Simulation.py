"""
@FileName：1_Creating_Simulation.py
@Description：
@Author：Ferry
@Time：2024/12/25 下午1:53
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""
import genesis as gs
import torch

gs.init(backend=gs.gpu, theme='light')

scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.01,
        gravity=(0, 0, -1.0),
    ),
    show_viewer=True,
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(3.5, 0.0, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
    ),
)
plane = scene.add_entity(gs.morphs.Plane())

franka = scene.add_entity(
    gs.morphs.URDF(
        file='urdf/panda_bullet/panda.urdf',
        pos=(0, 0, 1),
        euler=(0, 0, 90), # we follow scipy's extrinsic x-y-z rotation convention, in degrees,
        # quat  = (1.0, 0.0, 0.0, 0.0), # we use w-x-y-z convention for quaternions,
        scale=1.0,
        fixed=True,
    ),
)

# creat more parallels
num_envs = 20
scene.build(n_envs=num_envs, env_spacing=(1.0, 1.0))

franka.control_dofs_position(
    torch.tile(torch.tensor([0, 0, 0, -1.0, 0, 0, 0, 0.02, 0.02], device=gs.device), (num_envs, 1)),
)
for i in range(1000):
    scene.step()