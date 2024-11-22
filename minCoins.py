import sys
import ast


def min_coins(coins, amount):
    """
    Function to calculate the minimum number of coins needed to make the given amount.

    :param coins: List of coin denominations.
    :param amount: Target amount to make change for.
    :return: Minimum number of coins and the combination used.
    """
    # Initialize DP array where dp[i] is the minimum coins needed for amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed for amount 0

    # Keep track of combinations used for each amount
    combination = [None] * (amount + 1)

    # Populate the DP array
    for coin in coins:
        for i in range(coin, amount + 1):
            if dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                combination[i] = coin

    # Backtrack to find the coins used
    result = []
    current = amount
    while current > 0 and combination[current] is not None:
        # Insert coins in reverse order for descending output
        result.insert(0, combination[current])
        current -= combination[current]

    return (dp[amount], result) if dp[amount] != float('inf') else (None, [])


def main():
    if len(sys.argv) > 1:
        try:
            # Parse command line arguments
            coins = ast.literal_eval(sys.argv[1])
            amount = int(sys.argv[2])

            # Validate inputs
            if not isinstance(coins, list) or not all(isinstance(c, int) and c > 0 for c in coins):
                raise ValueError("Coins must be a list of positive integers.")
            if amount < 0:
                raise ValueError("Amount must be a non-negative integer.")

            # Sort coins in descending order for clarity in output
            coins.sort(reverse=True)

            # Calculate the minimum coins
            min_count, coin_combination = min_coins(coins, amount)

            if min_count is not None:
                # Format the coin combination into the required output format
                combination_str = "+".join(map(str, coin_combination))
                print(f"{min_count} Coins: {combination_str}")
            else:
                print("No solution")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
