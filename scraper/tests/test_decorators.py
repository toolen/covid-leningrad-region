from scraper.decorators import retry_on_failure


def test_retry_on_failure():
    tries = 3

    @retry_on_failure(interval_between_retries_sec=0.1)
    def test_function():
        nonlocal tries
        if tries != 1:
            tries -= 1
            raise Exception()
        else:
            return True

    assert test_function()
