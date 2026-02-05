# **CONNECTLY PROJECT**

**MO-IT152 - Integrative Programming and Technologies S3101**  
**Team Members:** Joyce Ferrer, Ryu Ken Lindo

---

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

**2.1 Install Django:**  
pip install django


**2.2 Install Django REST Framework (DRF):**  
pip install djangorestframework


**2.3 Install JWT authentication for DRF:**  
pip install djangorestframework-simplejwt


**2.4 Install CORS headers for API requests:**  
pip install django-cors-headers

**2.5 Install below for HTTPS:**  
pip show Werkzeug

pip install django-extensions

pip install pyOpenSSL

Git Bash app

---

## **3. Verify installation**

**3.1 Check Django version:**  
python -m django --version


**3.2 Check DRF installation:**  
pip show djangorestframework
