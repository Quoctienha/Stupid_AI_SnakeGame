#Credit: https://www.youtube.com/watch?v=QFvqStqPCRU&list=PLG207c58YxEPezChoNZpiFi_m0RM2dLwC&index=15
import pygame
import sys
from pygame.math import Vector2
import random
import heapq
from collections import deque


#Setting
CONTROLLER_WIDTH = 200
cell_size = 40
cell_number = 19
SPEED =150
FONT_NAME = 'Font/Minecraft.ttf'
#color (RGB)
LIGHT_GREEN = (144,238,144)
LIME_GREEN = (50,205,50)
LIGHT_GRAY = (211, 211, 211)
BLUE = (0,87,217)
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
DARK_BLUE = (0,0,139)

#Class fruit
class Fruit:
    def __init__(self):
        #create the x, y position
        # to draw the square
        self.randomize()
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size,cell_size)
        
        #only use one
        screen.blit(self.apple,fruit_rect)              #with graphic
        #pygame.draw.rect(screen ,RED ,fruit_rect) #without graphic
    
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        
#Class snake
class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        
        #body graphics
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha() 
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha() 
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha() 
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha() 
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha() 
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha() 
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        
        #sounds
        self.eat_sound = pygame.mixer.Sound('Sound/eating.wav')
        
    def draw_snake(self):
        #Draw with graphic
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, block in enumerate(self.body):
            #1. we still need a rect for positioning
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            #2. what direction is the face heading
            if index == 0:
                #3. update the snake head
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                #4. update the snake tail
                screen.blit(self.tail, block_rect)
            else:
                #5. update the snake body
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect) #vertical body part
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect) #horizontal body part
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect) # top left
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect) #bottom left
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect) #top right
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect) #bottom left   
        # #Draw without graphic
        # for block in self.body:
        #     #create the x, y position
        #     # to draw the square
        #     x_pos = block.x * cell_size
        #     y_pos = block.y * cell_size
        #     snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        #     pygame.draw.rect(screen ,BLUE ,snake_rect)
    
    
    
    def update_head_graphics(self):
        head_direction = self.body[0] - self.body[1] #tell the direction of the head
        
        if head_direction == Vector2(1, 0):
            self.head = self.head_right
        if head_direction == Vector2(-1, 0):
            self.head = self.head_left
        if head_direction == Vector2(0, 1):
            self.head = self.head_down
        if head_direction == Vector2(0, -1):
            self.head = self.head_up
        
    def update_tail_graphics(self):
        #tell the direction of the tail
        tail_direction = self.body[len(self.body) - 1] - self.body[len(self.body) - 2]
        
        if tail_direction == Vector2(1, 0):
            self.tail = self.tail_right
        if tail_direction == Vector2(-1, 0):
            self.tail = self.tail_left
        if tail_direction == Vector2(0, 1):
            self.tail = self.tail_down
        if tail_direction == Vector2(0, -1):
            self.tail = self.tail_up
        
        
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]       
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

        
    def add_block(self):
        self.new_block = True
    
    def play_eat_sound(self):
        self.eat_sound.play()
    
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
 
