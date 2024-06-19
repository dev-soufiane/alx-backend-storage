#!/usr/bin/env python3
"""
Script to insert a document into a MongoDB collection using keyword arguments.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into a MongoDB collection
    based on keyword arguments.
    """
    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id
