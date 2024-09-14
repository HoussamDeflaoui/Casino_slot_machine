import random

MIN_DEPO = 10
MAX_DEPO = 1000
MAX_LINES = 3

ROWS = 3
COLS = 3
symbols_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbols_value = {
    "A": 6,
    "B": 4,
    "C": 3,
    "D": 2
}

def get_slot_machine_spin(ROWS, COLS, symbols_count):
    all_symbols = []
    for symbol, symbol_amount in symbols_count.items():
        for _ in range(symbol_amount):
            all_symbols.append(symbol)

    columns = []
    for _ in range(COLS):
        column = []
        current_column = all_symbols[:]
        for _ in range(ROWS):
            value = random.choice(current_column)
            current_column.remove(value)
            column.append(value)
        columns.append(column)

    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row])

def check_if_won(columns, lines, bet, values):
    winnings = 0
    winnings_lines = []

    for line in range(lines):
        symbol = columns[0][line]  # Get the symbol from the first column for this line
        for column in columns:
            if column[line] != symbol:  # Check if the symbol in this line matches across all columns
                break
        else:
            # All symbols in this line match
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)  # Line numbers are 1-based for user-friendly output

    return winnings, winnings_lines

def get_deposit():
    while True:
        deposit = input("Enter the amount you would like to deposit: £")
        if deposit.isdigit():
            deposit = int(deposit)
            if deposit < MIN_DEPO:
                print(f"Minimum Deposit is £{MIN_DEPO}")
            elif deposit > MAX_DEPO:
                print(f"Maximum Deposit is £{MAX_DEPO}")
            else:
                return deposit
        else:
            print("Deposit must be a number")

def get_lines():
    while True:
        lines = input("Enter the amount of lines you would like to bet on: ")
        if lines.isdigit():
            lines = int(lines)
            if lines < 1:
                print("Minimum amount of lines you can bet on is 1")
            elif lines > MAX_LINES:
                print(f"Maximum amount of lines you can bet on is {MAX_LINES}")
            else:
                return lines
        else:
            print("The number of lines must be in numbers")

def get_bet(deposit, lines):
    while True:
        bet = input("Enter the amount you would like to bet on each line: £")
        bet = bet.lower()  # Convert input to lowercase
        if bet == "depo":
            return "update_deposit"  # Signal to update deposit
        if bet.isdigit():
            bet = int(bet)
            if (bet * lines) <= deposit:
                return bet
            else:
                print("Insufficient balance in your account, please deposit more to bet this amount")
        else:
            print("The bet must be in numbers")

def main():
    deposit = get_deposit()

    while deposit > 0:
        print(f"\nCurrent balance: £{deposit}")

        lines = get_lines()

        while True:
            result = get_bet(deposit, lines)
            if result == "update_deposit":
                deposit = get_deposit()  # Update the deposit
            else:
                bet = result
                total = bet * lines
                if lines == 1:
                    word = "line"
                else:
                    word = "lines"
                print(f"You've bet £{bet} on {lines} {word}. Total Bet - £{total}")
                break  # Exit the loop once a valid bet is made

        slots = get_slot_machine_spin(ROWS, COLS, symbols_count)
        print_slot_machine(slots)
        winnings, winnings_lines = check_if_won(slots, lines, bet, symbols_value)

        deposit -= total  # Deduct the bet amount from deposit
        deposit += winnings  # Add winnings to deposit

        print(f"You've won £{winnings}")
        if winnings_lines:
            print("You've won on lines", *winnings_lines)
        else:
            print("No wins this time.")

        if deposit > 0:
            continue_playing = input("Press 'k' to quit or any other key to spin again: ")
            if continue_playing.lower() == 'k':
                break
        else:
            print("Your balance is zero. Game over.")

    print("Thank you for playing! Your final balance is £", deposit)

if __name__ == "__main__":
    main()