class AI:
    def __init__(self):
        pass
     
    def is_position_free(self, position, snake_body):
        # Kiểm tra vị trí có nằm trong grid và không va vào thân rắn không
        return (
            0 <= position.x < cell_number and
            0 <= position.y < cell_number and
            position not in snake_body
        )   
     
    def find_safe_move(self, snake):
        # Tìm một bước đi an toàn nếu không có đường đến quả táo hoặc đuôi
        current_head = snake.body[0]
        for direction in [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]:
            new_head = current_head + direction
            if self.is_position_free(new_head, snake.body):
                return [direction]  # Trả về một bước đi an toàn

        return []  # Nếu không có bước đi an toàn nào, trả về rỗng
    
    
    
    
    def DFS(self, snake, target):
        # Khởi tạo stack DFS với vị trí đầu, thân rắn hiện tại và đường đi
        stack = [(snake.body, [])]  # (body_positions, path)
        visited = set(tuple(part) for part in snake.body)  # Theo dõi các vị trí cơ thể ban đầu

        while stack:
            body_positions, path = stack.pop()
            current_head = body_positions[0]  # Đầu hiện tại của rắn

            # Kiểm tra nếu đầu rắn ở vị trí của quả
            if current_head == target:
                return path

            # Duyệt qua mỗi hướng di chuyển (phải, trái, xuống, lên)
            for direction in [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]:
                new_head = current_head + direction
                new_head_tuple = (new_head.x, new_head.y)

                # Tạo vị trí thân rắn mới bằng cách di chuyển
                new_body_positions = [new_head] + body_positions[:-1]
                
                # Kiểm tra điều kiện: trong bounds, chưa duyệt, và không va vào thân
                if (new_head_tuple not in visited 
                    and 0 <= new_head.x < cell_number 
                    and 0 <= new_head.y < cell_number
                    and self.is_position_free(new_head, new_body_positions[1:])):

                    visited.add(new_head_tuple)
                    stack.append((new_body_positions, path + [direction]))

        # Nếu không tìm thấy đường đi
        return []
   
    def DFS_with_space_creation(self, snake, fruit):
        # Tìm đường đến quả táo
        path_to_fruit = self.DFS(snake, fruit.pos)
        if path_to_fruit:
            return path_to_fruit  # Nếu có đường đến quả táo, đi theo nó

        # Nếu không tìm thấy đường đến quả táo, tìm đường đến đuôi để tạo không gian
        tail_pos = snake.body[-1]  # Vị trí của đuôi rắn
        path_to_tail = self.DFS(snake, tail_pos)
        
        if path_to_tail:
            return path_to_tail  # Đi theo đuôi để tạo không gian

        # Nếu không tìm thấy cả đường đến quả táo và đuôi, tìm một bước an toàn bất kỳ
        return self.find_safe_move(snake)
    
    
    
    
    def BFS(self, snake, target):
        # Khởi tạo hàng đợi BFS với vị trí đầu, thân rắn hiện tại và đường đi
        queue = deque([(snake.body[:], [])])  # (body_positions, path)
        visited = set(tuple(part) for part in snake.body)  # Theo dõi các vị trí cơ thể ban đầu

        while queue:
            body_positions, path = queue.popleft()
            current_head = body_positions[0]  # Đầu hiện tại của rắn

            # Kiểm tra nếu đầu rắn ở vị trí đích
            if current_head == target:
                return path

            # Duyệt qua mỗi hướng di chuyển (phải, trái, xuống, lên)
            for direction in [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]:
                new_head = current_head + direction
                new_head_tuple = (new_head.x, new_head.y)

                # Tạo vị trí thân rắn mới bằng cách di chuyển
                new_body_positions = [new_head] + body_positions[:-1]

                # Kiểm tra điều kiện: trong bounds, chưa duyệt, và không va vào thân
                if (new_head_tuple not in visited and
                    self.is_position_free(new_head, new_body_positions[1:])):

                    visited.add(new_head_tuple)
                    queue.append((new_body_positions, path + [direction]))

        # Nếu không tìm thấy đường đi
        return []
    
    def BFS_with_space_creation(self, snake, fruit):
        # Tìm đường đến quả táo
        path_to_fruit = self.BFS(snake, fruit.pos)
        if path_to_fruit:
            return path_to_fruit  # Nếu có đường đến quả táo, đi theo nó

        # Nếu không tìm thấy đường đến quả táo, tìm đường đến đuôi để tạo không gian
        tail_pos = snake.body[-1]  # Vị trí của đuôi rắn
        path_to_tail = self.BFS(snake, tail_pos)
        
        if path_to_tail:
            return path_to_tail  # Đi theo đuôi để tạo không gian

        # Nếu không tìm thấy cả đường đến quả táo và đuôi, tìm một bước an toàn bất kỳ
        return self.find_safe_move(snake)
    
    
    
    def UCS(self, snake, target):
        # Khởi tạo priority queue với chi phí ban đầu là 0, vị trí đầu, và thân rắn hiện tại
        priority_queue = [(0, tuple((part.x, part.y) for part in snake.body), [])]  # (cost, body_positions, path)
        visited = set(tuple((part.x, part.y) for part in snake.body))  # Theo dõi các vị trí cơ thể ban đầu

        while priority_queue:
            cost, body_positions, path = heapq.heappop(priority_queue)
            current_head = Vector2(body_positions[0][0], body_positions[0][1])  # Tạo lại current_head từ tuple

            # Kiểm tra nếu đầu rắn ở vị trí của quả
            if current_head == target:
                return path

            # Duyệt qua mỗi hướng di chuyển (phải, trái, xuống, lên)
            for direction in [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]:
                new_head = current_head + direction
                new_head_tuple = (new_head.x, new_head.y)

                # Tạo vị trí thân rắn mới bằng cách di chuyển
                new_body_positions = [new_head_tuple] + list(body_positions[:-1])

                # Kiểm tra điều kiện: trong bounds, chưa duyệt, và không va vào thân
                if (new_head_tuple not in visited 
                    and self.is_position_free(new_head, new_body_positions[1:])):
                    
                    #cost mới
                    new_cost = cost + 1
                        
                    # Thêm vị trí mới vào hàng đợi với chi phí tăng thêm 1
                    visited.add(new_head_tuple)
                    heapq.heappush(priority_queue, (new_cost, tuple(new_body_positions), path + [direction]))

        # Nếu không tìm thấy đường đi
        return []
    
    def UCS_with_space_creation(self, snake, fruit):
        # Tìm đường đến quả táo
        path_to_fruit = self.UCS(snake, fruit.pos)
        if path_to_fruit:
            return path_to_fruit  # Nếu có đường đến quả táo, đi theo nó

        # Nếu không tìm thấy đường đến quả táo, tìm đường đến đuôi để tạo không gian
        tail_pos = snake.body[-1]  # Vị trí của đuôi rắn
        path_to_tail = self.UCS(snake, tail_pos)
        
        if path_to_tail:
            return path_to_tail  # Đi theo đuôi để tạo không gian

        # Nếu không tìm thấy cả đường đến quả táo và đuôi, tìm một bước an toàn bất kỳ
        return self.find_safe_move(snake)
    
    
    
    def GREEDY(self, snake, target):
        # Khởi tạo priority queue với khoảng cách ban đầu là 0, vị trí đầu và thân rắn hiện tại
        priority_queue = [(0, tuple((part.x, part.y) for part in snake.body), [])]  # (distance, body_positions, path)
        visited = set(tuple((part.x, part.y) for part in snake.body))  # Theo dõi các vị trí cơ thể đã ghé thăm

        while priority_queue:
            _, body_positions, path = heapq.heappop(priority_queue)
            current_head = Vector2(body_positions[0][0], body_positions[0][1])  # Tạo lại current_head từ tuple

            # Kiểm tra nếu đầu rắn ở vị trí của quả
            if current_head == target:
                return path

            # Duyệt qua mỗi hướng di chuyển (phải, trái, xuống, lên)
            for direction in [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]:
                new_head = current_head + direction
                new_head_tuple = (new_head.x, new_head.y)

                # Tạo vị trí thân rắn mới bằng cách di chuyển
                new_body_positions = [new_head_tuple] + list(body_positions[:-1])

                # Kiểm tra điều kiện: trong bounds, chưa duyệt, và không va vào thân
                if (new_head_tuple not in visited 
                    and self.is_position_free(new_head, new_body_positions[1:])):

                    # Tính khoảng cách Manhattan từ new_head đến vị trí quả
                    distance_to_fruit = abs(new_head.x - target.x) + abs(new_head.y - target.y)
                
                    # Thêm vào hàng đợi ưu tiên, dựa trên khoảng cách đến quả
                    visited.add(new_head_tuple)
                    heapq.heappush(priority_queue, (distance_to_fruit, tuple(new_body_positions), path + [direction]))

        # Nếu không tìm thấy đường đi
        return []
    
    def GREEDY_with_space_creation(self, snake, fruit):
        # Tìm đường đến quả táo
        path_to_fruit = self.GREEDY(snake, fruit.pos)
        if path_to_fruit:
            return path_to_fruit  # Nếu có đường đến quả táo, đi theo nó

        # Nếu không tìm thấy đường đến quả táo, tìm đường đến đuôi để tạo không gian
        tail_pos = snake.body[-1]  # Vị trí của đuôi rắn
        path_to_tail = self.GREEDY(snake, tail_pos)
        
        if path_to_tail:
            return path_to_tail  # Đi theo đuôi để tạo không gian

        # Nếu không tìm thấy cả đường đến quả táo và đuôi, tìm một bước an toàn bất kỳ
        return self.find_safe_move(snake)
    
    
    
    def Astar(self, snake, target):
        # Khởi tạo priority queue với khoảng cách ban đầu là 0, vị trí đầu và thân rắn hiện tại
        priority_queue = [(0,0, tuple((part.x, part.y) for part in snake.body), [])]  # (cost, body_positions, path)
        visited = set(tuple((part.x, part.y) for part in snake.body))  # Theo dõi các vị trí cơ thể đã ghé thăm

        while priority_queue:
            f_cost, g_cost, body_positions, path = heapq.heappop(priority_queue)
            current_head = Vector2(body_positions[0][0], body_positions[0][1])  # Tạo lại current_head từ tuple

            # Kiểm tra nếu đầu rắn ở vị trí của quả
            if current_head == target:
                return path

            # Duyệt qua mỗi hướng di chuyển (phải, trái, xuống, lên)
            for direction in [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]:
                new_head = current_head + direction
                new_head_tuple = (new_head.x, new_head.y)

                # Tạo vị trí thân rắn mới bằng cách di chuyển
                new_body_positions = [new_head_tuple] + list(body_positions[:-1])

                # Kiểm tra điều kiện: trong bounds, chưa duyệt, và không va vào thân
                if (new_head_tuple not in visited 
                    and self.is_position_free(new_head, new_body_positions[1:])):

                    # Tính toán chi phí thực tế (g_cost) và heuristic (h_cost)
                    # if len(path):
                    #     if direction == path[0]:
                    #         g_cost = g_cost + 10
                    #     else:
                    #         g_cost = g_cost + 14
                    # else:
                    #     if direction == snake.direction:
                    #         g_cost = g_cost + 10
                    #     else:
                    #         g_cost = g_cost + 14
                    g_cost = g_cost + 1
                    h_cost = abs(new_head.x - target.x) + abs(new_head.y - target.y)
                
                    # Thêm vào hàng đợi ưu tiên, dựa trên khoảng cách đến quả
                    visited.add(new_head_tuple)
                    heapq.heappush(priority_queue, (g_cost + h_cost, g_cost , tuple(new_body_positions), path + [direction]))

        # Nếu không tìm thấy đường đi
        return []
       
    def Astar_with_space_creation(self, snake, fruit):
        # Tìm đường đến quả táo
        path_to_fruit = self.Astar(snake, fruit.pos)
        if path_to_fruit:
            return path_to_fruit  # Nếu có đường đến quả táo, đi theo nó

        # Nếu không tìm thấy đường đến quả táo, tìm đường đến đuôi để tạo không gian
        tail_pos = snake.body[-1]  # Vị trí của đuôi rắn
        path_to_tail = self.Astar(snake, tail_pos)
        
        if path_to_tail:
            return path_to_tail  # Đi theo đuôi để tạo không gian

        # Nếu không tìm thấy cả đường đến quả táo và đuôi, tìm một bước an toàn bất kỳ
        return self.find_safe_move(snake)    
    
