"""
Topic 2.2: Parameterized Decorators & The Role of @functools.wraps
==================================================================
Key Python Mechanism:
A standard decorator accepts 1 argument: the target function.
`@decorator` is equivalent to: `func = decorator(func)`

A PARAMETERIZED decorator requires THREE layers of nested functions:
Layer 1: Accepts the decorator arguments (@retry(max_attempts=3))
Layer 2: Accepts the target function (decorator(func))
Layer 3: The wrapper that intercepts the call (wrapper(*args, **kwargs))

Why @functools.wraps is MANDATORY:
Without `@wraps`, the decorated function loses its identity!
Its `__name__` becomes 'wrapper', its `__doc__` is erased,
and FastAPI route schemas / introspection tools will fail!
"""

import functools
import time
from typing import Callable, Any


# -----------------------------------------------------------------------------
# 1. THE ENTERPRISE RETRY DECORATOR (3 Layers)
# -----------------------------------------------------------------------------
def retry(
    max_attempts: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Layer 1: Decorator Factory that accepts configuration parameters.
    """
    def decorator(func: Callable) -> Callable:
        """
        Layer 2: Receives the target function to be decorated.
        """
        # @functools.wraps copies __name__, __doc__, __annotations__ to wrapper!
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Layer 3: The actual interceptor that executes when func() is called.
            """
            delay = initial_delay
            attempt = 1

            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    print(f" [Attempt {attempt}/{max_attempts} Failed] Error: {err}")
                    if attempt == max_attempts:
                        print(f" [Retries Exhausted] Raising exception...")
                        raise

                    print(f" -> Backing off for {delay:.2f}s before retry...")
                    time.sleep(delay)
                    delay *= backoff_factor
                    attempt += 1

        return wrapper
    return decorator


# -----------------------------------------------------------------------------
# 2. TESTING WITH AN UNSTABLE EXTERNAL API
# -----------------------------------------------------------------------------
# Simulated counter of network failures
mock_network_failures = 2


@retry(max_attempts=4, initial_delay=0.2, backoff_factor=2.0, exceptions=(ConnectionError,))
def call_payment_gateway(amount: float, currency: str = "USD") -> dict:
    """Sends a charge request to Stripe payment gateway."""
    global mock_network_failures

    print(f" [Calling Stripe API] Charging {amount} {currency}...")
    if mock_network_failures > 0:
        mock_network_failures -= 1
        raise ConnectionError("504 Gateway Timeout from Stripe")

    return {"status": "SUCCESS", "transaction_id": "txn_9948274"}


# -----------------------------------------------------------------------------
# 3. DEMONSTRATION & @wraps VERIFICATION
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: PARAMETERIZED RETRY DECORATOR & @functools.wraps")
    print("=" * 70)

    # 1. Verify Metadata Preservation via @functools.wraps
    print("\n[Step 1: Inspecting Function Identity & Docstring]")
    print(f"Function Name: '{call_payment_gateway.__name__}'")
    print(f"Docstring:     '{call_payment_gateway.__doc__}'")
    # If we had not used @functools.wraps, __name__ would be literally 'wrapper'!

    # 2. Executing Function with Automated Retry & Exponential Backoff
    print("\n[Step 2: Executing Network Call with Exponential Backoff]")
    result = call_payment_gateway(amount=199.99, currency="USD")
    print(f"\nFinal Result: {result}")

    print("\n" + "=" * 70)
    print("SUCCESS: Decorator automatically handled retries and exponential backoff!")
    print("=" * 70)
