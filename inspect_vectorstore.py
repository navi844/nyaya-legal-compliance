from __future__ import annotations

from vectorstore import get_client


def inspect() -> list[dict]:
    client = get_client()
    collections = client.list_collections()
    items = []
    for collection in collections:
        items.append({'name': collection.name, 'count': collection.count()})
    return items


if __name__ == '__main__':
    print(inspect())
