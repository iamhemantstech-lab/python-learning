"""
Topic 2.1: First-Class Functions, Lexical Scope & The Mechanics of Closures
===========================================================================
Deep Python Concept:
In Python, functions are first-class citizens:
1. They can be assigned to variables.
2. Passed as arguments to other functions.
3. Returned from functions.

What is a CLOSURE?
A closure occurs when a nested function retains access to variables from its
enclosing scope (outer function), EVEN AFTER the outer function has finished executing!

CPython stores these captured variables inside `__closure__` tuples containing `cell` objects.
"""

# -----------------------------------------------------------------------------
# 1. THE CLOSURE PATTERN: Configurable API Rate Limiter
# -----------------------------------------------------------------------------
def create_rate_limiter(max_calls: int, window_name: str):
    """
    Outer function creates a closed state environment.
    `max_calls` and `call_count` are captured by `limiter`.
    """
    call_count = 0  # Free variable to be captured by the inner function

    def limiter(user_id: str) -> bool:
        # `nonlocal` tells Python to modify `call_count` in the enclosing scope,
        # rather than creating a new local variable!
        nonlocal call_count
        if call_count >= max_calls:
            print(f" [429 BLOCKED] User '{user_id}' exceeded limit of {max_calls} in '{window_name}'")
            return False

        call_count += 1
        print(f" [200 ALLOWED] User '{user_id}' executed action. ({call_count}/{max_calls} used)")
        return True

    return limiter  # Returning the function object without calling it!


# -----------------------------------------------------------------------------
# 2. UNDER-THE-HOOD CPYTHON INSPECTION
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: HOW PYTHON HANDLES CLOSURES UNDER THE HOOD")
    print("=" * 70)

    # Instantiate two separate limiter closures with their own isolated state
    standard_user_limiter = create_rate_limiter(max_calls=3, window_name="1-Minute Window")
    vip_user_limiter = create_rate_limiter(max_calls=5, window_name="1-Minute Window")

    print("\n[Step 1: Calling standard_user_limiter]")
    standard_user_limiter("dev_user")
    standard_user_limiter("dev_user")
    standard_user_limiter("dev_user")
    standard_user_limiter("dev_user")  # Exceeds limit

    print("\n[Step 2: Proving Isolated State (VIP Limiter has its own count)]")
    vip_user_limiter("admin_dev")  # Starts at 1/5!

    # 3. Dissecting Python's Internal Closure Structure
    print("\n" + "=" * 70)
    print("CPYTHON INTERNAL INSPECTION:")
    print("=" * 70)
    print(f"Captured free variables: {standard_user_limiter.__code__.co_freevars}")
    print(f"Internal __closure__ tuple: {standard_user_limiter.__closure__}")

    for var_name, cell in zip(standard_user_limiter.__code__.co_freevars, standard_user_limiter.__closure__):
        print(f" -> Variable '{var_name}' currently holds value: {cell.cell_contents}")

    print("=" * 70)
