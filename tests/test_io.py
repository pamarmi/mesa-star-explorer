from mesa_star_explorer.io import load_mesa_table


def test_loading():
    meta, data = load_mesa_table("examples/sample_LOGS/history_1M.data")

    assert len(data) > 0
    assert "star_age" in data.columns