class Main:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
        self.Ai = AI()
        self.state = "STOPPED"
        
        #sounds
        self.game_over_sound = pygame.mixer.Sound('Sound/game_over.wav')
        self.background_sound = pygame.mixer.Sound('Sound/background_music.wav')
    
    def update(self):
        if self.state == "RUNNING":
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()
    
    def play_background_music(self):
        self.background_sound.set_volume(0.5)
        self.background_sound.play(-1)
        
    def draw_elements(self):
        #draw grass
        self.draw_grass()
        #draw the fruit
        self.fruit.draw_fruit()
        #draw the snake
        self.snake.draw_snake()
        #draw score
        self.draw_score()
        #draw menu
        self.draw_controler()
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:          
            #draw a new fruit 
            self.fruit.randomize()
            #add another block to the snake
            self.snake.add_block()
            #play eating sound
            self.snake.play_eat_sound()           
            #prevent fruit spawn on the snake
            for block in self.snake.body:
                if block == self.fruit.pos:
                    self.fruit.randomize()
            
    def check_fail(self):
        #check if snake go out of the screen
        if not 0 <= self.snake.body[0].x < cell_number:          
            self.game_over()
        if not 0 <= self.snake.body[0].y < cell_number:          
            self.game_over()
            
        #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                
    def game_over(self):
        self.game_over_sound.play()
        self.snake.reset() 
        self.fruit.randomize()
        self.state = "STOPPED"
        
    
    def draw_grass(self):
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, LIME_GREEN,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, LIME_GREEN,grass_rect)
    
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)      
        score_surface = score_font.render(score_text, True, BLACK)
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(midright = (score_rect.left, score_rect.centery))
        
        screen.blit(score_surface, score_rect)
        screen.blit(self.fruit.apple, apple_rect)
        
    def draw_controler(self):
        menu_rect = pygame.Rect(cell_size * cell_number, 0, 200, cell_size * cell_number)
        pygame.draw.rect(screen, LIGHT_GRAY, menu_rect)
        
        
    def draw_screen_for_AI(self):
        #color the screen
        screen.fill(LIGHT_GREEN)
        #draw game elements
        self.draw_elements()
        #draw button
        Reset_button.draw_button(screen)
        Pause_button.draw_button(screen)
        Back_button.draw_button(screen)
        
        DFS_button.draw_button(screen)
        BFS_button.draw_button(screen)
        UCS_button.draw_button(screen)
        GREEDY_button.draw_button(screen)
        Astar_button.draw_button(screen)
                
   
