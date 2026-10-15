#!/usr/bin/env python3
"""Print a bookstore inventory report from MongoDB Atlas."""

import logging
import os
import sys
# I'm not sure why the pymongo import doesn't work, but the uv script still runs
from pymongo import MongoClient

# Credentials come from the environment, never from this file.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Mix loaded authors (002, 003) with the author added in Case Study 1.
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

"""Print each listed author and the books linked by author_ids."""
# Count how many of the requested ids exist in the authors collection.
def print_author_report(authors, books, author_ids):
    total = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {total}")
    print()

    for author_id in author_ids:
        author = authors.find_one({"_id": author_id})
        if author is None:
            log.warning("No author document for %s", author_id)
            continue

        print(author["name"])
        # A book matches when this author's _id appears in author_ids.
        for book in books.find({"author_ids": author["_id"]}):
            print(f"  {book['title']} ({book['published_year']})")
        print()

"""Connect to Atlas, print the author/book report, and close the client."""
def main():
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        log.error(
            "Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, and MONGODB_ATLAS_PWD"
        )
        sys.exit(1)

    client = None
    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        # Ping so a bad password fails here instead of on the first query.
        client.admin.command("ping")
        log.info("Connected to MongoDB Atlas")

        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        print_author_report(authors, books, AUTHOR_IDS)
    except Exception:
        log.exception("Failed to connect or query MongoDB")
        sys.exit(1)
    finally:
        if client is not None:
            client.close()
            log.info("Closed MongoDB client")


if __name__ == "__main__":
    main()
