import os
import time
import algorithms
import rich
from rich.console import Console;c=Console()
from rich.text import Text
from math import floor
from tzlocal import get_localzone

import random
#random.seed(69420)

# >>> init >>>
c = Console()
suit = ['♡', '♤', '♧', '♢']
theme = rich.style.Style(color='red',bgcolor='white')
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
#dealer_hand = []
#player_hand = []
user_balance = 1000
d_balance = 10000000
prize_pool = 0
turn = 0
bet = 0
# <<< init <<<

def get_local_currency():  # TODO
    #euro = ['Austria','Belgium','Cyprus','Estonia','Finland','France','Germany','Greece','Ireland','Italy','Latvia',                    'Lithuania','Luxembourg','Malta','Netherlands','Portugal','Spain','Slovenia','Slovakia']
    #pound = []

    tz = str(get_localzone())
    if 'Europe' in tz and 'London' not in tz:
        return '€'
    elif 'Europe' in tz and 'London' in tz:
        return '£'
    else:
        return '$'
cur = get_local_currency()

def rematch():
    """Initialise new game
    """
    global deck, dealer_hand, player_hand, prize_pool, turn, bet
    dealer_hand = []
    player_hand = []
    prize_pool = 0
    turn = 0
    bet = 0
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    thegame()

def wipe():
    """Clear the terminal.
    """
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('CLS') # or whatever idc windows lol
        
def logo():
    """Print logo.
    """
    global c
    wipe()
    c.print(' L')
    time.sleep(0.1)
    wipe()
    c.print(' L E')
    time.sleep(0.1)
    wipe()
    c.print(' L E O')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \'')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B                ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L              ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L A            ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L A C          ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L A C K        ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L A C K J      ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L A C K J A    ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L A C K J A C  ')
    time.sleep(0.1)
    wipe()
    c.print(' L E O \' S   B L A C K J A C K')
    time.sleep(0.4)
    wipe()
    time.sleep(0.4)
    c.print(' L E O \' S   B L A C K J A C K')
    time.sleep(0.4)
    wipe()
    time.sleep(0.4)
    c.print(' L E O \' S   B L A C K J A C K')
    time.sleep(0.8)
    wipe()
    time.sleep(0.4)

def prize_status():
    """
    Show prize pool and balance
    """
    global user_balance, prize_pool, cur
    c.print(f'Prize pool: {cur}{prize_pool}\nBalance: {cur}{user_balance}')

def betting(bet):
    """
    Betting function. Checks if bet amount is valid then adds to prize pool.

    Args:
        bet ([int]): bet amount
    """
    wipe()
    global user_balance, d_balance, prize_pool, cur
    try:
        bet = int(input(f'Enter bet amount (Current balance: {cur}{user_balance}): '))
        if 0 < bet <= user_balance:
            user_balance -= bet
            d_balance -= bet
            prize_pool += 2 * bet
            prize_status()
        else:
            c.print('Invalid amount.')
            time.sleep(2)
            betting(bet)
    except:
        c.print('Invalid character inserted.')
        time.sleep(2)
        betting(bet)

def deal_init():
    """
    First round deal. Shuffles deck the pops a card, then for values > 10 convert them to face cards

    Returns:
        list: list containing a player's hand
    """
    global deck
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        if card == 11: 
            card = 'J'
        elif card == 12:
            card = 'Q'
        elif card == 13:
            card = 'K'
        elif card == 14:
            card = 'A'
        hand.append(card)
    return hand

def hit_card(hand):
    """Pops a single card from the deck then adds to a player's hand

    Args:
        hand (list): A player's hand

    Returns:
        hand: list containing a player's cards with a newly-added card
    """
    global deck
    card = deck.pop()
    if card == 11: 
        card = 'J'
    elif card == 12:
        card = 'Q'
    elif card == 13:
        card = 'K'
    elif card == 14:
        card = 'A'
    hand.append(card)
    return hand

def double_card(hand, user_balance):
    """Pops two cards from the deck and doubles the prize pool.

    Args:
        hand ([type]): [description]
        user_balance ([type]): [description]

    Returns:
        list: list containing a player's cards with two newly-added cards
    """
    global deck, prize_pool, bet, d_balance
    user_balance -= bet
    d_balance -= bet
    prize_pool *= 2
    for i in range(2):
        card = deck.pop()
        if card == 11: 
            card = 'J'
        elif card == 12:
            card = 'Q'
        elif card == 13:
            card = 'K'
        elif card == 14:
            card = 'A'
        hand.append(card)
    return hand

