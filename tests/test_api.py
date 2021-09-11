import pytest
import json
from api.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    assert client.get("/health").status_code == 200

def test_price_valid_query(client):
    pairs = " btc_usd ,ETH_GBP,kyl_aud"
    assert client.get(f"/prices?currency_pairs={pairs}").status_code == 200

def test_price_invalid(client):
    pairs = ".btc_usd,None_Btc,do_t_eth,test,tes_ting!,"
    assert client.get(f"/prices?currency_pairs={pairs}").status_code == 404

def test_price_response_type(client):
    pairs = "ksm_dot,kyl_usdt,bnb_gbp"
    response = json.loads(client.get(f"/prices?currency_pairs={pairs}").data.decode("utf8"))
    assert isinstance(response, dict)

def test_price_response_structure(client):
    pairs = "uni_eth,link_aud,ltc_jpy,testing_usd"
    response = json.loads(client.get(f"/prices?currency_pairs={pairs}").data.decode("utf8"))
    assert isinstance(response["payload"], list)
    assert isinstance(response["completed_at"], str)
    assert isinstance(response["started_at"], str)
    for price in response["payload"]:
        assert isinstance(price["price"], (float, int))
        for key,value in price.items():
            if key != "price":
                assert isinstance(value, str)
