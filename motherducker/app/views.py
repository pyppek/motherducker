from django.shortcuts import render
from viewflow import frontend
from viewflow.base import Flow

# hello world demo

@frontend.register
class HelloWorldFlow(Flow):
    ...