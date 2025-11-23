# **🎓 Veridia Student Information System (Web-SSIS)**

Welcome to the repository for **Veridia**, the Simple Student Information System (SSIS) web application. This application provides a modern dashboard for managing students, academic programs, and colleges.

## **✨ Technologies**

| Component | Technology |
| :---- | :---- |
| **Frontend** | Vue 3 (Vite) |
| **Styling** | Tailwind CSS / DaisyUI |
| **Backend** | Python Flask (Pipenv) |

## **🚀 Local Setup Guide**

Follow these instructions to get both the backend API and the frontend client running locally.

### **1\. ⚙️ Backend Setup (Python/Flask)**

This process sets up the Flask API that handles data and authentication.

1. **Navigate to the backend directory:**  
   cd backend

2. **Install dependencies and create virtual environment:**  
   pipenv install

3. **Activate the virtual environment:**  
   pipenv shell  
   💡 *Note: All subsequent commands for the backend should be run while the virtual environment is active.*  
4. Create and Configure Environment Variables:  
   Copy the example configuration to a new .env file:  
   cp .env.example .env

   Now, open the **.env** file and add your required configuration (e.g., DATABASE\_URI, SECRET\_KEY, etc.).  
5. **Run the Development Server:**  
   flask run

   The API will now be running (usually at http://127.0.0.1:5000).

### **2\. 🖥️ Frontend Setup (Vue/Vite)**

The frontend is configured to build directly into the backend's dist folder for production, but should be run separately for development.

1. **Navigate to the frontend directory:**  
   cd frontend

   *(Ensure you are in a separate terminal window, or exit the backend shell first, unless your IDE handles simultaneous servers.)*  
2. **Install dependencies using npm:**  
   npm install

3. **Start the Frontend Development Server (Hot Reload):**  
   npm run dev

### **3\. 📦 Production Build**

Use this command when ready to deploy or serve the app using the Flask server.

1. **Compile and Minify for Production (Deploys files to backend/dist):**  
   npm run build  
