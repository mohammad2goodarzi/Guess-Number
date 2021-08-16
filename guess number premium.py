import time
import pygame
import random


def game(position=(40, 65)):
    current_round.clear()
    for i in range(5):
        x, y = position
        position2 = (x + 25, y)
        current_round.append(position)
        pygame.draw.line(screen, (250, 250, 250), position, position2, 2)
        position = (x + 30, y)


def hint(guess):
    flags = []
    list1 = list(guess)
    list2 = list(main_number)
    for i in range(len(list2)):
        if list2[i] == list1[i]:
            flags.append(1)
            list1[i] = None
            list2[i] = None
    for i in range(len(list2)):
        if list2[i] is None:
            continue
        obj1 = list2[i]
        if list1[i] == obj1:
            flags.append(1)
            list1[i] = None
            list2[i] = None
        else:
            if obj1 in list1:
                flags.append(0)
                list1[list1.index(obj1)] = None
                list2[i] = None
    flags.sort()
    flags.reverse()
    return flags


def submit():
    the_guess = ''.join(current_guess)
    flags = hint(the_guess)
    # print(flags)
    x, y = current_round[-1]
    x += 28
    y -= 27
    for i in range(len(flags)):
        if flags[i] == 1:
            image = pygame.image.load(r'D:\green circle.png')
            screen.blit(image, (x, y))
            x += 23
        else:
            image = pygame.image.load(r'D:\yellow circle.png')
            screen.blit(image, (x, y))
            x += 23
    if the_guess == main_number:
        return True
    return False


def back(i):
    position = current_round[i - 1]
    pygame.draw.rect(screen, (0, 0, 0), (position[0] , position[1] - 30, 30, 30))
    return i - 1


def input_number(i, n):
    text = font.render(n, True, (255, 121, 77))
    screen.blit(text, (current_round[i][0] + 4, current_round[i][1] - 29))
    return i + 1


def numbers_placement():
    started_position = (315, 320)
    for i in range(4):
        for j in range(3):
            position1 = (started_position[0] + (j * (50 + 10)), started_position[1] + (i * (50 + 10)))
            position2 = (position1[0] + 50, position1[1] + 50)
            if i * 3 + j == 9:
                the_list1.append(['submit', [position1, position2]])
            elif i * 3 + j == 10:
                the_list1.append(['0', [position1, position2]])
            elif i * 3 + j == 11:
                the_list1.append(['back', [position1, position2]])
            else:
                the_list1.append([str(i * 3 + j + 1), [position1, position2]])
    the_dict1 = dict(the_list1)

    for i in range(4):
        for j in range(3):
            position = the_list1[i * 3 + j][1][0]
            pygame.draw.rect(screen, (250, 250, 250), (position[0], position[1], 50, 50))
            if i * 3 + j == 9:
                image = pygame.image.load(r'D:\tick2.png')
                screen.blit(image, (position[0], position[1]))
            elif i * 3 + j == 10:
                text = font.render('0', True, (10, 10, 10))
                screen.blit(text, (position[0] + 16, position[1] + 8))
            elif i * 3 + j == 11:
                image = pygame.image.load(r'D:\back button.png')
                screen.blit(image, (position[0], position[1]))
            else:
                text = font.render(str(i * 3 + j + 1), True, (10, 10, 10))
                screen.blit(text, (position[0] + 16, position[1] + 8))
    return the_dict1


def selected_number(position):
    x, y = position
    for i in the_dict:
        p1 = the_dict[i][0]
        p2 = the_dict[i][1]
        if p1[0] < x < p2[0] and p1[1] < y < p2[1]:
            return i
    return None


pygame.init()

done, done2 = False, False
r1, r2 = 800, 560
entered_Resolution = (r1, r2)
screen = pygame.display.set_mode(entered_Resolution)

main_number = ''.join([random.choice('0123456789') for j in range(5)])
font = pygame.font.Font(None, 50)

the_list1 = []
the_dict = numbers_placement()
current_round = []
current_guess = []
x, y = 40, 65
game()
rounds = 1
y += 45
# print(current_round)
i = 0
while not done:
    if done2:
        time.sleep(3)
        done = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONUP:
            mousePosition = pygame.mouse.get_pos()
            number = selected_number(mousePosition)
            if number:
                if number == 'back':
                    if i != 0:
                        i = back(i)
                        current_guess.pop(i)
                elif number == 'submit':
                    if i == 5:
                        i = 0
                        if submit():
                            print(main_number)
                            print('you win!!!')
                            text = font.render('the number was: ' + main_number, True, (10, 200, 10))
                            screen.blit(text, (200, 270))
                            done2 = True
                        else:
                            if rounds < 10:
                                pos = (x, y)
                                game(pos)
                                current_guess.clear()
                                rounds += 1
                                y = (y // 244) * -225 + (y + 45)
                                x = (rounds // 5) * 380 + 40
                            else:
                                print('you lose!!!')
                                text = font.render('the number was: ' + main_number, True, (200, 200, 10))
                                screen.blit(text, (200, 270))
                                done2 = True
                                print(main_number)
                else:
                    if i < 5:
                        i = input_number(i, number)
                        current_guess.append(number)

    pygame.display.flip()
