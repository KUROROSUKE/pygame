import pygame
import sys
import json
from random import randint
from collections import Counter
import select_use

ai_hand, pl_hand = [],[]
cards, ai_cards = [], []
ai_selected_cards, ai_selected_places = [], [0,0,0,0,0,0,0,0]
pl_selected_cards, pl_selected_places = [], [0,0,0,0,0,0,0,0]
ai_point,pl_point = 0, 0
make_material = {}
turn = "pl"

elementToNumber = {"H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10,"Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20,"Fe": 26, "Cu": 29, "Zn": 30, "I": 53}
elements = ['H'] * 30 + ['O'] * 25 + ['C'] * 20 + ['He', 'Li', 'Be', 'B', 'N', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Fe', 'Cu', 'Zn', 'I']

start_x, start_y = 40, 100
spacing = 110

with open('compound/standard.json', 'r', encoding='utf-8') as file:
    elements_info = json.load(file)['material']
    
components_info = [elem['components'] for elem in elements_info]

pygame.init()

width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('元素ゲーム')

WHITE = (255, 255, 255)

japanese_font_path = "font/BIZ-UDGothicR.ttc"
japanese_font = pygame.font.Font(japanese_font_path, 20)


def pl_generate():
    global pl_point,pl_selected_cards,pl_selected_places
    element_info = search(Counter(pl_selected_cards))
    if element_info:
        generate_element_info = [element_info['name'],element_info['formula']]
        pl_point += element_info['point']
        pl_exchange()
        print(generate_element_info)
        return generate_element_info
    pl_selected_cards = []
    pl_selected_places = [0,0,0,0,0,0,0,0]

def pl_exchange():
    global pl_hand,pl_selected_cards,pl_selected_places
    for num,select in enumerate(pl_selected_places):
        if select:
            pl_hand[num] = get_random_card()
    pl_selected_cards = []
    pl_selected_places = [0,0,0,0,0,0,0,0]

def ai_generate():
    global ai_point,ai_selected_cards,ai_selected_places
    
    element_info = search(Counter(ai_selected_cards))
    if element_info:
        generate_element_info = [element_info['name'], element_info['formula']]
        ai_point += element_info['point']
        ai_exchange()
        return generate_element_info
    ai_selected_cards = []
    ai_selected_places = [0,0,0,0,0,0,0,0]

def ai_exchange():
    global ai_hand,ai_selected_cards,ai_selected_places
    for num,select in enumerate(ai_selected_places):
        if select:
            ai_hand[num] = get_random_card()
    ai_selected_cards = []
    ai_selected_places = [0,0,0,0,0,0,0,0]

def ai_select_AI():
    global ai_selected_cards, ai_selected_places
    # AIの行動を予測して処理する
    action, cards_to_select = select_use.predict(ai_hand)
    
    for num,card in enumerate(ai_hand):
        if card in cards_to_select:
            ai_selected_cards.append(card)
            ai_selected_places[num] = 1
            cards_to_select.remove(card)
    return action

def ai_select_COM():#古いほうの奴。AIを使わないので、無限ループに陥らないように使う。
    create_materials = can_make_materials()
    if create_materials:
        max_point = 0
        select_cards = {}
        for create_material in create_materials:
            if max_point < create_material['point']:
                max_point = create_material['point']
                select_cards = create_material['components']
        select_cards = dict_to_array(select_cards)
        for num,card in enumerate(ai_hand):
            if card in select_cards:
                ai_selected_cards.append(card)
                ai_selected_places[num] = 1
                select_cards.remove(card)
        return "generate"
    else:
        element_counts = Counter(elements)
        least_frequent = min(element_counts.values())
        select_cards = {key: count for key, count in element_counts.items() if count == least_frequent}
        select_cards = dict_to_array(select_cards)
        for num,card in enumerate(ai_hand):
            if card in select_cards:
                ai_selected_cards.append(card)
                ai_selected_places[num] = 1
                select_cards.remove(card)
        return "exchange"

def search(selected_cards):
    generate_element_num = None
    for num,tmp_components in enumerate(components_info):
        if selected_cards == tmp_components:
            generate_element_num = num + 1
    if generate_element_num:
        return elements_info[generate_element_num - 1]

def can_make_materials():
    element_counter = Counter(ai_hand)
    possible_compounds = []
    for compound in elements_info:
        required_elements = compound['components']
        compound_counter = Counter(required_elements)
        if all(element_counter.get(elem, 0) >= count for elem, count in compound_counter.items()):
            possible_compounds.append(compound)
    return possible_compounds

def get_random_card():
    return elements[randint(0,len(elements)-1)]

def initialize_hand():
    for _ in range(8):
        pl_hand.append(get_random_card())
        ai_hand.append(get_random_card())

def dict_to_array(components):
    result_list = []
    for key, value in components.items():
        result_list.extend([key] * value)
    return result_list

def pl_generate_action():
    global pl_point
    generate_material_info = pl_generate()
    update_card_objects()
    win_check()
    ai_turn()

def update_card_objects():
    global cards, ai_cards
    cards.clear()
    for index, element in enumerate(pl_hand):
        if element in card_images:
            image_path = card_images[element]
            position = (start_x + index * spacing, start_y + 200)
            card = Card(element, image_path, position, index)
            cards.append(card)
    
    ai_cards.clear()
    for index, element in enumerate(ai_hand):
        if element in card_images:
            image_path = card_images[element]
            position = (start_x + index * spacing, start_y)
            ai_card = AICard(element, image_path, position)
            ai_cards.append(ai_card)

def update_pl_point_view():
    text_surf = japanese_font.render(f"プレイヤーのポイント： {pl_point}", True, (0, 0, 0))
    return text_surf

def update_ai_point_view():
    text_surf = japanese_font.render(f"AIのポイント： {ai_point}", True, (0, 0, 0))
    return text_surf

def win_check():
    global turn, winner
    if pl_point >= 250:
        turn = "end"
        winner = "プレイヤーの勝利"
    elif ai_point >= 250:
        turn = "end"
        winner = "AIの勝利"

def exchange_cards():
    if turn != "end" and any(pl_selected_places):
        pl_exchange()
        update_card_objects()
        win_check()
        ai_turn()

def generate_material():
    if turn != "end" and any(pl_selected_places):
        pl_generate_action()

def ai_turn():
    global ai_point
    if turn != "end":
        action = ai_select_AI()
        if action == "generate":
            info = ai_generate()
            if not info:
                action = ai_select_COM()
                if action == "generate":
                    info = ai_generate()
                elif action == "exchange":
                    ai_exchange()
        elif action == "exchange":
            ai_exchange()
        
        update_card_objects()

def draw_winner_message(screen, winner_message):
    if winner_message:
        font = pygame.font.Font(japanese_font_path, 64)
        text_surf = font.render(winner_message, True, (255, 0, 0))  # 赤色で勝利メッセージを表示
        text_rect = text_surf.get_rect(center=(width // 2, height // 2))
        screen.blit(text_surf, text_rect)


class Button:
    def __init__(self, text, position, size, callback):
        self.text = text
        self.position = position
        self.size = size
        self.callback = callback
        self.font = pygame.font.Font(japanese_font_path, 36)
        self.rect = pygame.Rect(position, size)
        self.text_surf = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def on_click(self):
        self.callback()

class Card(pygame.sprite.Sprite):
    def __init__(self, element, image_path, position, index):
        super().__init__()
        self.element = element
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.index = index
        self.is_selected = False

    def draw(self, surface):
        if self.is_selected:
            image = pygame.transform.scale(self.original_image, (int(self.rect.width * 1.3), int(self.rect.height * 1.3)))
            rect = image.get_rect(center=self.rect.center)
        else:
            image = self.original_image
            rect = self.rect
        surface.blit(image, rect.topleft)

    def on_click(self):
        global pl_selected_cards, pl_selected_places
        if pl_selected_places[self.index] == 1:
            pl_selected_cards.remove(self.element)
            pl_selected_places[self.index] = 0
            self.is_selected = False
        else:
            pl_selected_cards.append(self.element)
            pl_selected_places[self.index] = 1
            self.is_selected = True

class AICard(pygame.sprite.Sprite):
    def __init__(self, element, image_path, position):
        super().__init__()
        self.element = element
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.is_selected = False

    def draw(self, surface):
        if self.is_selected:
            image = pygame.transform.scale(self.original_image, (int(self.rect.width * 1.2), int(self.rect.height * 1.2)))
            rect = image.get_rect(center=self.rect.center)
        else:
            image = self.original_image
            rect = self.rect
        surface.blit(image, rect.topleft)

card_images = {
    "H" :  "image/1.png",
    "He":  "image/2.png",
    "Li":  "image/3.png",
    "Be":  "image/4.png",
    "B" :  "image/5.png",
    "C" :  "image/6.png",
    "N" :  "image/7.png",
    "O" :  "image/8.png",
    "F" :  "image/9.png",
    "Ne": "image/10.png",
    "Na": "image/11.png",
    "Mg": "image/12.png",
    "Al": "image/13.png",
    "Si": "image/14.png",
    "P" : "image/15.png",
    "S" : "image/16.png",
    "Cl": "image/17.png",
    "Ar": "image/18.png",
    "K" : "image/19.png",
    "Ca": "image/20.png",
    "Fe": "image/26.png",
    "Cu": "image/29.png",
    "Zn": "image/30.png",
    "I" : "image/53.png",
}

buttons = [
    Button("交換", (50, 500), (200, 50), exchange_cards),
    Button("生成", (300, 500), (200, 50), generate_material)
]


initialize_hand()
update_card_objects()

winner = None  # 勝利者情報を保持する変数を定義

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and turn != "end":
            for card in cards:
                if card.rect.collidepoint(event.pos):
                    card.on_click()
            for button in buttons:
                if button.rect.collidepoint(event.pos) and any(pl_selected_places):
                    button.on_click()

    screen.fill(WHITE)
    for card in cards:
        card.draw(screen)
    for button in buttons:
        button.draw(screen)
    for ai_card in ai_cards:
        ai_card.draw(screen)

    screen.blit(update_pl_point_view(), (10, 210))
    screen.blit(update_ai_point_view(), (10, 40))

    if winner:
        draw_winner_message(screen, winner)

    pygame.display.flip()
