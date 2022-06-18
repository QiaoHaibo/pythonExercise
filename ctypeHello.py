import sys
import ctypes
from sdl2 import *
from sdl2.sdlimage import *




def main():
    SDL_Init(SDL_INIT_EVERYTHING)
    #print("SDL_IMAGE_MAJOR_VERSION:",SDL_IMAGE_MAJOR_VERSION)
    window = SDL_CreateWindow(b"Hello World",
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              592, 460, SDL_WINDOW_SHOWN)
    windowsurface = SDL_GetWindowSurface(window)

    #image = SDL_LoadBMP(b"resources\\people.bmp")   #768 474 -> 12 8
    image = IMG_Load(b"resources\\people.bmp")
    sw = 64
    sh = 59
    sxi = 0
    syi = 0

    
    

    running = True
    event = SDL_Event()
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break

        rt = SDL_Rect(sxi*sw,syi*sh,sw,sh)
        SDL_BlitSurface(image, rt, windowsurface,None)
        SDL_UpdateWindowSurface(window)
        sxi = sxi +1
        if sxi >= 12:
            sxi = 0
            if syi >= 7:
                syi = 0
            syi = syi + 1
        SDL_Delay(200)

    SDL_FreeSurface(image)
    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())