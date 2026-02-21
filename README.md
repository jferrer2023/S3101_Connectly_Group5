# **CONNECTLY PROJECT**

**MO-IT152 - Integrative Programming and Technologies S3101**  
**Team Members:** Joyce Ferrer, Ryu Ken Lindo

---

## **Test Users**
root: root (Admin)

Moderator1: abcd1234! (Moderator)

User1: abcd1234!

User2: abcd1234!

## **1. Project Setup**

### **1.1 Create the virtual environment**
Create a virtual environment named `venv`:

python -m venv venv



### **1.2 Activate the virtual environment**

**Windows:**  
venv\Scripts\activate


**macOS / Linux:**  
source venv/bin/activate


---

## **2. Install required packages**

- pip install django
- pip install djangorestframework
- pip install djangorestframework-simplejwt
- pip install django-cors-headers
- pip install Werkzeug
- pip install django-extensions
- pip install pyOpenSSL

---

## **3. Verify installation**

- python -m django --version
- pip show djangorestframework

---

## **4. Design Patterns Testing**

**4.1 Singleton:**  
python singletons/test_logger.py

python -m singletons.test_singleton


**4.2 Factory Pattern:**  
python factories/test_post_factory.py

---

**CMD Command to Run:**  

python manage.py runserver_plus 127.0.0.1:8000 --cert-file cert.pem --key-file key.pem

**Web Links:**  

MS2

- https://127.0.0.1:8000/api-auth/login/
- https://127.0.0.1:8000/posts/posts/
- https://127.0.0.1:8000/posts/posts/1/
- https://127.0.0.1:8000/posts/posts/1/like/
- https://127.0.0.1:8000/posts/posts/1/comments/
- https://127.0.0.1:8000/posts/posts/1/comments/11/
- https://127.0.0.1:8000/posts/feed
- https://127.0.0.1:8000/posts/posts/?page=2
- https://127.0.0.1:8000/posts/posts/1/comments/?page=2
- https://127.0.0.1:8000/posts/feed/?page=2


MS1

- Login Page - https://127.0.0.1:8000/api-auth/login/
- Home Page - https://127.0.0.1:8000/posts/posts/
- User Management - https://127.0.0.1:8000/posts/users/
- Select a User to Amend/Delete e.g. id:3 - https://127.0.0.1:8000/posts/users/3/ 
- Select a post to Amend/Delete e.g. id:2 - https://127.0.0.1:8000/posts/posts/2/
- Comments - https://127.0.0.1:8000/posts/comments
- Select a comment to Amend/Delete e.g. id:26 - https://127.0.0.1:8000/posts/comments/26/

- https://127.0.0.1:8000/tasks/tasks/
- https://127.0.0.1:8000/tasks/users/

