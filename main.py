import pygame
import math
import json

pygame.init()

display_width = 1836
display_height = 762
infinity = 9223372036854775807

feetPerPixel = 14

def dijkstras(start, end, adjacency_matrix):
    verticies = []
    dist = []
    prev = []

    for i in range(len(adjacency_matrix)):
        dist.append(infinity)
        prev.append(None)
        verticies.append(i)
    dist[start] = 0

    while not len(verticies) == 0:
        minDist = infinity # vertex in Q with min distance
        u = 0
        for i in range(len(dist)):
            if dist[i] < minDist and i in verticies:
                minDist = dist[i]
                u = i

        if u == end: # if found target, work backwards to reconstruct path
            path = []
            u = end
            if not prev[u] == None or u == start:
                while not u == None:
                    path.insert(0, u)
                    u = prev[u]
            break

        verticies.remove(u)

        neighbors = [] # calculate all neighbors of current node
        for i in range(len(adjacency_matrix)):
                dst = adjacency_matrix[i][u]
                if not dst == 0:
                    neighbors.append(i)

        for n in neighbors:
            if n in verticies:
                alt = dist[u] + adjacency_matrix[n][u]
                if alt < dist[n]:
                    dist[n] = alt
                    prev[n] = u

    return path

def pathDist(path, adjacency_table):
    distance = 0

    for i in range(len(path) - 1):
        distance += adjacency_table[path[i]][path[i + 1]]
    
    return distance

def get_emissions(distance):
        return distance / 25.7 * 8887;

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Map Editor')

clock = pygame.time.Clock()

