Travel Destination Suggester

By: Clara, Karina, Logan, Reanne

Project Overview:
The Travel Destination Suggester is an interactive web application designed to recommend the ideal vacation spot based on user preferences. The quiz asks users 9 questions about their travel style and preferences, then suggests a destination tailored to their responses. Whether you're looking for a relaxing beach, an adventurous mountain retreat, or a cultural city escape, this quiz will help guide your travel plans.

---

Features:

User Login/Sign-Up  
Users can sign up with a unique username and password.  
Passwords are securely hashed before storing in a JSON file.  
Existing users can log in to access the quiz.

Interactive Quiz  
The quiz asks users about travel preferences (e.g., relaxation vs. adventure, preferred climate).  
A progress bar shows how many questions remain.  
Users cannot proceed to the next question until an answer is provided.

Destination Results  
Based on quiz answers, users receive a recommended destination.  
For each destination, the page provides:  
- Local food recommendations  
- Must-visit places and attractions  
- Activities to do in the destination country

Retake Option  
After receiving results, users can easily retake the quiz by clicking a "Try Again" button.

Log Out Option  
Users can log out at any time to return to the login page.

Error Handling  
If a destination page is not linked or an error occurs, the application displays a custom error page to guide the user.



Technologies Used:

Backend:  
Flask (Python): Handles the web application's backend, including user login, session management, and quiz routing.

Frontend:  
HTML: Provides the structure of the application.  
CSS: Styles the web pages and ensures a user-friendly layout.  

Data Storage:  
JSON File: Stores user credentials, quiz responses, and destination preferences securely in a user_data.json file.

---

How It Works:

1. User Login/Sign-Up:  
   Users can create an account by providing a unique username and password.  
   Upon successful login, users are directed to the quiz page.

2. Interactive Quiz:  
   Users answer 9 questions about their travel preferences (e.g., type of vacation, preferred climate, etc.).  
   A progress bar is displayed to show the user's progress.  
   Each question must be answered before the user can proceed.

3. Destination Recommendation:  
   After completing the quiz, the app calculates the best destination based on the answers.  
   The destination results page displays the recommended location along with details about:  
   - Local food, must-visit places, and activities.

4. Retake Quiz:  
   Users can retake the quiz by clicking the "Try Again" button to get new results.

5. Log Out:  
   Users can log out of their accounts to return to the login page.

6. Error Handling:  
   If a destination is not properly linked in the routing, a custom error page will be displayed to the user.



