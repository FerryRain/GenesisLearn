"""
@FileName：9_Interection_debugging.py
@Description：
@Author：Ferry
@Time：2024/12/27 下午2:48
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""

import genesis as gs

gs.init()

scene = gs.Scene(show_viewer=False)

plane = scene.add_entity(gs.morphs.Plane())
franka = scene.add_entity(
    gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"),
)

cam_0 = scene.add_camera()
scene.build()

# enter IPython's interactive mode
import IPython

IPython.embed()
