import ibm_cloud_sdk_core
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace
from DB import db_connect
from ibmcloudant.cloudant_v1 import AllDocsQuery, Document, CloudantV1
import re