def total(hand):
    """
    Calculates the total sum of a player's hand.

    Args:
        hand (list): A list containing a player's cards

    Returns:
        int: sum of all the cards a player has.
    """
    total = 0
    for card in hand:
        if type(card) is str:
            if card == 'J' or card == 'Q' or card == 'K':
                total += 10
            elif card == 'A':
                total += 11
        else:
            total += card
        
        if card == 'A' and total > 21:
            total -= 10
    return total

def dealer_win(d_hand, p_hand):
    """
    Checks win condition for dealer. If dealer meets the win condition, returns True, and if player meets the win condition, returns False. If for some reason neither person meets the win condition, returns a 'Draw'.

    Args:
        d_hand (list): List containing dealer's hand
        p_hand (list): List containing player's hand

    Returns:
        bool or str: Win condition for dealer
    """
    sum_d_hand = total(d_hand)
    sum_p_hand = total(p_hand)
    
    if sum_d_hand > 21 or sum_p_hand > 21:
        if sum_d_hand > 21:
            return False
        else:
            return True       
    elif sum_d_hand <= 21 and sum_p_hand <= 21:
        if sum_d_hand > sum_p_hand:
            return True
        else:
            return False
    elif sum_d_hand == sum_p_hand:
        return 'Draw'

def print_cards(hand, suit, term_width=49):
    """
    Returns a f-string for every card from a player's hand. Looks pretty when printed. Scales with respect to the width of the terminal.

    Args:
        hand (list): List containing a player's hand
        suit (list): List containing a set of suits
        term_width (int, optional): Terminal width for scaling purpose. Defaults to 49.

    Returns:
        str: F-string containing the pretty card visuals
    """
    border = {'v_bar': '│',
              'h_bar': '─',
              'top_left': '┌',
              'top_centre': '┬',
              'top_right': '┐',
              'mid_left': '├',
              'mid_centre': '┼',
              'mid_right': '┤',
              'bot_left': '└',
              'bot_centre': '┴',
              'bot_right': '┘'
              }
    space = " "
    n_cards = len(hand)
    empty = ''
    top = ''
    mid_left = f''
    mid_mid = f''
    mid_right = f''
    btm = f''
    
    assert len(hand) == len(suit), f'Lengths of hand({hand}) and suit({suit}) do not match.'

    card_len = int(floor(term_width * 0.2))

    if card_len < 7:
        card_len = 7
    elif card_len > 13:
        card_len = 13
    else:
        if card_len % 2 == 0:
            card_len -= 1
    
    len_side = int((card_len-1)/2)

    for i in range(n_cards):
        #c.print(f'{hand[i]}, {type(hand[i])}')
        if hand[i] is str :
                empty += f'{border["v_bar"]}{space * card_len}{border["v_bar"]}  '
                top += f'{border["top_left"]}{border["h_bar"] * card_len}{border["top_right"]}  '
                mid_left += f'{border["v_bar"]}{space}{str(hand[i])}{space * (card_len-2)}{border["v_bar"]}  '
                mid_mid += f'{border["v_bar"]}{space*len_side}{Text(str(suit[i]), style = "blue")}{space*len_side}{border["v_bar"]}  '
                mid_right += f'{border["v_bar"]}{space * (card_len-2)}{str(hand[i])}{space}{border["v_bar"]}  '
                btm += f'{border["bot_left"]}{border["h_bar"] * card_len}{border["bot_right"]}  '
        elif hand[i] == 10:
                empty += f'{border["v_bar"]}{space * card_len}{border["v_bar"]}  '
                top += f'{border["top_left"]}{border["h_bar"] * card_len}{border["top_right"]}  '
                mid_left += f'{border["v_bar"]}{space}{str(hand[i])}{space * (card_len-3)}{border["v_bar"]}  '
                mid_mid += f'{border["v_bar"]}{space*len_side}{Text(str(suit[i]), style = "blue")}{space*len_side}{border["v_bar"]}  '
                mid_right += f'{border["v_bar"]}{space * (card_len-3)}{str(hand[i])}{space}{border["v_bar"]}  '
                btm += f'{border["bot_left"]}{border["h_bar"] * card_len}{border["bot_right"]}  '
        else:
            empty += f'{border["v_bar"]}{space * card_len}{border["v_bar"]}  '
            top += f'{border["top_left"]}{border["h_bar"] * card_len}{border["top_right"]}  '
            mid_left += f'{border["v_bar"]}{space}{str(hand[i])}{space * (card_len-2)}{border["v_bar"]}  '
            mid_mid += f'{border["v_bar"]}{space*len_side}{Text(str(suit[i]), style = "blue")}{space*len_side}{border["v_bar"]}  '
            mid_right += f'{border["v_bar"]}{space * (card_len-2)}{str(hand[i])}{space}{border["v_bar"]}  '
            btm += f'{border["bot_left"]}{border["h_bar"] * card_len}{border["bot_right"]}  '
    if card_len < 9:
        return top+'\n'+mid_left+'\n'+empty+'\n'+mid_mid+'\n'+empty+'\n'+mid_right+'\n'+btm
    elif 9 <= card_len < 12:
        return top+'\n'+mid_left+'\n'+empty+'\n'+empty+'\n'+mid_mid+'\n'+empty+'\n'+empty+'\n'+mid_right+'\n'+btm
    elif card_len >= 12:
        return top+'\n'+mid_left+'\n'+empty+'\n'+empty+'\n'+empty+'\n'+mid_mid+'\n'+empty+'\n'+empty+'\n'+empty+'\n'+mid_right+'\n'+btm

