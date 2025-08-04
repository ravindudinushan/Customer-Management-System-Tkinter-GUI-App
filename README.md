# ✨ Customer Management System (Tkinter GUI App)

A modern and responsive **Customer Management System** built with Python and Tkinter. This application allows users to **add, view, search, and track customers**, including **daily sequence tracking** and **Sinhala voice notifications** using Google Text-to-Speech.

---

## 🚀 Features

- 📥 Add new customers with auto-generated ID and daily sequence number  
- 🔍 Advanced customer search by Name, ID, or Daily Number  
- 📅 View all or today's customers separately  
- 🧾 Real-time statistics (Total & Today’s customer count)  
- 🗣️ Sinhala voice notification using `gTTS`  
- 📊 Stylish and responsive UI with modern colors and layout  
- 🔄 Auto-updating digital clock and status bar  
- 📦 SQLite database integration (local and portable)  

---

## 🛠️ Technologies Used

| Tech / Library       | Purpose                                  |
|----------------------|------------------------------------------|
| `Python`             | Core language                            |
| `Tkinter`            | GUI framework                            |
| `ttk` (Themed Tk)    | Enhanced styling for modern widgets      |
| `SQLite3`            | Embedded database for persistence        |
| `gTTS`               | Google Text-to-Speech (Sinhala)          |
| `playsound`          | Playback of TTS-generated audio          |
| `datetime`           | Time tracking for sequences & clock      |
| `os` & `random`      | ID generation and file management        |

---

## 🧠 How It Works

- Customers are added with a unique ID and a daily sequence number.
- All records are stored in an SQLite database.
- You can filter or search customer data using several fields.
- The app plays a Sinhala welcome message when a new customer is added.

---
