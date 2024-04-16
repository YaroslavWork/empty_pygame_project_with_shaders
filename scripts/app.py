import pygame
import moderngl
import array
import sys

import scripts.settings as s
from scripts.camera import Camera
from scripts.field import Field
from scripts.UI.text import Text


class App:

    def __init__(self) -> None:
        # Initialize pygame and settings
        pygame.init()

        self.size = self.width, self.height = s.SIZE
        self.name = s.NAME
        self.colors = s.COLORS
        self.fps = s.FPS

        # Set pygame window
        pygame.display.set_caption(self.name)

        # Set pygame windows
        self.screen = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.UI_display = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.game_display = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        # Set pygame ctx and clock
        self.ctx = moderngl.create_context()
        self.clock = pygame.time.Clock()


        # Set input variables
        self.dt = 0
        self.mouse_pos = (0, 0)
        self.keys = []

        # Set model variables
        self.camera = Camera(x=0, y=0, distance=10, resolution=self.size)
        # This line takes data from save file
        self.field = Field()

        # Set shader variables
        self.quad_buffer = self.ctx.buffer(array.array('f', [
            # position (x, y)  # texture (u, v)
            -1.0, 1.0, 0.0, 0.0,  # top left
            1.0, 1.0, 1.0, 0.0,  # top right
            -1.0, -1.0, 0.0, 1.0,  # bottom left
            1.0, -1.0, 1.0, 1.0,  # bottom right
        ]))

        vert_shader = open(f'{sys.path[0]}/scripts/shaders/vert_shader.glsl', 'r').read()
        frag_shader = open(f'{sys.path[0]}/scripts/shaders/frag_shader.glsl', 'r').read()

        self.program = self.ctx.program(
            vertex_shader=vert_shader,
            fragment_shader=frag_shader
        )
        self.render_object = self.ctx.vertex_array(
            self.program,
            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')]
        )



    def surf_to_texture(self, surf: pygame.Surface) -> moderngl.Texture:
        """
        Convert pygame surface to moderngl texture
        """
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex


    def update(self) -> None:
        """
        Main update function of the program.
        This function is called every frame
        """

        # -*-*- Input Block -*-*-
        self.mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If you want to close the program...
                close()
                Text.fonts = {}  # Clear fonts

            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button down...
                if event.button == 1:
                    pass
                elif event.button == 3:
                    pass

            if event.type == pygame.KEYDOWN:  # If key button down...
                if event.key == pygame.K_SPACE:
                    pass

        self.keys = pygame.key.get_pressed()  # Get all keys (pressed or not)
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.camera.move_left(1, self.dt)
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.camera.move_right(1, self.dt)
        if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
            self.camera.move_up(1, self.dt)
        if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
            self.camera.move_down(1, self.dt)
        if self.keys[pygame.K_e]:
            self.camera.scale_in(1, self.dt)
        if self.keys[pygame.K_q]:
            self.camera.scale_out(1, self.dt)
        # -*-*-             -*-*-

        # -*-*- Physics Block -*-*-

        # -*-*-               -*-*-

        # -*-*- Rendering Block -*-*-
        self.UI_display.fill(s.COLORS['transparent'])  # Clear UI display
        self.game_display.fill(s.COLORS['transparent'])  # Clear game display

        self.camera.draw_map_scale(self.UI_display, offset=(140, 15))  # Draw map scale
        Text("FPS: " + str(int(self.clock.get_fps())), (0, 0, 0), 20).print(self.UI_display,
                                                                            (self.width - 70, self.height - 21),
                                                                            False)  # FPS counter
        # -*-*-                 -*-*-

        # -*-*- Shaders Block -*-*-
        frame_tex1 = self.surf_to_texture(self.game_display)
        frame_tex2 = self.surf_to_texture(self.UI_display)

        frame_tex1.use(1)
        self.program['gameTex'] = 1
        frame_tex2.use(2)
        self.program['uiTex'] = 2

        # self.program['time'] = pygame.time.get_ticks() / 1000
        self.program['backgroundColor'] = (
            s.COLORS['background'][0] / 255,
            s.COLORS['background'][1] / 255,
            s.COLORS['background'][2] / 255
        )
        # self.program['resolution'] = self.size
        # self.program['cameraPos'] = (self.camera.x, self.camera.y)
#       # self.program['cameraDist'] = self.camera.distance

        self.render_object.render(moderngl.TRIANGLE_STRIP)

        # -*-*- Update Block -*-*-
        pygame.display.flip()

        frame_tex1.release()
        frame_tex2.release()

        self.dt = self.clock.tick(self.fps)
        # -*-*-              -*-*-


def close():
    pygame.quit()
    exit()
