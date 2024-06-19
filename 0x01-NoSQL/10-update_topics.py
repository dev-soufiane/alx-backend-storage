#!/usr/bin/env python3
"""
Script to update topics of a school document in a MongoDB collection.
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
