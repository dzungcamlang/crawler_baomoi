result = [
    {'_id': '', 'score': 0},
    {'_id': '', 'score': 0},
    {'_id': '', 'score': 0},
    {'_id': '', 'score': 0},
    {'_id': '', 'score': 0}
]
scores = [4, 7, 3, 9, 7, 9, 5, 3]
for idx_scores, val_scores in enumerate(scores):
    for idx_result, val_result in enumerate(result):
        if val_scores == val_result['score']:
            break
        if val_scores > val_result['score']:
            item_to_insert = {'_id': idx_scores, 'score': val_scores}
            result.insert(idx_result, item_to_insert)
            result.pop()
            break

print(result)
