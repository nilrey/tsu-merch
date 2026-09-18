import re
from backend.models.product import Product, ProductImage, ProductParameter
from backend.models.order import OrderRequest, OrderItemRequest, FeedbackRequest

results = []

# Test 1: Valid product with hex colors
try:
    p = Product(
        key="tshirt",
        name="Футболка",
        description="Тест",
        price=1800,
        colors=["#29488B", "#000000"]
    )
    results.append(f"✅ Valid product with hex colors: OK")
except Exception as e:
    results.append(f"❌ Valid product with hex colors: FAILED - {e}")

# Test 2: Invalid hex color
try:
    Product(key="t", name="t", description="d", price=100, colors=["invalid"])
    results.append(f"❌ Invalid hex color should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Invalid hex color rejected: OK")

# Test 3: Negative price
try:
    Product(key="t", name="t", description="d", price=-5)
    results.append(f"❌ Negative price should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Negative price rejected: OK")

# Test 4: Valid order with consent
try:
    o = OrderRequest(
        name="Иван Иванов",
        email="test@example.com",
        items=[OrderItemRequest(product_key="tshirt", color="#29488B")],
        consent=True,
        honeypot=""
    )
    results.append(f"✅ Valid order with consent: OK")
except Exception as e:
    results.append(f"❌ Valid order: FAILED - {e}")

# Test 5: Empty items
try:
    OrderRequest(name="Test", email="t@t.com", items=[], consent=True)
    results.append(f"❌ Empty items should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Empty items rejected: OK")

# Test 6: Consent false
try:
    OrderRequest(
        name="Test", email="t@t.com",
        items=[OrderItemRequest(product_key="tshirt", color="#29488B")],
        consent=False
    )
    results.append(f"❌ Consent false should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Consent false rejected: OK")

# Test 7: Honeypot filled (spam trap)
try:
    OrderRequest(
        name="Test", email="t@t.com",
        items=[OrderItemRequest(product_key="tshirt", color="#29488B")],
        consent=True, honeypot="spam"
    )
    results.append(f"❌ Honeypot filled should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Honeypot filled rejected: OK")

# Test 8: Valid feedback (email)
try:
    f = FeedbackRequest(
        name="Test",
        contact_type="email",
        email="test@example.com",
        message="Hello",
        consent=True,
        honeypot=""
    )
    results.append(f"✅ Valid feedback (email): OK")
except Exception as e:
    results.append(f"❌ Valid feedback (email): FAILED - {e}")

# Test 9: Feedback phone without phone
try:
    FeedbackRequest(
        name="Test", contact_type="phone",
        phone=None, message="Hello", consent=True
    )
    results.append(f"❌ Phone feedback without phone should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Phone feedback without phone rejected: OK")

# Test 10: Feedback email without email
try:
    FeedbackRequest(
        name="Test", contact_type="email",
        email=None, message="Hello", consent=True
    )
    results.append(f"❌ Email feedback without email should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Email feedback without email rejected: OK")

# Test 11: Feedback consent false
try:
    FeedbackRequest(
        name="Test", contact_type="email",
        email="t@t.com", message="Hi", consent=False
    )
    results.append(f"❌ Feedback consent false should fail: FAILED - did not raise")
except Exception:
    results.append(f"✅ Feedback consent false rejected: OK")

for r in results:
    print(r)

passed = sum(1 for r in results if r.startswith("✅"))
failed = sum(1 for r in results if r.startswith("❌"))
print(f"\nResults: {passed} passed, {failed} failed")
