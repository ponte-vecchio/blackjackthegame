from blackjack import total

def dealer_strategy(hand, playerhand, turn, difficulty='normal'):
    if difficulty == 'easy':
        if total(hand) < 7:
            return 'd'
        elif 7 <= total(hand) <= 11:
            return 'd'
        elif 12 <= total(hand) <= 15:
            return 'h'
        elif total(hand) < 15:
            return 's'
        
    if difficulty == 'normal':
        # soft
        if 'A' in hand:
            newhand = [11 if x == 'A' else x for x in hand]
            if turn == 1:
                if 'J' in hand or 'Q' in hand or 'K' in hand:
                    return 's'
                elif sum(newhand) == 20:
                    return 's'
                elif sum(newhand) == 19:
                    if 6 not in playerhand:
                        return 's'
                    else:
                        return 'd'
                elif sum(newhand) == 18:
                    elsestop_18 = [2, 3, 4, 5, 6]
                    hit_18 = [9, 10, 11]
                    d_switch = None
                    for i in elsestop_18:
                        if i in playerhand:
                            d_switch = 'd'
                    
                    for i in hit_18:
                        if i in playerhand:
                            d_switch = 'h'
                            
                    if d_switch is not None:
                        return d_switch
                    else:
                        return 's'
                elif sum(newhand) == 17:
                    elsehit_17 = []
                elif sum(newhand) >= 15:
                    newhand = [1 if x==11 else x for x in newhand]
                    if sum(newhand) < 11:
                        return 'd'
                    elif sum(newhand) >= 11:
                        return 'h'
                else:
                    return 'h'
                        
            elif turn > 1:
                if 'J' in hand or 'Q' in hand or 'K' in hand:
                    newhand = [10 if x == 'J' or x == 'Q' or x == 'K' else x for x in newhand]
                    if sum(newhand) > 19:
                        return 's'
                    elif sum(newhand) <= 18:
                        newhand = [1 if x==11 else x for x in newhand]
                        if sum(newhand) <= 14:
                            return 'h'
                        else:
                            return 's'
                    else:
                        return 's'
                elif sum(newhand) > 19:
                    return 's'
                elif sum(newhand) <= 18:
                    newhand = [1 if x==11 else x for x in newhand]
                    if sum(newhand) <= 14:
                        return 'h'
                else:
                    return 's'
        
        # hard
        else:
            if 'J' in hand or 'Q' in hand or 'K' in hand:
                newhand = [10 if x == 'J' or x == 'Q' or x == 'K' else x for x in hand]
                print(newhand)
                if sum(newhand) >= 17:
                    return 's'
                elif 13 <= sum(newhand) <= 16:
                    hard_hit = [7, 8, 9, 10]
                    d_switch = None
                    for i in hard_hit:
                        if i in playerhand:
                            d_switch = 'h'

                    if d_switch is not None:
                        return d_switch
                    else:
                        return 's'
                elif sum(newhand) == 12:
                    stand = [4,5,6]
                    d_switch = None
                    
                    for i in stand:
                        if i in playerhand:
                            d_switch = 's'
                    
                    if d_switch is not None:
                        return d_switch
                    else:
                        return 'h'
                elif sum(newhand) == 11:
                    return 'h'
                elif sum(newhand) == 10:
                    double = [2,3,4,5,6,7,8,9]
                    d_switch = None
                    
                    for i in double:
                        if i in playerhand:
                            d_switch = 'd'
                    
                    if d_switch is not None:
                        return d_switch
                    else:
                        return 'h'
                elif sum(newhand) == 9:
                    double = [3, 4, 5, 6]
                    d_switch = None
                    
                    for i in double:
                        if i in playerhand:
                            d_switch = 'd'
                    
                    if d_switch is not None:
                        return d_switch
                    else:
                        return 'h'
                elif sum(newhand) <= 8:
                    return 'h'
            elif sum(hand) >= 17:
                return 's'
            elif 13 <= sum(hand) <= 16:
                hard_hit = [7, 8, 9, 10]
                d_switch = None
                for i in hard_hit:
                    if i in playerhand:
                        d_switch = 'h'

                if d_switch is not None:
                    return d_switch
                else:
                    return 's'
            elif sum(hand) == 12:
                stand = [4,5,6]
                d_switch = None
                
                for i in stand:
                    if i in playerhand:
                        d_switch = 's'
                
                if d_switch is not None:
                    return d_switch
                else:
                    return 'h'
            elif sum(hand) == 11:
                return 'h'
            elif sum(hand) == 10:
                double = [2,3,4,5,6,7,8,9]
                d_switch = None
                
                for i in double:
                    if i in playerhand:
                        d_switch = 'd'
                
                if d_switch is not None:
                    return d_switch
                else:
                    return 'h'
            elif sum(hand) == 9:
                double = [3, 4, 5, 6]
                d_switch = None
                
                for i in double:
                    if i in playerhand:
                        d_switch = 'd'
                
                if d_switch is not None:
                    return d_switch
                else:
                    return 'h'
            elif sum(hand) <= 8:
                return 'h'
            
    if difficulty == 'cheater': #TODO
        pass
