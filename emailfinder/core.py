import time

from emailfinder.utils.finder import google
from emailfinder.utils.finder import bing
from emailfinder.utils.finder import baidu
from emailfinder.utils.finder import yandex
from emailfinder.utils.color_print import print_error, print_ok
from concurrent.futures import ThreadPoolExecutor, as_completed

SEARCH_ENGINES_METHODS = {
    "google": google.search,
    "bing": bing.search,
    "baidu": baidu.search,
    "yandex": yandex.search
}

data_emails = []
data_list = []


def _search(engine, target):
    emails = None
    print(f"Searching in {engine}...")
    try:
        emails = SEARCH_ENGINES_METHODS[engine](target)
        print_ok(f"{engine} done!")
    except Exception as ex:
        print_error(f"{engine} error {ex}")
    return emails


def _get_emails(target):
    threads = 4
    emails = set()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_emails = {executor.submit(_search, engine, target): engine for engine in SEARCH_ENGINES_METHODS.keys()}
        for i, future in enumerate(as_completed(future_emails)):
            try:
                searcher_list = ['bing', 'google', 'baidu', 'yandex']
                data = future.result()
                print(f"{searcher_list[i]}: {data}")
                for value in data:
                    data_result = {
                        f"Find_in_{searcher_list[i]}": value
                    }
                    data_list.append(data_result)
                if data:
                    emails = emails.union(data)
            except Exception as e:
                print_error(f"Error: {e}")
    return data_list


def processing(target):
    data_emails = _get_emails(target)
    return data_emails