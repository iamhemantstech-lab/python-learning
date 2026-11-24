r"""
Topic 1.2: Multiple Inheritance, the "Diamond Problem" & MRO (Method Resolution Order)
=====================================================================================
Crucial Interview Concept:
Many developers believe `super()` simply calls the "parent class".
IN PYTHON, THAT IS FALSE!
`super()` calls the NEXT class in the Method Resolution Order (MRO) list,
calculated using Python's C3 Linearization algorithm.

Scenario: The Classic Diamond Problem in Backend Architecture
           [BaseService]
             /        \
    [AuditMixin]    [MetricsMixin]
             \        /
         [PaymentService]
"""

class BaseService:
    def execute(self, action: str):
        print(f" -> [BaseService] Executing core operation: '{action}'")


class AuditMixin(BaseService):
    def execute(self, action: str):
        print(f" -> [AuditMixin] Logging action '{action}' to audit database")
        # Notice: super() does NOT necessarily call BaseService here!
        # It calls whatever is NEXT in the MRO!
        super().execute(action)
        print(f" -> [AuditMixin] Audit log complete.")


class MetricsMixin(BaseService):
    def execute(self, action: str):
        print(f" -> [MetricsMixin] Incrementing Prometheus counter for '{action}'")
        super().execute(action)
        print(f" -> [MetricsMixin] Metrics recorded.")


# Diamond Inheritance: PaymentService inherits from both Mixins
class PaymentService(AuditMixin, MetricsMixin):
    def execute(self, action: str):
        print(f"[PaymentService] Starting payment flow for '{action}'")
        super().execute(action)
        print(f"[PaymentService] Payment flow finished successfully.")


if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: METHOD RESOLUTION ORDER (MRO) & COOPERATIVE MULTIPLE INHERITANCE")
    print("=" * 70)

    # 1. Let's inspect the MRO order calculated by Python:
    print("\n[Step 1: Inspecting the MRO of PaymentService]")
    mro_classes = [cls.__name__ for cls in PaymentService.__mro__]
    print(" -> ".join(mro_classes))

    # 2. Let's run the method and watch the cooperative call chain:
    print("\n[Step 2: Executing PaymentService.execute()]")
    service = PaymentService()
    service.execute("CHARGE_CARD_100_USD")

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS FOR SENIOR INTERVIEWS:")
    print("1. AuditMixin's super().execute() called MetricsMixin, NOT BaseService!")
    print("2. Python uses C3 Linearization to guarantee every class in the diamond")
    print("   is visited exactly ONCE without duplicate calls.")
    print("=" * 70)
