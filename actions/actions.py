#!/usr/bin/env python
# coding=utf-8
'''
Date: 2022-01-27 14:09:33
LastEditors: Chunbai_zz
LastEditTime: 2022-02-16 14:24:16
Description: message
'''
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Dict, Text, Any, List
from area_sort import area_transfor
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

class Node:
    def __init__(self, parent, name, type):
        self.parent = parent
        self.name = name
        self.type = type

class DriverForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "driver_done"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["date_time", "address_from", "address_to"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        address_to = tracker.get_slot('address_to')
        address_from = tracker.get_slot('address_from')
        date_time = tracker.get_slot('date_time')
        print([str(date_time), str(address_to), str(address_from)])
        dispatcher.utter_message("正在为您查询{}从{}到{}的货物".format(str(date_time), str(area_transfor(address_from)), str(area_transfor(address_to))))
        return []

