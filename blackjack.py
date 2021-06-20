import os
import time
import algorithms
from tzlocal import get_localzone

import random
#random.seed(69420)

# >>> init >>>
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
#dealer_hand = []
#player_hand = []
user_balance = 1000
d_balance = 10000000
prize_pool = 0
turn = 0
bet = 0
# <<< init <<<

def get_local_currency():
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
    global deck, dealer_hand, player_hand, prize_pool, turn, bet
    dealer_hand = []
    player_hand = []
    prize_pool = 0
    turn = 0
    bet = 0
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    thegame()

def wipe():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('CLS') # or whatever
        
def logo():
    wipe()
    print(' L')
    time.sleep(0.1)
    wipe()
    print(' L E')
    time.sleep(0.1)
    wipe()
    print(' L E O')
    time.sleep(0.1)
    wipe()
    print(' L E O \'')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B                ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L              ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L A            ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L A C          ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L A C K        ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L A C K J      ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L A C K J A    ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L A C K J A C  ')
    time.sleep(0.1)
    wipe()
    print(' L E O \' S   B L A C K J A C K')
    time.sleep(0.4)
    wipe()
    time.sleep(0.4)
    print(' L E O \' S   B L A C K J A C K')
    time.sleep(0.4)
    wipe()
    time.sleep(0.4)
    print(' L E O \' S   B L A C K J A C K')
    time.sleep(0.8)
    wipe()
    time.sleep(0.4)

def prize_status():
    global user_balance, prize_pool, cur
    print(f'Prize pool: {cur}{prize_pool}\nBalance: {cur}{user_balance}')

def betting(bet):
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
            print('Invalid amount.')
            time.sleep(2)
            betting(bet)
    except:
        print('Invalid character inserted.')
        time.sleep(2)
        betting(bet)

def deal_init():
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
    global deck, prize_pool, bet, d_balance
    user_balance -= bet
    d_balance -= bet
    prize_pool *= prize_pool
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

def showhand(d_hand, p_hand):
    print('Dealer\'s hand')
    new_dealer = d_hand.copy()
    new_dealer[0] = '?'
    for card in new_dealer:
        print(f'{card}')
            
    print('\nYour hand')
    new_player = p_hand.copy()
    for card in new_player:
        print(f'{card}')

def thegame():
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
                print('You chose to hit')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(3)
            if selection == 'd':
                double_card(player_hand, user_balance)
                wipe()
                print('You chose to double up')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(3)
            if selection == 's':
                wipe()
                print('You chose to stay')
                player_fold = True
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(3)
                
            
            # dealer action
            print(dealer_hand)
            d_strat = algorithms.dealer_strategy(dealer_hand, player_hand, turn)
            print(d_strat)
            if d_strat == 'h':
                hit_card(dealer_hand)
                print(dealer_hand)
                wipe()
                print('Dealer hits')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(2)
            if d_strat == 'd':
                double_card(dealer_hand, d_balance)
                wipe()
                print('Dealer doubles')
                prize_status()
                showhand(dealer_hand, player_hand)
                time.sleep(2)
            if d_strat == 's':
                wipe()
                print('Dealer stays')
                prize_status()
                showhand(dealer_hand, player_hand)
                dealer_fold = True
                time.sleep(2)
            
            if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                print('Win condition met by excess')
                    
                if dealer_win(dealer_hand, player_hand) == True:
                    print('House wins')
                    time.sleep(5)
                    d_balance += prize_pool
                    if user_balance >= 1:
                        rematch()
                    else:
                        print('GAME OVER')
                        time.sleep(5)
                        break
                
                elif dealer_win(dealer_hand, player_hand) == False:
                    print('You win')
                    time.sleep(5)
                    user_balance += prize_pool
                    rematch()
                    
                elif dealer_win(dealer_hand, player_hand) == 'Draw':
                    print('Draw')
                    time.sleep(5)
                    user_balance += prize_pool / 2
                    d_balance =- prize_pool / 2
                    rematch()
            elif dealer_fold is True and player_fold is True:
                print('Win condition met, both staying')
                time.sleep(1.5)

                if dealer_win(dealer_hand, player_hand) == True:
                    print('House wins')
                    d_balance += prize_pool
                    time.sleep(5)
                    if user_balance >= 1:
                        rematch()
                
                elif dealer_win(dealer_hand, player_hand) == False:
                    print('You win')
                    time.sleep(5)
                    user_balance += prize_pool
                    rematch()
                    
                elif dealer_win(dealer_hand, player_hand) == 'Draw':
                    print('Draw')
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
                        print('Win condition met')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        print('House wins')
                        time.sleep(5)
                        if user_balance >= 1:
                            rematch()
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()

                if selection == 's':
                    wipe()
                    prize_status()
                    showhand(dealer_hand, player_hand)
                    time.sleep(2)
                    if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                        print('Win condition met')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        print('House wins')
                        time.sleep(5)
                        if user_balance >= 1:
                            rematch()
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
            
            # dealer action
            if dealer_fold is False:
                d_strat = algorithms.dealer_strategy(dealer_hand, player_hand, turn)
                print(d_strat)
                if d_strat == 'h':
                    hit_card(dealer_hand)
                    wipe()
                    print('Dealer hits')
                    prize_status()
                    showhand(dealer_hand, player_hand)
                    time.sleep(2)
                    if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                        print('Win condition met by excess')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        print('House wins')
                        time.sleep(5)
                        d_balance += prize_pool
                        if user_balance >= 1:
                            rematch()
                        else:
                            print('GAME OVER')
                            time.sleep(5)
                            break
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool / 2
                        d_balance =- prize_pool / 2
                        rematch()
                if d_strat == 's':
                    wipe()
                    print('Dealer stands')
                    prize_status()
                    showhand(dealer_hand, player_hand)
                    time.sleep(2)
                    if total(dealer_hand) >= 21 or total(player_hand) >= 21:
                        print('Win condition met by excess')
                    
                    if dealer_win(dealer_hand, player_hand) == True:
                        print('House wins')
                        time.sleep(5)
                        d_balance += prize_pool
                        if user_balance >= 1:
                            rematch()
                        else:
                            print('GAME OVER')
                            time.sleep(5)
                            break
                    
                    elif dealer_win(dealer_hand, player_hand) == False:
                        print('You win')
                        time.sleep(5)
                        user_balance += prize_pool
                        rematch()
                        
                    elif dealer_win(dealer_hand, player_hand) == 'Draw':
                        print('Draw')
                        time.sleep(5)
                        user_balance += prize_pool / 2
                        d_balance =- prize_pool / 2
                        rematch()
                

            
            elif dealer_fold is True and player_fold is True:
                print('Win condition met, both staying')
                time.sleep(1.5)

                if dealer_win(dealer_hand, player_hand) == True:
                    print('House wins')
                    d_balance += prize_pool
                    time.sleep(5)
                    if user_balance >= 1:
                        rematch()
                
                elif dealer_win(dealer_hand, player_hand) == False:
                    print('You win')
                    time.sleep(5)
                    user_balance += prize_pool
                    rematch()
                    
                elif dealer_win(dealer_hand, player_hand) == 'Draw':
                    print('Draw')
                    time.sleep(5)
                    user_balance += prize_pool / 2
                    d_balance += prize_pool / 2
                    rematch()
            
            turn += 1

if __name__ == '__main__':
    cur = get_local_currency()
    game_online = True
    selection = None
    logo()
    thegame()