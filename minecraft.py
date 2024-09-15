from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app=Ursina(title="Minecraft Denemesi",icon='assets/Minecraft_icon.ico')

texture_dict={
  'grass' : 'assets/grass_texture.png',
  'stone' : 'assets/stone_block.png',
  'collebstone' : 'assets/collebstone_texture.png',
  'wood' : 'assets/wood_block.png',
  'brick':'assets/brick_texture.png',
  'dirt' : 'assets/dirt_texture.png',
  'sky' : 'assets/skybox.png',
  'arm' : 'assets/arm_texture2.png'
}

textures=list(texture_dict.values())
block_pick = 1
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)


sky=Entity(
    parent=scene,
    model='sphere',
    texture=texture_dict['sky'],
    scale=1000,
    double_sided=True )


def input(key):
    if key == 'escape':  
        mouse.locked = not mouse.locked  
        mouse.visible = not mouse.visible 


class Crosshair(Entity):
    def __init__(self):
        super().__init__()

        self.horizontal_line = Entity(
            parent=camera.ui,
            model='quad',  
            scale=(0.04, 0.004),  
            color=color.white,
            position=(0, 0,-0.1)  
        )

        self.vertical_line = Entity(
            parent=camera.ui,
            model='quad',
            scale=(0.004, 0.04),  
            color=color.white,
            position=(0, 0,-0.1)  
        )
            
     
crosshair = Crosshair()


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=textures[0]):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            scale=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.lime,
        )


    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                for i in range (9):
                    if block_pick == i+1:
                       voxel = Voxel(position=self.position + mouse.normal, texture=textures[i])
                
            if self.y!=0:
               if key == 'right mouse down':
                   punch_sound.play()
                   destroy(self)


              
world_size=20
world_depth=5

for z in range(world_size):
    for x in range(world_size):
        for y in range(world_depth):
            if y == 4:
                voxel = Voxel(position=(x, y, z), texture=textures[0])
            elif y == 0:
                voxel = Voxel(position=(x, y, z), texture=textures[1])
            else:
                voxel = Voxel(position=(x, y, z), texture=textures[5])
                


class Selected_voxel(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/block',
            texture=textures[block_pick],
            scale=0.15,
            rotation=(30, -10),
            position=(0.4, -0.3,3)
            )

    def active(self):
        self.position = (0.3, -0.2,3)
   

    def passive(self):
        self.position = (0.4, -0.3,3)
     
   
selected_voxel=Selected_voxel()



class Hand(Entity):
    def __init__(self):
	    super().__init__(
	    parent = camera.ui,
	    model = 'assets/arm',
	    texture = texture_dict['arm'],
	    scale = 0.2,
	    rotation = (150,-10),
	    position = (0.6,-0.6)
            )

    def active(self):
	    self.position = (0.5,-0.5)
	   

    def passive(self):
	    self.position =(0.6,-0.6)
	   
hand=Hand()




class NonInteractiveButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_color = self.color
        self.collision = False

        

class Border(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        cell_size = 0.08  
        spacing = 0.02
        self.cells = []
        for i in range(9):
                    cell = NonInteractiveButton(               
                    parent=self,
                    model='quad',
                    color=color.rgba(0, 0, 0, 0.5),
                    scale=(cell_size, cell_size),  
                    origin=(-0.5, 0),
                    position=Vec3(-0.43 + i * (cell_size + spacing), -0.42, -0.03),
                    render_order=3,no=i+1)
                    self.cells.append(cell)
            
border=Border()


        
class TableUI(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        cell_size = 0.08  
        spacing = 0.02  

        self.cells = [] 
        for i in range(6):
                cell = NonInteractiveButton(               
                parent=self,
                model='quad',
                color=color.rgb(1, 1, 1),
                texture=["assets/grass_block.png","assets/Stone3d.png","assets/collebstone_block.png","assets/plank3d.png","assets/Brick3d.png","assets/dirt_block.png"][i],
                scale=(cell_size, cell_size),  
                origin=(-0.5, 0),
                position=Vec3(-0.43 + i * (cell_size + spacing), -0.42,-0.04) , 
                text_entity = Text(parent=self, text=str(i+1), position=Vec3(-0.43 + i * (cell_size + spacing), -0.382,-0.041),text_color=color.white),
                render_order=4)
                self.cells.append(cell)

       
table = TableUI()

              
player = FirstPersonController(position=(10,15,10))

min_x, max_x = 1, world_size-1
min_z, max_z = 1, world_size-1

def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
        selected_voxel.active()
    else:
        hand.passive()
        selected_voxel.passive()
    if held_keys['1']: block_pick=1
    if held_keys['2']: block_pick=2
    if held_keys['3']: block_pick=3
    if held_keys['4']: block_pick=4
    if held_keys['5']: block_pick=5
    if held_keys['6']: block_pick=6

    selected_voxel.texture=textures[block_pick-1]
    cells=border.cells
    
    for cell in cells:
        if cell.no == block_pick:  
            cell.color = color.rgba(1, 0, 0, 0.5)
        else:
             cell.color = color.rgba(0, 0, 0, 0.5)

    if player.x < min_x:
         player.x = min_x
    if player.x > max_x:
         player.x = max_x

    if player.z < min_z:
         player.z = min_z
    if player.z > max_z:
         player.z = max_z
        


app.run()

