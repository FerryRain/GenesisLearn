"""
@FileName：Liquid_Simulation.py
@Description：
@Author：Ferry
@Time：2024/12/26 下午8:34
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""
import genesis as gs

########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################

scene = gs.Scene(
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(0.0, -2, 1.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
        max_FPS=200,
    ),
    sim_options=gs.options.SimOptions(
        dt=4e-3,
        substeps=10,
    ),
    sph_options=gs.options.SPHOptions(
        lower_bound=(-0.8, -0.8, 0.0),
        upper_bound=(0.8, 0.8, 1),
        particle_size=0.01,
    ),
    vis_options=gs.options.VisOptions(
        visualize_sph_boundary=True,
    ),
    show_viewer=True,
)

########################## entities ##########################
plane = scene.add_entity(
    morph=gs.morphs.Plane(),
)

liquid = scene.add_entity(
    # viscous liquid
    material=gs.materials.SPH.Liquid(mu=0.02, gamma=0.02),
    # material=gs.materials.SPH.Liquid(),
    morph=gs.morphs.Box(
        pos=(0.0, 0.0, 0.65),
        size=(0.5, 0.5, 0.5),
    ),
    surface=gs.surfaces.Default(
        color=(0.4, 0.8, 1.0),
        vis_mode="particle",
    ),
)

########################## build ##########################
scene.build()      # [Genesis] [20:32:34] [ERROR] Batching is only supported for rigid-only scenes as of now.


horizon = 1000

while True:
    for i in range(horizon):
        scene.step()

    # get particle positions
    particles = liquid.get_particles()

    scene.reset()
