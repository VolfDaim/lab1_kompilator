import pygame
import sys
import objects


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

    objects.draw_field(screen)
    text_field = objects.inputBox(30, 30, 770, 50, 'Введите команду')
    robot = objects.Robot()

    while True:
        screen.fill((30, 30, 30))

        objects.draw_field(screen)
        text_field.draw(screen)
        robot.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    robot.move(text_field.text)
                    text_field.clean()
                elif event.key == pygame.K_BACKSPACE:
                    text_field.backspace()
                else:
                    text_field.handle_event(event)

        pygame.display.flip()


if __name__ == '__main__':
    main()
