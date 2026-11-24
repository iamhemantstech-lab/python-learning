"""
Topic 1.1: Abstract Base Classes (ABC) & Composition over Inheritance
====================================================================
Real-World Backend Scenario:
A notification engine that sends alerts via Email, SMS, or Slack.
Instead of hardcoding notification logic inside our UserService,
we define a strict contract (Interface) using Python's `abc` module
and inject it using COMPOSITION ("has-a" relationship).
"""

from abc import ABC, abstractmethod
from typing import Protocol


# -----------------------------------------------------------------------------
# 1. THE CONTRACT: Abstract Base Class (ABC)
# -----------------------------------------------------------------------------
class BaseNotifier(ABC):
    """
    An Abstract Base Class cannot be instantiated directly.
    It forces any child class to implement all `@abstractmethod`s.
    """

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """All notifiers must implement this method."""
        pass

    @property
    @abstractmethod
    def channel_name(self) -> str:
        """All notifiers must expose which channel they operate on."""
        pass


# -----------------------------------------------------------------------------
# 2. CONCRETE IMPLEMENTATIONS (Polymorphism)
# -----------------------------------------------------------------------------
class EmailNotifier(BaseNotifier):
    def __init__(self, smtp_server: str = "smtp.company.com"):
        self.smtp_server = smtp_server

    @property
    def channel_name(self) -> str:
        return "EMAIL"

    def send(self, recipient: str, message: str) -> bool:
        print(f"[{self.channel_name}] Connecting to {self.smtp_server}...")
        print(f"[{self.channel_name}] Sending email to '{recipient}': {message}")
        return True


class SMSNotifier(BaseNotifier):
    def __init__(self, gateway_api_key: str = "secret-sms-key"):
        self.gateway_api_key = gateway_api_key

    @property
    def channel_name(self) -> str:
        return "SMS"

    def send(self, recipient: str, message: str) -> bool:
        print(f"[{self.channel_name}] Authenticating with SMS Gateway (Key: {self.gateway_api_key[:4]}****)...")
        print(f"[{self.channel_name}] Dispatching SMS to '{recipient}': {message}")
        return True


class SlackNotifier(BaseNotifier):
    def __init__(self, webhook_url: str = "https://hooks.slack.com/services/..."):
        self.webhook_url = webhook_url

    @property
    def channel_name(self) -> str:
        return "SLACK"

    def send(self, recipient: str, message: str) -> bool:
        print(f"[{self.channel_name}] Posting payload to webhook: {self.webhook_url[:28]}...")
        print(f"[{self.channel_name}] Sending Slack message to '{recipient}': {message}")
        return True


# -----------------------------------------------------------------------------
# 3. COMPOSITION OVER INHERITANCE: The UserService
# -----------------------------------------------------------------------------
# Anti-Pattern (Inheritance): `class UserService(EmailNotifier)`
# Why it's bad: A UserService IS NOT an EmailNotifier! What if we want to switch
# to SMS tomorrow? Inheritance tightly couples the two together.
#
# Best Practice (Composition): `UserService` HAS A `notifier`.
class UserService:
    def __init__(self, notifier: BaseNotifier):
        # We inject ANY notifier that respects the BaseNotifier contract!
        self.notifier = notifier

    def register_user(self, email: str, name: str):
        print(f"\n[UserService] Registering user '{name}' in database...")
        # Business logic here...

        # Trigger notification through the injected component
        welcome_msg = f"Welcome to our platform, {name}!"
        self.notifier.send(recipient=email, message=welcome_msg)


# -----------------------------------------------------------------------------
# 4. DEMONSTRATION & VERIFICATION
# __name__ -> indicate the current file name
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: ABSTRACT BASE CLASSES & COMPOSITION OVER INHERITANCE")
    print("=" * 70)

    # 1. Proving ABC Contract Enforcement:
    # What happens if someone tries to create an incomplete notifier?
    # class IncompleteNotifier(BaseNotifier):
    #     pass

    # try:
    #     incomplete = IncompleteNotifier()
    # except TypeError as e :
    #     print("\n[ABC Enforcement Check Passed!]")
    #     print(f"Python prevented instantiation: {e}")

    # 2. Seamlessly Swapping Implementations via Composition:
    email_service = UserService(notifier=EmailNotifier())
    email_service.register_user(email="dev@mail.com", name="Dev P")

    # We can switch to SMS without altering a SINGLE LINE of UserService!
    sms_service = UserService(notifier=SMSNotifier())
    sms_service.register_user(email="+919999999999", name="Dev P")

    # Or switch to Slack:
    slack_service = UserService(notifier=SlackNotifier())
    slack_service.register_user(email="#alerts-dev", name="Dev P")

    print("\n" + "=" * 70)
    print("SUCCESS: UserService is decoupled from specific notification vendors!")
    print("=" * 70)
