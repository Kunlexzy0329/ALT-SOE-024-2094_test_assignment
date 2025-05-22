from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']

    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


# ============Test to update the book=============
def test_update_book():
    # First, add a book to update
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    add_response = client.post("/books", json=payload)
    add_book_data = add_response.json()
    book_id = add_book_data['data']['id']

    # Prepare updated data using partial update (BookUpdate schema allows partial fields)
    updated_payload = {
        "title": "Johny bravo updated",
        "year": 2024,
        "pages": 600
        # 'author' and 'language' are omitted to test partial update
    }
    update_response = client.put(f"/books/{book_id}", json=updated_payload)
    assert update_response.status_code == 200
    update_book_data = update_response.json()
    assert update_book_data["message"] == "Book updated successfully"
    assert update_book_data["data"]["title"] == "Johny bravo updated"
    assert update_book_data["data"]["year"] == 2024
    assert update_book_data["data"]["pages"] == 600

    # The fields not updated should remain as before
    assert update_book_data["data"]["author"] == "John Doe"
    assert update_book_data["data"]["language"] == "English"

# ======Test update bok not found
def test_update_book_not_found():
    # Try updating a book with a non-existent ID
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    updated_payload = {
        "title": "Non-existent Book",
        "year": 2025,
        "pages": 100
    }
    response = client.put(f"/books/{non_existent_id}", json=updated_payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Book with id: {non_existent_id} not found"


# ============test to delete a book==========
def test_delete_book():
    # Add a book to delete
    payload = {
        "title": "Book to Delete",
        "author": "Jane Doe",
        "year": 2022,
        "pages": 300,
        "language": "English"
        }
    add_response = client.post("/books", json=payload)
    book_id = add_response.json()["data"]["id"]

    # Delete the book
    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == "Book deleted successfully"

    # Try to get the deleted book
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


def test_delete_book_not_found():
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/books/{non_existent_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Book with id: {non_existent_id} not found"