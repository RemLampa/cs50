from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def optimal_cell_distance(deletion_steps, insertion_steps, substitution_steps, last_char_a, last_char_b):
    """Infer the cost of adding the current letter from previous steps"""

    total_deletion_distance = (deletion_steps + 1, Operation.DELETED)

    total_insertion_distance = (insertion_steps + 1, Operation.INSERTED)

    total_substitution_steps = substitution_steps if last_char_a == last_char_b else substitution_steps + 1
    total_substitution_distance = (total_substitution_steps, Operation.SUBSTITUTED)

    return min(
        total_deletion_distance,
        total_insertion_distance,
        total_substitution_distance,
        key=lambda distance: distance[0])


def distances(a, b):
    """Calculate edit distance from a to b"""

    distance_matrix = [[(0, None)] * (len(b) + 1) for i in range(len(a) + 1)]

    # Solve for first column
    for i in range(1, len(a) + 1):
        distance_matrix[i][0] = (i, Operation.DELETED)

    # Solve for first row
    for j in range(1, len(b) + 1):
        distance_matrix[0][j] = (j, Operation.INSERTED)

    # Solve for the rest of the cells
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            previous_deletion_steps = distance_matrix[i-1][j][0]
            previous_insertion_steps = distance_matrix[i][j-1][0]

            previous_substitution_steps = distance_matrix[i-1][j-1][0]

            last_char_a = a[i-1]
            last_char_b = b[j-1]

            distance_matrix[i][j] = optimal_cell_distance(
                previous_deletion_steps,
                previous_insertion_steps,
                previous_substitution_steps,
                last_char_a,
                last_char_b
            )

    return distance_matrix