class button:
    def __init__(self, image_path, x_pos, y_pos, width, height):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.button_rect = pygame.Rect(x_pos, y_pos, width, height)
        
    def draw_button(self, screen):
        screen.blit(self.image, self.button_rect)
        
    def is_pressed(self):
        mouse_pos = pygame.mouse.get_pos()       
        if self.button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False
    
# Hàm để vẽ văn bản có viền
def draw_text_with_outline(text, font, color, outline_color, position):
    # Render viền
    outline = font.render(text, True, outline_color)
    # Render nội dung bên trong
    text_surface = font.render(text, True, color)

    # Các vị trí xung quanh để tạo viền
    offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
    for offset in offsets:
        screen.blit(outline, (position[0] + offset[0], position[1] + offset[1]))

    # Vẽ nội dung chính giữa
    screen.blit(text_surface, position)   
    
#initilize the game
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((CONTROLLER_WIDTH + cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption('Snake game')
clock = pygame.time.Clock()
score_font = pygame.font.Font(FONT_NAME, 25)
main_font = pygame.font.Font(FONT_NAME, 100)
member_font = pygame.font.Font(FONT_NAME, 30)


#create the objects
main_game = Main()
#main_game.play_background_music()
#event timer
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, SPEED)

#button
Reset_button = button('Graphics/Reset.png', 780, 10, 160, 100)
Pause_button = button('Graphics/Pause.png', 780, 120, 160, 100)
Back_button = button('Graphics/Back.png', 780, 230, 160, 100)

DFS_button = button('Graphics/DFS.png', 780, 340, 160, 32)
BFS_button = button('Graphics/BFS.png', 780, 382, 160, 32)
UCS_button = button('Graphics/UCS.png', 780, 424, 160, 32)
GREEDY_button = button('Graphics/GREEDY.png', 780, 466, 160, 32)
Astar_button = button('Graphics/Astar.png', 780, 508, 160, 32)

#Running the game
def main_menu():
    pygame.display.set_caption('Snake game')
    #background
    Main_menu = pygame.image.load('Graphics/Main_menu_background.webp').convert_alpha()
    Screen_rect = pygame.Rect(0, 0, CONTROLLER_WIDTH + cell_size * cell_number, cell_size * cell_number)
    #button    
    player_button = button('Graphics/Player.png', 400, 330, 160, 100)
    AI_button = button('Graphics/AI.png', 400, 450, 160, 100)
    
    while True:
        #draw background
        screen.blit(Main_menu,Screen_rect)
        #draw text snake game
        draw_text_with_outline('Snake game', main_font, WHITE, BLACK, (200, 50))        
        #draw members
        draw_text_with_outline('22110075 - Ha Quoc Tien', member_font, WHITE, BLACK, (250, 150 ))
        draw_text_with_outline('22110041 - Bui Nguyen An Khang', member_font, WHITE, BLACK, (250, 200 ))
        draw_text_with_outline('22110010 - Nguyen Huynh Quoc Bao', member_font, WHITE, BLACK, (250, 250 ))
        
        #draw button
        player_button.draw_button(screen)
        AI_button.draw_button(screen)
        
        for event in pygame.event.get():
            #close the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_button.is_pressed(): 
                    screen_for_player()
                if AI_button.is_pressed(): 
                    screen_for_AI()
                 
        
        #update all elements
        pygame.display.update()
        clock.tick(60) #framerate

def screen_for_AI():
    
    main_game.snake.reset()
    while True:
        pygame.display.set_caption('Snake game for AI')
        main_game.draw_screen_for_AI() 
        
        if main_game.state == "STOPPED":
            draw_text_with_outline('Chooes a algorithm to continue', member_font, WHITE, BLACK, (100, 150 ))
        
        for event in pygame.event.get():
            #close the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #moving to the right whe the game start           
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back_button.is_pressed(): 
                    main_menu()
                if Reset_button.is_pressed(): 
                    main_game.game_over()
                    
                if DFS_button.is_pressed(): 
                    main_game.state = "RUNNING"
                    DFS_game_loop()                 
              
                if BFS_button.is_pressed(): 
                    main_game.state = "RUNNING"
                    BFS_game_loop()
                
                if UCS_button.is_pressed(): 
                    main_game.state = "RUNNING"
                    UCS_game_loop()

                if GREEDY_button.is_pressed(): 
                    main_game.state = "RUNNING"
                    GREEDY_game_loop() 
                
                if Astar_button.is_pressed(): 
                    main_game.state = "RUNNING"
                    Astar_game_loop()                              
                    
                                  
        #update all elements
        pygame.display.update()
        clock.tick(60) #framerate


def DFS_game_loop():
    paused = False
    pygame.display.set_caption('Snake game DFS')
    while main_game.state == "RUNNING":
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back_button.is_pressed():
                    main_game.game_over()
                    main_menu()
                if Reset_button.is_pressed():
                    main_game.game_over()
                    
                if Pause_button.is_pressed():
                    paused = not paused
                    
        if paused:
            pygame.time.delay(100)
            continue
        directions = main_game.Ai.DFS_with_space_creation(main_game.snake, main_game.fruit)
        if directions:
            for direction in directions:
                main_game.snake.direction = direction
                main_game.update()
                main_game.draw_screen_for_AI()
                pygame.display.update()
                clock.tick(60)
                pygame.time.delay(100)
        else:
            # Cập nhật trạng thái trò chơi và hiển thị thông báo "No solution"
            draw_text_with_outline('No solution', member_font, WHITE, BLACK, (300, 150))
            pygame.display.update()
            pygame.time.delay(2000)  # Hiển thị trong 2 giây
            main_game.game_over()
            

def BFS_game_loop():
    paused = False
    pygame.display.set_caption('Snake game BFS')
    while main_game.state == "RUNNING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back_button.is_pressed():
                    main_game.game_over()
                    main_menu()
                    
                if Reset_button.is_pressed():
                    main_game.game_over()
                    
                if Pause_button.is_pressed():
                    paused = not paused

        if paused:
            pygame.time.delay(100)
            continue

        directions = main_game.Ai.BFS_with_space_creation(main_game.snake, main_game.fruit)
        
        if directions:
            for direction in directions:                
                main_game.snake.direction = direction
                main_game.update()
                main_game.draw_screen_for_AI()
                pygame.display.update()
                clock.tick(60)
                pygame.time.delay(100)
        else:
            # Cập nhật trạng thái trò chơi và hiển thị thông báo "No solution"         
            draw_text_with_outline('No solution', member_font, WHITE, BLACK, (300, 150))
            pygame.display.update()
            pygame.time.delay(2000)
            main_game.game_over()
            

def UCS_game_loop():
    paused = False
    pygame.display.set_caption('Snake game UCS')
    while main_game.state == "RUNNING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back_button.is_pressed():
                    main_game.game_over()
                    main_menu()
                if Reset_button.is_pressed():
                    main_game.game_over()
                   
                if Pause_button.is_pressed():
                    paused = not paused

        if paused:
            pygame.time.delay(100)
            continue

        directions = main_game.Ai.UCS_with_space_creation(main_game.snake, main_game.fruit)
        
        if directions:
            for direction in directions:                
                main_game.snake.direction = direction
                main_game.update()
                main_game.draw_screen_for_AI()
                pygame.display.update()
                clock.tick(60)
                pygame.time.delay(100)
        else:
            # Cập nhật trạng thái trò chơi và hiển thị thông báo "No solution"         
            draw_text_with_outline('No solution', member_font, WHITE, BLACK, (300, 150))
            pygame.display.update()
            pygame.time.delay(2000)
            main_game.game_over()
           
def GREEDY_game_loop():
    paused = False
    pygame.display.set_caption('Snake game GREEDY')
    while main_game.state == "RUNNING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back_button.is_pressed():
                    main_game.game_over()
                    main_menu()
                if Reset_button.is_pressed():
                    main_game.game_over()
                   
                if Pause_button.is_pressed():
                    paused = not paused

        if paused:
            pygame.time.delay(100)
            continue

        directions = main_game.Ai.GREEDY_with_space_creation(main_game.snake, main_game.fruit)
        
        if directions:
            for direction in directions:                
                main_game.snake.direction = direction
                main_game.update()
                main_game.draw_screen_for_AI()
                pygame.display.update()
                clock.tick(60)
                pygame.time.delay(100)
        else:
            # Cập nhật trạng thái trò chơi và hiển thị thông báo "No solution"         
            draw_text_with_outline('No solution', member_font, WHITE, BLACK, (300, 150))
            pygame.display.update()
            pygame.time.delay(2000)
            main_game.game_over() 
            
def Astar_game_loop():
    paused = False
    pygame.display.set_caption('Snake game A*')
    while main_game.state == "RUNNING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back_button.is_pressed():
                    main_game.game_over()
                    main_menu()
                if Reset_button.is_pressed():
                    main_game.game_over()
                   
                if Pause_button.is_pressed():
                    paused = not paused

        if paused:
            pygame.time.delay(100)
            continue

        directions = main_game.Ai.Astar_with_space_creation(main_game.snake, main_game.fruit)
        
        if directions:
            for direction in directions:                
                main_game.snake.direction = direction
                main_game.update()
                main_game.draw_screen_for_AI()
                pygame.display.update()
                clock.tick(60)
                pygame.time.delay(100)
        else:
            # Cập nhật trạng thái trò chơi và hiển thị thông báo "No solution"         
            draw_text_with_outline('No solution', member_font, WHITE, BLACK, (300, 150))
            pygame.display.update()
            pygame.time.delay(2000)
            main_game.game_over()

def screen_for_player():
    pygame.display.set_caption('Snake game for player')
    

    while True:
        #color the screen
        screen.fill(LIGHT_GREEN)
        #draw game elements
        main_game.draw_elements()
        #draw button
        Reset_button.draw_button(screen)
        Pause_button.draw_button(screen)
        Back_button.draw_button(screen)
        
        
        if main_game.state == "STOPPED":
            draw_text_with_outline('Press any keys to continue', member_font, WHITE, BLACK, (150, 150 ))
        
        for event in pygame.event.get():
            #close the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            #moving to the right whe the game start
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if main_game.state == "STOPPED":
                    main_game.state = "RUNNING"
                if event.key == pygame.K_UP and not main_game.snake.direction == Vector2(0, 1):
                    main_game.snake.direction = Vector2(0, -1)              
                if event.key == pygame.K_DOWN and not main_game.snake.direction == Vector2(0, -1):
                    main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and not main_game.snake.direction == Vector2(1, 0):
                    main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and not main_game.snake.direction == Vector2(-1, 0):
                    main_game.snake.direction = Vector2(1, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Reset_button.is_pressed(): 
                    main_game.game_over()
                if Pause_button.is_pressed(): 
                    main_game.state = "STOPPED"
                if Back_button.is_pressed(): 
                    main_menu()
                      
        #update all elements
        pygame.display.update()
        clock.tick(60) #framerate

main_menu()
    

