import sys, math, random
import pygame
import pygame.draw
import numpy

__screenSize__ = (1600,1280)
__cellSize__ = 20
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))

__wallcolor = (10,10,10)

def getColorCell(n):
    if n == -1:
        return (0,200,0)
    if n == 0:
        return (255,255,255)
    if n == 2:
        return (255, 0, 0)
    tmp = (1-n)*240 + 10
    return (tmp, tmp, tmp)

class Grid:
    _grid= None
    def __init__(self):
        print("Creating a grid of dimensions " + str(__gridDim__))
        self._grid = numpy.zeros(__gridDim__)

    def addWallFromMouse(self, coord, w):
        x = int(coord[0] / __cellSize__)
        y = int(coord[1] / __cellSize__)
        self._grid[x,y] = w

    # draw the exploration graph
    def add_path(self, coord):
        self._grid[coord[0],coord[1]] = -1

    # draw the solution path
    def addPath(self, path_arr=[]):
        if path_arr is not None:
            for coord in path_arr:
                self._grid[coord[0],coord[1]] = 2


    def reset_path(self):
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                if self._grid[x,y] == -1 or self._grid[x,y] == 2:
                    self._grid[x,y] = 0

    def drawMe(self):
        pass


class Node():
  

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    


class Scene:
    _mouseCoords = (0,0)
    _grid = None
    _font = None
    _first_clic = (-1, -1)
    _second_clic = (-1, -1)

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode(__screenSize__)
        self._font = pygame.font.SysFont('Arial',25)
        self._grid = Grid()

    def drawMe(self):
        if self._grid._grid is None:
            return
        self._screen.fill((128,128,128))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen, 
                        getColorCell(self._grid._grid.item((x,y))),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))

    def drawPath(self, path_array):
        if self._grid._grid is None:
            return
        self._screen.fill((128,128,128))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen, 
                        (125,70,125),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))


    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        pass

    def eventClic(self,coord,b, mouse=False): # ICI METTRE UN A* EN TEMPS REEL b?

        # variable initialization clic by clic
        if self._first_clic == (-1,-1):

            self._first_clic = (int(coord[0] / __cellSize__), int(coord[1] / __cellSize__))
            # Check if the is an obstacle wall
            if self._grid._grid[self._first_clic[0],self._first_clic[1]] == 1:
                self._first_clic = (-1,-1)
                return

        elif self._second_clic == (-1,-1) or mouse == True:
            self._second_clic = (int(coord[0] / __cellSize__), int(coord[1] / __cellSize__))
            # Check if the is an obstacle wall
            if self._grid._grid[self._second_clic[0],self._second_clic[1]] == 1:
                self._second_clic = (-1,-1)
                return
        
       

       
        # A*
        # les deux clics sont définit le départ et l'arrivée
        if self._first_clic != (-1,-1) and self._second_clic != (-1,-1):
            listeOuvert = []
            listeFermer = []


            # Create start and end node
            start_node = Node(None, self._first_clic)
            start_node.g = start_node.h = start_node.f = 0
            end_node = Node(None, self._second_clic)
            end_node.g = end_node.h = end_node.f = 0
            # g: distance between the current node and the start node
            # h: heuristic --> estimated distance from the current node to the end node
            # f: total cost of the node f=g+h

            listeOuvert.append(start_node)
            
            
            # Check if there are unexplored nodes
            while len(listeOuvert) > 0:

                # Get the current node
                current_node = listeOuvert[0]
                current_index = 0

                # look for the most optimal node
                for index, item in enumerate(listeOuvert):
                    if item.f < current_node.f:
                        current_node = item
                        current_index = index

                
                # pop the optimal node and add it to the closed list
                listeOuvert.pop(current_index)
                listeFermer.append(current_node)


                # Trouver le dernier noeud
                if current_node.position == end_node.position:
                    path = []
                    current = current_node
                    listeOuvert = []
                    while current is not None:
                        path.append(current.position)
                        current = current.parent
                    print(path[::-1])
                    return path[::-1]
                

                # Teste les positions adjacentes d'une case
                children = []
                for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0) ]: 
                    # get a posssible node move
                    node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                    
                    # check that we stay in the grid
                    if node_position[0] > (__gridDim__[0] - 1) or node_position[0] < 0 or node_position[1] > (__gridDim__[1] -1) or node_position[1] < 0:
                        continue


                    # Check if there is an obstacle wall
                    if self._grid._grid[node_position[0],node_position[1]] == 1:
                        continue
  

                    # Create new node
                    new_node = Node(current_node, node_position)
                    # Append
                    children.append(new_node)


                
                # Loop through children
                for child in children:
                    add_child = True
                    # Check if child is on the closed list
                    for closed_child in listeFermer:
                        if (child.position[0] == closed_child.position[0]) and (child.position[1] == closed_child.position[1]):
                            add_child = False
                    
                    # Initialize the new node
                    child.g = current_node.g + 1 # distance entre noeud de départ et le courant
                    # distance entre noeud courant et noeuds d'arrivé
                    child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                    child.f = child.g + child.h

                    # Check if child is in the open list
                    for open_node in listeOuvert:
                        if (child.position[0] == open_node.position[0]) and (child.position[1] == open_node.position[1]):
                            add_child = False
                            
                

                    if add_child == True:
                        listeOuvert.append(child)

                        # draw the exploration graph
                        self._grid.add_path(child.position)
                
               








                            

        pass
    def recordMouseMove(self, coord):
        pass

def main():
    buildingGrid = False # True if the user can add / remove walls / weights
    scene = Scene()
    done = False
    clock = pygame.time.Clock()
    buildingTrack = True
    wallWeight = 1
    start_node = False

    while done == False:
        clock.tick(1000)
        scene.update()
        scene.drawMe()
        if buildingTrack:
            additionalMessage = ": BUILDING (" + str(int(wallWeight*100)) + "%)"
        scene.drawText("Super A*" + additionalMessage, (10,10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print("Exiting")
                done=True
            if event.type == pygame.KEYDOWN: 
                
                if event.key == pygame.K_q or event.key==pygame.K_ESCAPE: # q
                    print("Exiting")
                    done = True
                    break
                
                
                if event.key == pygame.K_n:
                    buildingTrack = False
                    break
                if event.key == pygame.K_b :
                    buildingTrack = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buildingTrack:
                    scene._grid.addWallFromMouse(event.dict['pos'], wallWeight)
                else:
                    start_node = True
            elif event.type == pygame.MOUSEMOTION:
                if start_node == True:
                    scene._grid.reset_path()
                    path_arr = scene.eventClic(event.dict['pos'],None, mouse=True)
                    
                    scene._grid.addPath(path_arr)

                scene.recordMouseMove(event.dict['pos'])

    pygame.quit()

if not sys.flags.interactive: main()

