from tools import search_listings, suggest_outfit, create_fit_card

def test_search_returns_results():
    # Tests happy path search with keyword scoring
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    # Tests failure mode: Returns empty list instead of crashing
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []

def test_search_size_and_price_filter():
    # Tests size substring match (e.g., 'm' matching 'S/M') and price constraint
    results = search_listings("y2k", size="m", max_price=20)
    assert all(item["price"] <= 20 for item in results)
    assert all("m" in item.get("size", "").lower() for item in results)

def test_suggest_outfit_empty_wardrobe():
    # Tests failure mode: Graceful fallback when wardrobe is empty
    dummy_item = {"title": "Test Tee", "description": "A cool shirt", "style_tags": ["cool"]}
    empty_wardrobe = {"items": []}
    
    result = suggest_outfit(dummy_item, empty_wardrobe)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Error" not in result

def test_create_fit_card_empty_outfit():
    # Tests failure mode: Guard clause catches empty outfit string
    dummy_item = {"title": "Test Tee", "price": 10, "platform": "depop"}
    result = create_fit_card("   ", dummy_item) # Testing with whitespace
    
    assert result == "Error: Could not generate a fit card because the outfit suggestion is missing."