import os
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "document_ai")
class MemoryCursor:
	def __init__(self, documents):
		self._documents = list(documents)

	def sort(self, field, direction=-1):
		self._documents = sorted(
			self._documents,
			key=lambda doc: doc.get(field) or 0,
			reverse=direction == -1,
		)
		return self

	def __iter__(self):
		return iter(self._documents)

	def __len__(self):
		return len(self._documents)


class MemoryCollection:
	def __init__(self):
		self._documents = []

	def _matches(self, doc, query):
		if not query:
			return True
		for key, expected in query.items():
			actual = doc.get(key)
			if actual != expected:
				return False
		return True

	def insert_one(self, document):
		stored = dict(document)
		stored.setdefault("_id", ObjectId())
		self._documents.append(stored)
		return SimpleNamespace(inserted_id=stored["_id"])

	def find(self, query=None):
		query = query or {}
		return MemoryCursor(doc for doc in self._documents if self._matches(doc, query))

	def find_one(self, query=None):
		query = query or {}
		for doc in self._documents:
			if self._matches(doc, query):
				return doc
		return None

	def delete_one(self, query=None):
		query = query or {}
		for index, doc in enumerate(self._documents):
			if self._matches(doc, query):
				del self._documents[index]
				return

	def delete_many(self, query=None):
		query = query or {}
		self._documents = [doc for doc in self._documents if not self._matches(doc, query)]


def _build_mongo_collection():
	client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
	try:
		client.admin.command("ping")
		database = client[DATABASE_NAME]
		return database["documents"]
	except PyMongoError:
		return MemoryCollection()


documents_collection = _build_mongo_collection()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
