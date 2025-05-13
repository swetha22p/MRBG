import matplotlib.pyplot as plt

# Rule-based evaluation scores
scores = [
    3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2,
    3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3,
    3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 2, 2, 3, 1, 2,
    1, 3, 1
]
print(len(scores))
# Create a line plot
plt.figure(figsize=(15, 6))
plt.plot(scores, marker='o', linestyle='-', color='b', label='Rule-Based Evaluation')

# Add labels and title
plt.title('Rule-Based Evaluation Scores')
plt.xlabel('Index')
plt.ylabel('Score')
plt.yticks([1, 2, 3], ['Incorrect (1)', 'Moderate (2)', 'Correct (3)'])
plt.grid(True)

# Highlight specific scores
for i, score in enumerate(scores):
    if score == 1:
        plt.scatter(i, score, color='red', label='Incorrect' if i == 0 else None)
    elif score == 2:
        plt.scatter(i, score, color='orange', label='Moderate' if i == 0 else None)

# Add legend
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()