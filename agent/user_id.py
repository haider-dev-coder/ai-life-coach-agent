user_id = "haider123"
habit_memory = load_habits(user_id)
...
save_habit(user_id, {"latest": parsed.dict()})