def main():
    img = pygame.image.load('bostonmap.png')

    data = json.loads(open("boston.json", "r").read())
    adjacency_table = data["Boston"]["adjacency_table"]
    verticies = data["Boston"]["verticies"]
    edges = data["Boston"]["edges"]
    important_verticies = []

    path = []
    path2 = []

    font = pygame.font.Font("Roboto-Regular.ttf", 20)

    firstPerson = -1
    secondPerson = -1
    destination = -1

    debugLines = False
    debugText = False
    debugVerticies = True

    carpool = False

    vOff = 10;

    d1dist = 0
    d2dist = 0

    bestPath = 0
    worstPath = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    debugLines = not debugLines
                if event.key == pygame.K_t:
                    debugText = not debugText
                if event.key == pygame.K_v:
                    debugVerticies = not debugVerticies
                if event.key == pygame.K_ESCAPE:
                    firstPerson = -1
                    secondPerson = -1
                    destination = -1
                    path = []
                    path2 = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    for i in range(len(verticies)):
                        distance = math.sqrt(pow(verticies[i][0] - mousePos[0], 2) + pow(verticies[i][1] - mousePos[1] - 12, 2))
                        if distance < 10 and (i in important_verticies or debugVerticies):
                            if firstPerson == -1:
                                firstPerson = i
                            elif secondPerson == -1:
                                secondPerson = i
                            else:
                                destination = i
                                print(f"First Person: {firstPerson}, Second Person: {secondPerson}, Destination {destination}")
                                
                                firstToSecond = dijkstras(firstPerson, secondPerson, adjacency_table)
                                firstToDest = dijkstras(firstPerson, destination, adjacency_table)
                                secondToDest = dijkstras(secondPerson, destination, adjacency_table)

                                f2Sdist = pathDist(firstToSecond, adjacency_table)
                                f2Ddist = pathDist(firstToDest, adjacency_table)
                                S2Ddist = pathDist(secondToDest, adjacency_table)

                                if (f2Ddist + S2Ddist > f2Sdist + S2Ddist): # carpool
                                    bestPath = f2Sdist + S2Ddist
                                    worstPath = f2Ddist + S2Ddist
                                    print("Carpool")
                                    carpool = True
                                    path = firstToSecond
                                    path2 = secondToDest
                                    d1dist = f2Sdist + S2Ddist
                                    d2dist = 0
                                else: # dont carpool
                                    worstPath = f2Sdist + S2Ddist
                                    bestPath = f2Ddist + S2Ddist
                                    path = firstToDest
                                    path2 = secondToDest
                                    d1dist = f2Ddist
                                    d2dist = S2Ddist
                                    print("Do not carpool")
                                    carpool = False
                                print(path)
                                print(path2)
                            
        
        gameDisplay.fill((44,64,49))
        gameDisplay.blit(img, (0, 0))

        for i in edges:
            startPoint = i[1]
            endPoint = i[2]

            if debugLines:
                for j in range(len(i[0]) - 1):
                    pygame.draw.line(gameDisplay, (0, 0, 0), (i[0][j][0], i[0][j][1] - vOff), (i[0][j + 1][0], i[0][j+1][1] - vOff), 3)

            for ii in range(len(path) - 1):
                start = path[ii]
                end = path[ii + 1]

                if startPoint == start and endPoint == end:
                    for j in range(len(i[0]) - 1):
                        color = ii / (len(path) - 1) * 255
                        pygame.draw.line(gameDisplay, (0, 255, 0), (i[0][j][0], i[0][j][1] - vOff), (i[0][j + 1][0], i[0][j+1][1] - vOff), 4)
            
            for ii in range(len(path2) - 1):
                start = path2[ii]
                end = path2[ii + 1]

                if startPoint == start and endPoint == end:
                    for j in range(len(i[0]) - 1):
                        color = ii / (len(path2) - 1) * 255
                        pygame.draw.line(gameDisplay, (255, 255, 0), (i[0][j][0], i[0][j][1] - vOff), (i[0][j + 1][0], i[0][j+1][1] - vOff), 4)

        for i in range(len(verticies)): # draw verticies
            if i in important_verticies or debugVerticies:
                if i == firstPerson:
                    pygame.draw.circle(gameDisplay, (0, 255, 0), (verticies[i][0], verticies[i][1] - vOff), 10)
                elif i == secondPerson:
                    pygame.draw.circle(gameDisplay, (255, 255, 0), (verticies[i][0], verticies[i][1] - vOff), 10)
                elif i == destination:
                    pygame.draw.circle(gameDisplay, (0, 0, 255), (verticies[i][0], verticies[i][1] - vOff), 10)
                elif firstPerson == -1 or secondPerson == -1 or destination == -1:
                    pygame.draw.circle(gameDisplay, (255, 0, 0), (verticies[i][0], verticies[i][1] - vOff), 10)
                if debugText:
                    text = font.render(str(i), True, (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.center = (verticies[i][0], verticies[i][1] - vOff)
                    gameDisplay.blit(text, textRect)
        
        pygame.draw.rect(gameDisplay, (255, 255, 255), pygame.Rect(1536, 0, 500, 150))

        routeInfo = font.render("Route Information:", True, (0, 0, 0))
        routeRect = routeInfo.get_rect()
        routeRect.center = (1635, 15)
        gameDisplay.blit(routeInfo, routeRect)

        if not firstPerson == -1 and not secondPerson == -1 and not destination == -1:
            if carpool:
                carInfo = font.render("You should carpool", True, (0, 0, 0))
            else:
                carInfo = font.render("You should not carpool", True, (0, 0, 0))
            carRect = carInfo.get_rect()
            carRect.center = (1670, 40)
            gameDisplay.blit(carInfo, carRect)

            distText = font.render("One person drives " + str(round(d1dist/5280*feetPerPixel, 2)) + " miles", True, (0, 0, 0))
            dist2Text = font.render("One person drives " + str(round(d2dist/5280 * feetPerPixel, 2)) + " miles", True, (0, 0, 0))

            distRect = distText.get_rect()
            distRect.center = (1685, 70)
            gameDisplay.blit(distText, distRect)

            dist2Rect = dist2Text.get_rect()
            dist2Rect.center = (1685, 90)
            gameDisplay.blit(dist2Text, dist2Rect)

            carbon = font.render("Amount of carbon saved: ", True, (0, 0, 0))
            carbonSaved = (get_emissions(worstPath) - get_emissions(bestPath)) / get_emissions(worstPath) * 100
            percent = font.render(str(round(carbonSaved, 1)) + "%", True, (0, 0, 0))
            carbonRect = carbon.get_rect()
            carbonRect.center = (1685, 120)
            percentRect = percent.get_rect()
            percentRect.center = (1685, 140)

            if carpool:
                gameDisplay.blit(carbon, carbonRect)
                gameDisplay.blit(percent, percentRect)

        pygame.display.update()
        clock.tick(60)

main()
pygame.quit()
quit()
