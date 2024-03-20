"""
Function to decide which mallet to use for each key in the song.
Input: 
- List of notes
- Map of pairs of keys to distance
Output:
- List of pairs of keys where the first key is for left mallet and the second key is for right mallet
"""
def mallet_decision(notes, distance_map):
     # If there are no notes, return an empty list
    if not notes:
        return []

    # Initialize mallet positions to the first note (or the first two different notes if available)
    left_mallet = right_mallet = notes[0]
    if len(notes) > 1 and notes[0] != notes[1]:
        right_mallet = notes[1]

    decisions = []

    for note in notes:
        # If the note is the same as one of the mallets, prefer that mallet
        if note == left_mallet or note == right_mallet:
            decisions.append((left_mallet, right_mallet))
            continue

        # Calculate distances from the current note to the left and right mallet positions
        left_distance = distance_map.get((left_mallet, note), float('inf'))
        right_distance = distance_map.get((right_mallet, note), float('inf'))

        # Decide which mallet to use based on the distance and future considerations
        if left_distance <= right_distance:
            left_mallet = note
        else:
            right_mallet = note

        decisions.append((left_mallet, right_mallet))

    return decisions

#    # Initialize memoization table, potentially with -1 or None to indicate uncomputed states
#     memo = {}
#     n = len(notes)
    
#     def dp(i, pos_left, pos_right):
#         # Base case: If all notes have been considered, return 0 (no movement needed)
#         if i == n:
#             return 0
#         # Check if the current state has been computed before
#         if (i, pos_left, pos_right) in memo:
#             return memo[(i, pos_left, pos_right)]
        
#         # Calculate the cost of playing the next note with the left mallet
#         cost_left = distance_map[(pos_left, notes[i])] + dp(i + 1, notes[i], pos_right)
#         # Calculate the cost of playing the next note with the right mallet
#         cost_right = distance_map[(pos_right, notes[i])] + dp(i + 1, pos_left, notes[i])
        
#         # Choose the option with the minimum cost
#         memo[(i, pos_left, pos_right)] = min(cost_left, cost_right)
        
#         return memo[(i, pos_left, pos_right)]
    
#     # Initialize starting positions of mallets, for example, assuming they start at the first note
#     start_pos_left = notes[0]  # or some other logic to determine the starting position
#     start_pos_right = notes[0]  # Adjust as necessary
#     dp(0, start_pos_left, start_pos_right)
    
#     # Reconstruct the decision path from the memoization table
#     # This part requires additional logic to backtrack through your memoization
#     # table and determine the sequence of decisions (left or right mallet) that led to the minimum cost.

    
#     return []  # Return the reconstructed decision path