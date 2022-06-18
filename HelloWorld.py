import sys
import sdl2.ext

RESOURCES = sdl2.ext.Resources(__file__,"resources")

sdl2.ext.init()

window = sdl2.ext.Window("Hello World!",size=(800,600))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
sprite = factory.from_image(RESOURCES.get_path("DonaldDucksheet.gif"))
sub1 = sprite.subsprite((0,0,100,100))

spriterenderer = factory.create_sprite_render_system(window)
spriterenderer.render(sub1,50,50)

processor = sdl2.ext.TestEventProcessor()
processor.run(window)