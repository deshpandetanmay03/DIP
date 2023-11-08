from modules import pygame, sys
import math
import input_points
import tsp
import image_process

def draw_arrow(screen, start_pos, end_pos):
    color = (255, 0, 255)
    arrowhead_size = 15
    rotation = math.atan2(start_pos[1] - end_pos[1], end_pos[0] - start_pos[0]) + math.pi/2
    pygame.draw.polygon(screen, color, ((end_pos[0] + arrowhead_size * math.sin(rotation),
                                          end_pos[1] + arrowhead_size * math.cos(rotation)),
                                         (end_pos[0] + arrowhead_size * math.sin(rotation - 2.0944),
                                          end_pos[1] + arrowhead_size * math.cos(rotation - 2.0944)),
                                            end_pos,
                                         (end_pos[0] + arrowhead_size * math.sin(rotation + 2.0944),
                                          end_pos[1] + arrowhead_size * math.cos(rotation + 2.0944)),
                                        ))
pygame.init()
# Load the background image and scale it to fit the screen size
background = image_process.process_image("dip/input/2.TIF")
shape = background.shape[:2]

screen_width = 800 # get from array
screen_height = 600 # get from array

scale = min(shape[0]//screen_height, shape[1]//screen_width)

background = pygame.surfarray.make_surface(background)
background = pygame.transform.smoothscale(background, (screen_width*scale, screen_height*scale))

screen = pygame.display.set_mode((screen_width*scale, screen_height*scale))
# screen = pygame.display.set_mode((screen_width, screen_height))

# Create an empty list to store the selected points
points = []

# stages of the program
stage = 0

# Define the main loop
running = True
while running:
    # Fill the screen with the background image
    screen.blit(background, (0, 0))

    if stage == 0:

        if input_points.add_point(points, pygame.event.get()) == 0:
            if len(points) == 0:
                running = False
            stage = 1

        # Draw circles for each point in the points list
        for point in points:
            pygame.draw.circle(screen, (255, 63, 127), point, 5)

    elif stage == 1:
        labels, number_of_clusters = input_points.clustered(points)
        clusters = {i: [p for p,l in zip(points, labels) if l == i] for i in range(number_of_clusters)}

        import concurrent.futures

        def process_cluster(key):
            return key, tsp.tsp(clusters[key])

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for key, result in executor.map(process_cluster, clusters.keys()):
                clusters[key] = result

        cluster_centers = [tsp.mean_point(screen, points) for points in clusters.values()]
        cluster_centers = tsp.tsp(cluster_centers)

        stage = 2

    elif stage == 3:
        for event in pygame.event.get():
            # If the user clicks the close button, exit the loop
            if event.type == pygame.QUIT:
                stage = 4
        for label, points in clusters.items():
            if len(points) == 1:
                pygame.draw.circle(screen, (255, 0, 255), points[0], 5)
            else:
                pygame.draw.polygon(screen, (255, (255//(max(1, number_of_clusters-1)))*label, 0), points, 5)

        if len(cluster_centers) == 1:
            pygame.draw.circle(screen, (255, 127, 255), cluster_centers[0], 5)
        else:
            pygame.draw.polygon(screen, (255, 127, (255//(max(1, number_of_clusters-1)))*label), cluster_centers, 5)
        for i in range(len(cluster_centers)):
            draw_arrow(screen, cluster_centers[i-1], cluster_centers[i])
        pygame.draw.circle(screen, (127, 255, 127), cluster_centers[0], 20, 5)
    elif stage == 2:
        for label, points in clusters.items():
            if len(points) == 1:
                pygame.draw.circle(screen, (255, 0, 255), points[0])
            else:
                pygame.draw.polygon(screen, (255, (255//(max(1, number_of_clusters-1)))*label, 0), points)
        for event in pygame.event.get():
            # If the user clicks the close button, exit the loop
            if event.type == pygame.QUIT:
                stage = 3
    else:
        running = False

    # Update the display
    pygame.display.update()

# Quit pygame and sys modules
pygame.quit()
sys.exit()
