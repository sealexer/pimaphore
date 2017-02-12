import pygame


class SoundPlayer:
    def __init__(self, sound_file):
        self.sound_file = sound_file

    def init(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound_file)

    def shutdown(self):
        pygame.mixer.quit()

    def start(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()
        # pygame.mixer.music.fadeout(500)
        # pygame.mixer.music.rewind()

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()


class RotatingSoundPlayer:
    def __init__(self, sound_files):
        self.sound_files = sound_files
        self.current_file_index = 0

    def init(self):
        pygame.mixer.init()
        self.current_file_index = 0

    def shutdown(self):
        pygame.mixer.quit()

    def start(self):
        # print "Start playing " + str(self.sound_files[self.current_file_index])
        pygame.mixer.music.load(self.sound_files[self.current_file_index])
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()
        self.current_file_index = (self.current_file_index + 1) % len(self.sound_files)

    def pause(self):
        """ Just left for compatibility with SoundPlayer """
        pygame.mixer.music.pause()

    def resume(self):
        """ Just left for compatibility with SoundPlayer """
        pygame.mixer.music.unpause()
