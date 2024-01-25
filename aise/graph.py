from typing import List

import arcade
import random
import pyglet.clock


class AiseGraph(arcade.Sprite):
    """
    Create a graph showing performance statistics.
    """
    def __init__(self,
                 width, height,
                 graph_data: str = "FPS",
                 data_to_graph: List[float] = [],
                 update_rate: float = 0.1,
                 spacing: int = 3,
                 background_color=arcade.color.BLACK,
                 data_line_color=arcade.color.WHITE,
                 axis_color=arcade.color.DARK_YELLOW,
                 grid_color=arcade.color.DARK_YELLOW,
                 font_color=arcade.color.WHITE,
                 font_size=10):

        unique_id = str(random.random())

        self.minimap_texture = arcade.Texture.create_empty(unique_id, (width, height))
        super().__init__(texture=self.minimap_texture)
        self.background_color = background_color
        self.line_color = data_line_color
        self.grid_color = grid_color
        self.data_to_graph = data_to_graph
        self.proj = 0, self.width, 0, self.height
        self.axis_color = axis_color
        self.graph_data = graph_data
        self.max_data = 0.0
        self.font_color = font_color
        self.font_size = font_size
        self.spacing = spacing
        pyglet.clock.schedule_interval(self.update_graph, update_rate)

    def remove_from_sprite_lists(self):
        super().remove_from_sprite_lists()
        pyglet.clock.unschedule(self.update)

    def update_graph(self, delta_time: float):
        """
        Update the graph.
        """
        bottom_y = 15
        left_x = 25

        # Get the sprite list this is part of, return if none
        if self.sprite_lists is None or len(self.sprite_lists) == 0:
            return
        sprite_list = self.sprite_lists[0]

        # Clear and return if timings are disabled
        if not arcade.timings_enabled():
            with sprite_list.atlas.render_into(self.minimap_texture, projection=self.proj) as fbo:
                nothing_color = 0, 0, 0, 0
                fbo.clear(nothing_color)
            return

        # Get FPS and add to our historical data
        #self.data_to_graph.append(arcade.get_fps())

        if len(self.data_to_graph) == 0:
            return

        # Toss old data
        while len(self.data_to_graph) > self.width - left_x:
            self.data_to_graph.pop(0)

        # Set max data
        max_value = max(self.data_to_graph)
        self.max_data = ((max_value + 1.5) // 20 + 1) * 20.0

        # Render to the screen
        with sprite_list.atlas.render_into(self.minimap_texture, projection=self.proj) as fbo:
            fbo.clear(self.background_color)
            max_pixels = self.height - bottom_y
            point_list = []
            x = left_x
            for reading in self.data_to_graph:
                self.max_data = 1 if self.max_data == 0 else self.max_data
                y = (reading / self.max_data) * max_pixels + bottom_y
                point = x, y
                point_list.append(point)
                x += self.spacing

            # Draw the base line
            arcade.draw_line(left_x, bottom_y, left_x, self.height, self.axis_color)

            # Draw left axis
            arcade.draw_line(left_x, bottom_y, self.width, bottom_y, self.axis_color)

            # Draw number labels
            arcade.draw_text("0", left_x, bottom_y, self.font_color, self.font_size, anchor_x="right", anchor_y="center")  # noqa
            increment = self.max_data // 4
            for i in range(4):
                value = increment * i
                label = f"{int(value)}"
                y = (value / self.max_data) * max_pixels + bottom_y
                arcade.draw_text(label, left_x, y, self.font_color, self.font_size, anchor_x="right",
                                 anchor_y="center")
                arcade.draw_line(left_x, y, self.width, y, self.grid_color)

            # Draw label
            arcade.draw_text(self.graph_data, 0, 2, self.font_color, self.font_size, align="center",
                             width=int(self.width))

            # Draw graph
            arcade.draw_line_strip(point_list, self.line_color)




class AiseMGraph(arcade.Sprite):
    """
    Create a graph showing performance statistics.
    """
    def __init__(self,
                width, height,
                datasets: List[dict] = None,
                update_rate: float = 0.1,
                spacing: int = 3,
                background_color=arcade.color.BLACK,
                axis_color=arcade.color.DARK_YELLOW,
                grid_color=arcade.color.DARK_YELLOW,
                font_color=arcade.color.WHITE,
                font_size=10):
            
        unique_id = str(random.random())

        self.minimap_texture = arcade.Texture.create_empty(unique_id, (width, height))
        super().__init__(texture=self.minimap_texture)
        self.background_color = background_color
        #self.line_color = data_line_color
        self.grid_color = grid_color
        self.proj = 0, self.width, 0, self.height
        self.axis_color = axis_color
        #self.graph_data = graph_data
        self.datasets = datasets or []
        #self.max_data = 0.0
        self.font_color = font_color
        self.font_size = font_size
        self.spacing = spacing
        pyglet.clock.schedule_interval(self.update_graph, update_rate)

    def remove_from_sprite_lists(self):
        super().remove_from_sprite_lists()
        pyglet.clock.unschedule(self.update)

    def update_graph(self, delta_time: float):
        """
        Update the graph.
        """
        bottom_y = 15
        left_x = 25

        # Get the sprite list this is part of, return if none
        if self.sprite_lists is None or len(self.sprite_lists) == 0:
            return
        sprite_list = self.sprite_lists[0]

        # Clear and return if timings are disabled
        if not arcade.timings_enabled():
            with sprite_list.atlas.render_into(self.minimap_texture, projection=self.proj) as fbo:
                nothing_color = 0, 0, 0, 0
                fbo.clear(nothing_color)
            return

        with sprite_list.atlas.render_into(self.minimap_texture, projection=self.proj) as fbo:
            fbo.clear(self.background_color)
            max_pixels = self.height - bottom_y
            
            for dataset in self.datasets:
                point_list = []
                x = left_x

                # Check if dataset['data'] is empty
                if not dataset['data']:
                    continue
                                
                max_data = max(dataset['data'])  # Calculate max data for this dataset
                for reading in dataset['data']:
                    y = (reading / max_data) * max_pixels + bottom_y
                    point = x, y
                    point_list.append(point)
                    x += self.spacing
                
                # Draw the base line
                arcade.draw_line(left_x, bottom_y, left_x, self.height, dataset['axis_color'])

                # Draw left axis
                arcade.draw_line(left_x, bottom_y, self.width, bottom_y, dataset['axis_color'])

                # Draw number labels
                arcade.draw_text("0", left_x, bottom_y, self.font_color, self.font_size, anchor_x="right", anchor_y="center")  # noqa
                increment = max_data // 4
                for i in range(4):
                    value = increment * i
                    label = f"{int(value)}"
                    y = (value / max_data) * max_pixels + bottom_y
                    arcade.draw_text(label, left_x, y, self.font_color, self.font_size, anchor_x="right",
                                    anchor_y="center")
                    arcade.draw_line(left_x, y, self.width, y, dataset['grid_color'])

                # Draw legend
                arcade.draw_text(dataset['legend'], 0, 2, dataset['font_color'], self.font_size, align="center",
                                width=int(self.width))

                # Draw graph
                arcade.draw_line_strip(point_list, dataset['line_color'])