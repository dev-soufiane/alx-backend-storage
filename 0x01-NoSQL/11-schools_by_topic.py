#!/usr/bin/env python3
"""
Script to find schools offering a specific topic in a MongoDB collection.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns a cursor to retrieve schools offering a specific topic.
    """
    return mongo_collection.find({"topics": topic})
