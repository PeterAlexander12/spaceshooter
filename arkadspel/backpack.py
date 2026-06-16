# import pygame
# 
# BTN_W, BTN_H = 80, 30
# 
# equipped_id = None
# if lage == "backpack":
#     def get_button_rect(i):
#         y = ITEM_Y + i * (ITEM_H + GAP)
#         item_rect = pygame.Rect(ITEM_X, y, ITEM_W, ITEM_H)
#         return pygame.Rect(item_rect.right - BTN_W - 10,
#                            item_rect.y + (ITEM_H - BTN_H)//2,
#                            BTN_W, BTN_H)
# 
#     def draw(mouse_pos):
#         screen.fill((30,30,40))
#         for i, w in enumerate(weapons):
#             y = ITEM_Y + i * (ITEM_H + GAP)
#             item_rect = pygame.Rect(ITEM_X, y, ITEM_W, ITEM_H)
#             bg = (60,100,60) if w["id"] == equipped_id else (50,50,70)
#             pygame.draw.rect(screen, bg, item_rect, border_radius=6)
#             name = font.render(w["name"], True, (230,230,230))
#             screen.blit(name, (item_rect.x+8, item_rect.y+10))
#             btn = get_button_rect(i)
#             hover = btn.collidepoint(mouse_pos)
#             color = (200,200,200) if hover else (170,170,170)
#             pygame.draw.rect(screen, color, btn, border_radius=6)
#             txt = "Unequip" if w["id"] == equipped_id else "Equip"
#             screen.blit(font.render(txt, True, (0,0,0)), (btn.x+10, btn.y+6))
#         info = font.render(f"Equipped: {equipped_id or 'None'} (press SPACE to use)", True, (220,220,220))
#         screen.blit(info, (20, H-40))
# 
#     def use_equipped():
#         if not equipped_id:
#             print("No weapon equipped.")
#         else:
#             print(f"Using {equipped_id}!")
# 
#     def main():
#         global equipped_id
#         running = True
#         while running:
#             mouse_pos = pygame.mouse.get_pos()
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                     # click: toggle equip/unequip for the clicked weapon's button
#                     for i, w in enumerate(weapons):
#                         if get_button_rect(i).collidepoint(event.pos):
#                             if equipped_id == w["id"]:
#                                 equipped_id = None     # unequip
#                                 print(f"Unequipped {w['name']}")
#                         else:
#                             equipped_id = w["id"]  # equip
#                             print(f"Equipped {w['name']}")
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         use_equipped()
#             draw(mouse_pos)
#             pygame.display.flip()
#             clock.tick(60)
#         pygame.quit()
#         sys.exit()
# 
# if __name__ == "__main__":
#     main()