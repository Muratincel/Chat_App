# Simple Encrypted Chat App - Progress Summary

## 1️⃣ Project Setup
- Created a **Flask backend** to handle API requests.
- Used **SQLite** as the initial database (planning to migrate to Supabase later).
- Set up **frontend with HTML, CSS, and JavaScript** for the chat UI.

## 2️⃣ Backend Development
- Built API endpoints:
  - `/get_messages` → Fetch stored messages.
  - `/send_message` → Save new messages to the database.
- Configured **CORS (Cross-Origin Resource Sharing)** to allow frontend-backend communication.
- Implemented a **database model** to store messages with timestamps.

## 3️⃣ Frontend Integration
- Developed a **basic chat UI** in `index.html`.
- Connected frontend to backend using **AJAX requests** to send & receive messages.
- Messages are displayed dynamically on the page.

## 4️⃣ Timezone Handling
- Stored message timestamps in **UTC** format.
- Converted timestamps to **local time** before displaying in the frontend.
- Used **pytz** for accurate timezone conversion.

## 5️⃣ Next Steps
- Implement **real-time updates** (WebSockets or polling).
- Deploy the app using **free hosting providers** (Render, Supabase, Vercel, etc.).
- Explore **notifications** (SMS, email, or browser alerts).

🚀 **Project is working but needs real-time updates & deployment!**

