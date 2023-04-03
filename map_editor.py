import pygame
import math
import json

pygame.init()

display_width = 1836
display_height = 782

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Map Editor')

clock = pygame.time.Clock()

verticies = []
edges = []

drawnEdges = []

def main():
    display_width = 1836
    display_height = 782

    display_scale = 1.0

    xOffset = 0
    yOffset = 0

    showImg = True
    pause = False

    img = pygame.image.load('bostonmap.png')
    originalImg = pygame.image.load('bostonmap.png')

    edgeLines = []
    currentEdge = []
    edgeStart = None

    font = pygame.font.Font("freesansbold.ttf", 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1: # Zoom in
                    display_scale -= 0.05
                    img = pygame.transform.smoothscale(originalImg, (display_width * display_scale, display_height * display_scale))
                elif event.y == 1: # Zoom out
                    display_scale += 0.05
                    img = pygame.transform.smoothscale(originalImg, (display_width * display_scale, display_height * display_scale))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Cancel Floating Line
                    currentEdge = []
                    edgeStart = None
                if event.key == pygame.K_m: # Show/Hide Map
                    showImg = not showImg
                if event.key == pygame.K_p: # Pause
                    pause = not pause
                if event.key == pygame.K_l: # Undo edge
                    drawnEdges.pop()
                    edgeLines.pop()
                if event.key == pygame.K_j: # place edge (keyboard)
                    check = False
                    for i in range(len(verticies)):
                        clickPos = (round((mousePos[0] - xOffset) / display_scale, 1), round((mousePos[1] - yOffset) / display_scale, 1))
                        distance = math.sqrt(pow(clickPos[0] - verticies[i][0], 2) + pow(clickPos[1] - verticies[i][1], 2))

                        if distance < 10: # If clicked on vertex
                            if len(currentEdge) == 0: # Start edge
                                edgeStart = i
                                print(f"started edge at {edgeStart}")
                                currentEdge.append(clickPos)
                                check = True
                                break
                            else: # Finish edge
                                print(f"finished edge at {i}")
                                currentEdge.append(clickPos)

                                length = 0
                                for j in range(len(currentEdge) - 1):
                                    firstPoint = currentEdge[j]
                                    secondPoint = currentEdge[j + 1]
                                    length += math.sqrt(pow(firstPoint[0] - secondPoint[0], 2) + pow(firstPoint[1] - secondPoint[1], 2))

                                edges.append((edgeStart, i, length))
                                edgeLines += [currentEdge]

                                drawnEdges.append([currentEdge, edgeStart, i])
                                currentEdge = []

                                check = True
                                break
                    if not len(currentEdge) == 0 and not check: # Place pivot on edge
                            print("selected intermediate")
                            currentEdge.append(clickPos)
                
                if event.key == pygame.K_q: # zoom in (keyboard)
                    display_scale += 0.05
                    img = pygame.transform.smoothscale(originalImg, (display_width * display_scale, display_height * display_scale))
                if event.key == pygame.K_e: # zoom out (keyboard)
                    display_scale -= 0.05
                    img = pygame.transform.smoothscale(originalImg, (display_width * display_scale, display_height * display_scale))

                if event.key == pygame.K_u: # Undo vertex
                    verticies.pop(-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # place vertex
                    vertexPos = (round((mousePos[0] - xOffset) / display_scale, 1), round((mousePos[1] - yOffset) / display_scale, 1))
                    verticies.append(vertexPos)
                    print(f"Added vertex at: {vertexPos}")
                if event.button == 3: 
                    check = False
                    for i in range(len(verticies)):
                        clickPos = (round((mousePos[0] - xOffset) / display_scale, 1), round((mousePos[1] - yOffset) / display_scale, 1))
                        distance = math.sqrt(pow(clickPos[0] - verticies[i][0], 2) + pow(clickPos[1] - verticies[i][1], 2))

                        if distance < 10: # If clicked on vertex
                            if len(currentEdge) == 0: # Start edge
                                edgeStart = i
                                print(f"started edge at {edgeStart}")
                                currentEdge.append(clickPos)
                                check = True
                                break
                            else: # Finish edge
                                print(f"finished edge at {i}")
                                currentEdge.append(clickPos)

                                length = 0
                                for j in range(len(currentEdge) - 1):
                                    firstPoint = currentEdge[j]
                                    secondPoint = currentEdge[j + 1]
                                    length += math.sqrt(pow(firstPoint[0] - secondPoint[0], 2) + pow(firstPoint[1] - secondPoint[1], 2))

                                edges.append((edgeStart, i, length))
                                edgeLines += [currentEdge]

                                drawnEdges.append([currentEdge, edgeStart, i])
                                currentEdge = []

                                check = True
                                break
                    if not len(currentEdge) == 0 and not check: # Place pivot on edge
                            print("selected intermediate")
                            currentEdge.append(clickPos)

        gameDisplay.fill((44,64,49))
        if showImg: gameDisplay.blit(img, (xOffset,yOffset))

        mousePos = pygame.mouse.get_pos()
        pygame.draw.circle(gameDisplay, (255, 0, 0), mousePos, 10)

        if not pause:
            if mousePos[0] < display_width/10:
                xOffset += 4
            if mousePos[0] > display_width * 9/10:
                xOffset -= 4
            if mousePos[1] < display_height/10:
                yOffset += 4
            if mousePos[1] > display_height * 9/10:
                yOffset -= 4

        for i in edgeLines: # draw edges
            for j in range(len(i) - 1):
                startPoint = (i[j][0] * display_scale + xOffset, i[j][1] * display_scale + yOffset)
                endPoint = (i[j + 1][0] * display_scale + xOffset, i[j + 1][1] * display_scale + yOffset)
                pygame.draw.line(gameDisplay, (0, 0, 0), startPoint, endPoint, 3)
        if len(currentEdge) > 0: # draw edges being currently made
            for i in range(len(currentEdge) - 1): # draw each line that makes up an edge
                startPoint = (currentEdge[i][0] * display_scale + xOffset, currentEdge[i][1] * display_scale + yOffset)
                endPoint = (currentEdge[i + 1][0] * display_scale + xOffset, currentEdge[i + 1][1] * display_scale + yOffset)
                pygame.draw.line(gameDisplay, (0, 0, 255), startPoint, endPoint, 3)
            
            startPoint = (currentEdge[-1][0] * display_scale + xOffset, currentEdge[-1][1] * display_scale + yOffset)
            pygame.draw.line(gameDisplay, (0, 0, 255), startPoint, mousePos, 3) # draw a line that represents next edge
        for i in range(len(verticies)): # draw verticies
            drawPos = (verticies[i][0] * display_scale + xOffset, verticies[i][1]*display_scale + yOffset)
            pygame.draw.circle(gameDisplay, (255, 0, 0), drawPos, 10)

            text = font.render(str(i), True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = drawPos

            gameDisplay.blit(text, textRect)

        zoomText = font.render("Zoom: " + str(round(display_scale, 2)), True, (255, 255, 255))
        zoomTextRect = zoomText.get_rect()
        zoomTextRect.center = (60, 20)

        clickPos = (round((mousePos[0] - xOffset) / display_scale), round((mousePos[1] - yOffset) / display_scale))
        mouseText = font.render(str(clickPos), True, (255, 255, 255))
        mouseTextRect = mouseText.get_rect()
        mouseTextRect.center = (60, 50)

        gameDisplay.blit(zoomText, zoomTextRect)
        gameDisplay.blit(mouseText, mouseTextRect)

        pygame.display.update()
        clock.tick(60)

main()
pygame.quit()

# build adjacency tables out of edges and verticies lists
adjacency_table = [[0 for x in range(len(verticies))] for y in range(len(verticies))]

for i in edges:
    adjacency_table[i[1]][i[0]] = int(i[2])

verticies = json.dumps(verticies)
drawnEdges = json.dumps(drawnEdges)

data = '{"Wachusett": {\n    "verticies": ' + str(verticies) + ',\n   "edges": ' + str(drawnEdges) + ',\n    "adjacency_table": ' + str(adjacency_table) + '\n}\n}'

file = open("test.json", "w")

file.write(data)

quit()
