# This is a sample Python script.
from game_classes import Card, Deck
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    real_card = Card(5,)
    real_deck = Deck()
    #real_deck.shuffle_deck()
    #real_deck.draw_card()
    for i in range(10):
        card = real_deck.draw_card()
        print(card)
    real_deck.print_discard()
    real_deck.print_deck()
    real_deck.reveal_card()

    #real_deck.reveal_card()
    #real_deck.print_deck()
    #print(random.random())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
