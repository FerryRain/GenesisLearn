"""
@FileName：2_Visual_Render.py
@Description：
@Author：Ferry
@Time：2024/12/25 下午5:13
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""
import genesis as gs
gs.init()

scene = gs.Scene(
    show_viewer=True,
    viewer_options=gs.options.ViewerOptions(
        # res=(1920, 1080),
        camera_pos=(3.5, .0, 2.5),
        camera_lookat=(.0,.0,.5),
        camera_fov=40,
    ),
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        world_frame_size=1.0,
        show_link_frame=False,
        show_cameras=False,
        plane_reflection=True,
        ambient_light=(0.1, 0.1, 0.1),
    ),
    # renderer=gs.renderers.RayTracer(),
    renderer=gs.renderers.Rasterizer(),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"),
)

cam = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0, 0, 0.5),
    fov=30,
    GUI=True,
)

scene.build()

# render rgb, depth, segmentation, normal



import numpy as np

while True:
    # cam.start_recording()
    for i in range(10000):
        scene.step()
        cam.set_pose(
            pos=(3.0 * np.sin(i / 60), 3.0 * np.cos(i / 60), 2.5),
            lookat=(0, 0, 0.5),
        )
        # rgb, depth, segmentation, normal = cam.render(rgb=True, depth=True, segmentation=True, normal=True)
        rgb, depth, segmentation, normal = cam.render(segmentation=True)
        # cam.render()
    # cam.stop_recording(save_to_filename="video.mp4", fps=60)
