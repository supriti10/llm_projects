def get_prompt(mode, user_input):
    if mode == "Creative":
        return f"Be highly creative:\n{user_input}"
    elif mode == "Logic":
        return f"Solve step-by-step:\n{user_input}"
    elif mode == "Debate":
        return f"Give a strong argument:\n{user_input}"
    return user_input