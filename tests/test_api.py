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

def test_price_invalid_query_1(client):
    pairs = ".btc_usd,None_Btc,do_t_eth,eth,tes.ting,"
    assert client.get(f"/prices?currency_pairs={pairs}").status_code == 400

def test_price_invalid_query_2(client):
    pairs = ",,wbt*c_eur,,,bt!c_usD"
    assert client.get(f"/prices?currency_pairs={pairs}").status_code == 400

def test_price_response_type(client):
    pairs = "ksm_dot,kyl_usdt,bnb_gbp,testing_usd,"
    response = json.loads(client.get(f"/prices?currency_pairs={pairs}").data.decode("utf8"))
    assert isinstance(response, dict)

def test_price_response_structure_1(client):
    pairs = "uni_eth,link_aud,ltc_jpy,testing_usd"
    response = json.loads(client.get(f"/prices?currency_pairs={pairs}").data.decode("utf8"))
    assert isinstance(response["sources"], dict)
    assert isinstance(response["completed_at"], str)
    assert isinstance(response["started_at"], str)

def test_price_response_structure_2(client):
    pairs = "doge_eur,fil_btc,xlm_gbp,kyl_testing"
    response = json.loads(client.get(f"/prices?currency_pairs={pairs}").data.decode("utf8"))
    for source in response["sources"].values():
        for pair in source.values():
            assert isinstance(pair["payload"], dict) or isinstance(pair["payload"], float)
            assert isinstance(pair["processed_at"], str)
            assert isinstance(pair["source"], str)