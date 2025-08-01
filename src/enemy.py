# src/enemy.py
import pygame
import random
from config import WIDTH
pygame.font.init()

words = ['summer', 'define', 'dog', 'catch', 'soda', 'list', 'leaf', 'bell', 'byte', 'cute', 'circle', 'red', 'angle', 'reset', 'cool', 'class', 'iterator', 'chat', 'fact', 'object', 'cancel', 'mop', 'speak', 'bash', 'avocado', 'trap', 'fun', 'world', 'chem', 'atom', 'keyboard', 'lake', 'panel', 'function', 'dance', 'break', 'fish', 'wing', 'tape', 'admin', 'null', 'frog', 'start', 'terminal', 'blue', 'soap', 'package', 'bit', 'fireball', 'monster', 'stack', 'event', 'bio', 'quick', 'screen', 'bank', 'past', 'trip', 'timer', 'lemon', 'drop', 'barn', 'pink', 'upgrade', 'pop', 'dust', 'value', 'lava', 'jeep', 'disk', 'storm', 'variable', 'network', 'bite', 'json', 'clam', 'mode', 'lambda', 'ship', 'quiet', 'planet', 'animate', 'rain', 'clay', 'figure', 'term', 'crab', 'apple', 'snake', 'mint', 'cola', 'dragon', 'log', 'fire', 'fight', 'while', 'fusion', 'score', 'block', 'song', 'clap', 'grid', 'goal', 'html', 'top', 'slow', 'buzz', 'luck', 'must', 'beep', 'scale', 'float', 'pirate', 'hop', 'kangaroo', 'gap', 'line', 'loop', 'roll', 'juice', 'bed', 'milk', 'bat', 'band', 'java', 'door', 'rest', 'lazy', 'rat', 'coin', 'film', 'page', 'click', 'operator', 'hall', 'charm', 'golf', 'energy', 'math', 'grape', 'black', 'star', 'word', 'holiday', 'select', 'candy', 'run', 'graphics', 'horn', 'sandwich', 'car', 'sand', 'game', 'map', 'dream', 'light', 'raise', 'palm', 'net', 'echo', 'vast', 'decoder', 'ball', 'node', 'maze', 'debug', 'bread', 'wind', 'jar', 'drum', 'print', 'sugar', 'display', 'command', 'build', 'awesome', 'snap', 'zoom', 'sun', 'farm', 'random', 'dark', 'grip', 'drift', 'button', 'flash', 'ruby', 'solo', 'fan', 'parallel', 'club', 'jump', 'import', 'snip', 'serve', 'east', 'glass', 'west', 'space', 'test', 'watch', 'tip', 'rock', 'tap', 'nap', 'brick', 'fast', 'flap', 'input', 'pen', 'exam', 'cell', 'tool', 'format', 'count', 'hill', 'golden', 'backpack', 'happy', 'tree', 'snow', 'rope', 'plant', 'desk', 'data', 'cake', 'args', 'card', 'best', 'check', 'alert', 'bird', 'refresh', 'fork', 'cat', 'umbrella', 'moon', 'bike', 'bold', 'lucky', 'smile', 'book', 'quiz', 'compile', 'hat', 'note', 'bug', 'element', 'picture', 'zip', 'nest', 'lens', 'mouse', 'rust', 'base', 'winter', 'code', 'table', 'rice', 'yarn', 'magic', 'ping', 'mask', 'clip', 'lamp', 'chip', 'bark', 'kick', 'green', 'window', 'return', 'tune', 'howl']

font_enemy = pygame.font.Font(None, 32)

class Enemy:
    def __init__(self):
        self.word = random.choice(words)
        self.x = random.randint(50, WIDTH - 100)
        self.y = -50
        self.speed = random.randint(1, 3)
        self.rect = pygame.Rect(self.x, self.y, 100, 40)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 0, 0), self.rect, border_radius=8)
        text = font_enemy.render(self.word, True, (255, 255, 255))
        surface.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))
