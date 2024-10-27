// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore"; // Import Firestore
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD4Ke3QaVYR5P5lTe8EsXEMv0eVegmPzJQ",
  authDomain: "research-project-8003b.firebaseapp.com",
  projectId: "research-project-8003b",
  storageBucket: "research-project-8003b.appspot.com",
  messagingSenderId: "257310846877",
  appId: "1:257310846877:web:57768ca96d913039c10974",
  measurementId: "G-D9XS4T9DGV"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app); // Initialize Firestore

export { auth, db }; // Export both auth and db
