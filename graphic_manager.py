from typing import Callable, Any
import pygame


# 프레임 단위의 그래픽을 그려주는 클래스
class Function_TimingManager:
    def __init__(self):
        self.__functions: list[list[Callable[[pygame.Surface, *Any], None]]] = []
        self.__function_params: list[list[tuple[Any]]] = []

    def add_functions(self, func, after_frame, params):
        while len(self.__functions) <= after_frame:
            self.__functions.append([])
        while len(self.__function_params) <= after_frame:
            self.__function_params.append([])
        self.__functions[after_frame].append(func)
        self.__function_params[after_frame].append(params)

    def execute(self):
        if len(self.__functions) == 0:
            return
        for motion, params in zip(self.__functions.pop(0), self.__function_params.pop(0)):
            motion(*params)

    def motion_playing(self):
        return len(self.__functions) != 0

    def motion_length(self):
        return len(self.__functions)

    def clear(self):
        self.__functions: list[list[Callable[[pygame.Surface, *Any], None]]] = []
        self.__function_params: list[list[tuple[Any]]] = []


timing_manager = Function_TimingManager()
