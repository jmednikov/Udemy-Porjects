
# needed for a few parts of the game
import random

#all card suits, ranks, and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

values ={"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10,
        "Jack":10, "Queen":10, "King":10, "Ace":11}

# to show that the player wants to keep playing
playing=True


# CLASS DEFINITIONS
class Card:
    # the class the makes the cards
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    # the class for making the deck
    def __init__(self):
        # start with an empty list
        self.deck = [] 
        for suit in suits:
            for rank in ranks:
            # makes the deak class
                self.deck.append(Card(suit,rank))

    # allows someone to check that is in the deck
    def __stg__(self):
        # start with an empty string
        deck_comp = ''  
        # add each Card object's print string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() 
        return 'The deck has:' + deck_comp

   #suffles the deck using the suffle function from the random library
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        #uses the pop method to take cards out of the deck
        single_card = self.deck.pop()
        return single_card


class Hand:
    
    def __init__(self):
        # start with an empty list like in the Deck class
        self.cards = []  
        # start with zero value
        self.value = 0   
        # added an attribute to keep track of aces as in blackjack they are 1 and 11
        self.aces = 0    
    
    # this adds the cards for your hand
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces
    
    # allows player to not get a bust just due to an ace and something else
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            

# the chips for betting as well as how meny chips the player has
class Chips:
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


# FUNCTION DEFINITIONS:

#This func allows you to make bets while also minimizeing errors
def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

# the "hit" in blackjack
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
# the players option
def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

    
def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)
    
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")
    
# GAMEPLAY!
# Set up the Player's chips
player_chips = Chips()  # remember the default value is 100
while True:
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    
    
    # Prompt the Player for their bet:
    take_bet(player_chips)
    
    # Show the cards:
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from  hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)
        
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
    
    # If Player hasn't busted, play Dealer's hand        
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
            
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Test different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)

    # Inform Player of their chips total    
    print("\nPlayer's winnings stand at",player_chips.total)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break
        

        
        