def showhand(d_hand, p_hand):
    """
    Prints the hands of the dealer & the player. The first card of the dealer is anonymised with a '?'.
    Args:
        d_hand (list): List containing dealer's hands
        p_hand (list): List containing player's hands
    """
    global c, suit
    c.print('Dealer\'s hand')
    rand_suit = random.choices(suit, k=len(d_hand))
    new_dealer = d_hand.copy()
    new_dealer[0] = '?'
    show_dealer = print_cards(new_dealer, rand_suit, term_width=c.width)
    c.print(show_dealer)
            
    c.print('\nYour hand')
    new_player = p_hand.copy()
    rand_suit = random.choices(suit, k=len(p_hand))
    show_player = print_cards(p_hand, rand_suit, term_width=c.width)
    c.print(show_player)

def thegame():
    """
    Leothelion's Blackjack Game
    """
    global user_balance, turn, d_balance, game_online, player_hand, dealer_hand, bet

    while user_balance > 1:
        player_hand = deal_init()
        dealer_hand = deal_init()
        player_fold = False
        dealer_fold = False
        betting(bet)
        turn += 1
        showhand(dealer_hand, player_hand)
        time.sleep(2)
        while turn == 1:
            # player action
            selection = input('\n[H]it / [D]ouble / [S]tay\n').lower()
            if selection == 'h':
                hit_card(player_hand)
                wipe()
                c.print('You chose to hit')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(3)
            if selection == 'd':
                double_card(player_hand, user_balance)
                wipe()
                c.print('You chose to double up')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(3)
            if selection == 's':
                wipe()
                c.print('You chose to stay')
                player_fold = True
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(3)
                
            
            # dealer action
            c.print(dealer_hand)
            d_strat = algorithms.dealer_strategy(dealer_hand, player_hand, turn)
            c.print(d_strat)
            if d_strat == 'h':
                hit_card(dealer_hand)
                c.print(dealer_hand)
                wipe()
                c.print('Dealer hits')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(2)
            if d_strat == 'd':
                double_card(dealer_hand, d_balance)
                wipe()
                c.print('Dealer doubles')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(2)
            if d_strat == 's':
                wipe()
                c.print('Dealer stays')
                prize_status()
                showhand(dealer_hand, player_hand)
                dealer_fold = True
                time.sleep(2)
            
            if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                c.print('Win condition met by excess')
                    
                if dealer_win(dealer_hand, player_hand) == True:
                    c.print('House wins')
                    time.sleep(5)
                    d_balance += prize_pool
                    if user_balance >= 1:
                        rematch()
                    else:
                        c.print('GAME OVER')
                        time.sleep(5)
                        break
                
                elif dealer_win(dealer_hand, player_hand) == False:
                    c.print('You win')
                    time.sleep(5)
                    user_balance += prize_pool
                    rematch()
                    
                elif dealer_win(dealer_hand, player_hand) == 'Draw':
                    c.print('Draw')
                    time.sleep(5)
                    user_balance += prize_pool / 2
                    d_balance =- prize_pool / 2
                    rematch()
            elif dealer_fold is True and player_fold is True:
                c.print('Win condition met, both staying')
                time.sleep(1.5)

                if dealer_win(dealer_hand, player_hand) == True:
                    c.print('House wins')
                    d_balance += prize_pool
                    time.sleep(5)
                    if user_balance >= 1:
                        rematch()
                
                elif dealer_win(dealer_hand, player_hand) == False:
                    c.print('You win')
                    time.sleep(5)
                    user_balance += prize_pool
                    rematch()
                    
                elif dealer_win(dealer_hand, player_hand) == 'Draw':
                    c.print('Draw')
                    time.sleep(5)
                    user_balance += prize_pool / 2
                    d_balance += prize_pool / 2
                    rematch()
                
            turn += 1
                
        while turn > 1:
            if player_fold is False:
                selection = input('\n[H]it / [S]tay\n').lower()
                if selection == 'h':
                    hit_card(player_hand)
                    wipe()
                    prize_status()
                    showhand(dealer_hand, player_hand)
                    time.sleep(2)
                    if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                        c.print('Win condition met')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        c.print('House wins')
                        time.sleep(5)
                        if user_balance >= 1:
                            rematch()
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        c.print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        c.print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()

                if selection == 's':
                    wipe()
                    prize_status()
                    showhand(dealer_hand, player_hand)
                    time.sleep(2)
                    if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                        c.print('Win condition met')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        c.print('House wins')
                        time.sleep(5)
                        if user_balance >= 1:
                            rematch()
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        c.print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        c.print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
            
            # dealer action
            if dealer_fold is False:
                d_strat = algorithms.dealer_strategy(dealer_hand, player_hand, turn)
                c.print(d_strat)
                if d_strat == 'h':
                    hit_card(dealer_hand)
                    wipe()
                    c.print('Dealer hits')
                    prize_status()
                    showhand(dealer_hand, player_hand)
                    time.sleep(2)
                    if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                        c.print('Win condition met by excess')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        c.print('House wins')
                        time.sleep(5)
                        d_balance += prize_pool
                        if user_balance >= 1:
                            rematch()
                        else:
                            c.print('GAME OVER')
                            time.sleep(5)
                            break
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        c.print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        c.print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool / 2
                        d_balance =- prize_pool / 2
                        rematch()
                if d_strat == 's':
                    wipe()
                    c.print('Dealer stands')
                    prize_status()
                    showhand(dealer_hand, player_hand)
                    time.sleep(2)
                    if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                        c.print('Win condition met by excess')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        c.print('House wins')
                        time.sleep(5)
                        d_balance += prize_pool
                        if user_balance >= 1:
                            rematch()
                        else:
                            c.print('GAME OVER')
                            time.sleep(5)
                            break
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        c.print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        c.print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool / 2
                        d_balance =- prize_pool / 2
                        rematch()
                

            
            elif dealer_fold is True and player_fold is True:
                c.print('Win condition met, both staying')
                time.sleep(1.5)

                if dealer_win(dealer_hand, player_hand) == True:
                    c.print('House wins')
                    d_balance += prize_pool
                    time.sleep(5)
                    if user_balance >= 1:
                        rematch()
                
                elif dealer_win(dealer_hand, player_hand) == False:
                    c.print('You win')
                    time.sleep(5)
                    user_balance += prize_pool
                    rematch()
                    
                elif dealer_win(dealer_hand, player_hand) == 'Draw':
                    c.print('Draw')
                    time.sleep(5)
                    user_balance += prize_pool / 2
                    d_balance += prize_pool / 2
                    rematch()
            
            turn += 1

if __name__ == '__main__':
    cur = get_local_currency()
    game_online = True
    selection = None
    c.print(logo(), style = theme)
    thegame()