#!/bin/bash


class GridWidthHeight:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height


class GridLayer:
    def __init__(self, grid_width_height):
        self.__dimensions = grid_width_height
        self.__grid2D = [[None for _ in range(self.__dimensions.width)] for _ in range(self.__dimensions.height)]

    def __getitem__(self, index):
        return self.__grid2D[index]

    @property
    def width(self):
        return self.__dimensions.width

    @property
    def height(self):
        return self.__dimensions.height


class GridMap:
    def __init__(self, grid_width_height):
        self.__dimensions = grid_width_height
        self.__layers = {}

    def add_layer(self, key):
        self.__layers[key] = GridLayer(self.__dimensions)

    def remove_layer(self, key):
        return self.__layers.pop(key, None)

    def __getitem__(self, key):
        return self.__layers[key]

    def __contains__(self, *args, **kwargs):
        self.__layers.__contains__(args, kwargs)

    def get_depth(self):
        return len(self.__layers)

    @property
    def width(self):
        return self.__dimensions.width

    @property
    def height(self):
        return self.__dimensions.height
