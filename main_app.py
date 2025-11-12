"""
Main Dual-Panel Desktop Application
Left Panel: AI Tutor
Right Panel: Financial Planning App
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import webbrowser
import subprocess
import os
import sys
from pathlib import Path
import json
from azure_services import AzureServicesManager
from ai_tutor import AITutor


class DualPanelApp:
    """Main application with dual panels"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Planning Assistant - AI Tutor & Planning App")
        self.root.geometry("1400x800")
        
        # Initialize Azure services
        self.azure_manager = AzureServicesManager()
        self.load_configuration()
        
        # Initialize AI Tutor
        self.ai_tutor = AITutor(self.azure_manager)
        
        # Setup UI
        self.setup_ui()
        
        # Streamlit process
        self.streamlit_process = None
        self.streamlit_port = 8501
        
    def load_configuration(self):
        """Load Azure configuration from file or environment"""
        config_file = Path(__file__).parent / "config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                self.azure_manager.initialize_from_config(config)
                return
            except Exception as e:
                print(f"Error loading config file: {e}")
        
        # Fallback to environment variables
        self.azure_manager.initialize_from_env()
    
    def setup_ui(self):
        """Setup the dual-panel user interface"""
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Left Panel - AI Tutor
        self.setup_left_panel(main_container)
        
        # Separator
        separator = ttk.Separator(main_container, orient=tk.VERTICAL)
        separator.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=5)
        
        # Right Panel - Financial Planning App
        self.setup_right_panel(main_container)
        
        # Status bar at the bottom
        self.setup_status_bar()
    
    def setup_left_panel(self, parent):
        """Setup the left panel with AI Tutor"""
        left_panel = ttk.Frame(parent, padding="5")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        left_panel.grid_rowconfigure(2, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ttk.Label(left_panel, text="🤖 AI Tutor", 
                         font=('Helvetica', 16, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Tutorial Topics Section
        topics_frame = ttk.LabelFrame(left_panel, text="Quick Topics", padding="5")
        topics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Topics dropdown
        topics_label = ttk.Label(topics_frame, text="Select a tutorial topic:")
        topics_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.topics_var = tk.StringVar()
        topics = self.ai_tutor.get_tutorial_topics()
        self.topics_dropdown = ttk.Combobox(topics_frame, textvariable=self.topics_var,
                                           values=topics, state='readonly', width=35)
        self.topics_dropdown.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        load_topic_btn = ttk.Button(topics_frame, text="Load Tutorial",
                                    command=self.load_tutorial)
        load_topic_btn.grid(row=2, column=0, sticky=tk.W)
        
        # Chat/Conversation Area
        chat_frame = ttk.LabelFrame(left_panel, text="Conversation", padding="5")
        chat_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        # Chat history display
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD,
                                                      width=50, height=20,
                                                      font=('Arial', 10))
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="blue", font=('Arial', 10, 'bold'))
        self.chat_display.tag_config("assistant", foreground="green", font=('Arial', 10))
        self.chat_display.tag_config("system", foreground="gray", font=('Arial', 9, 'italic'))
        
        # Initial welcome message
        self.add_chat_message("system", "Welcome! I'm your AI tutor. I can help you understand how the financial planning app works. Ask me anything!")
        
        # Input area
        input_frame = ttk.Frame(left_panel)
        input_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.question_entry = ttk.Entry(input_frame, font=('Arial', 10))
        self.question_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.question_entry.bind('<Return>', lambda e: self.ask_question())
        
        ask_btn = ttk.Button(input_frame, text="Ask", command=self.ask_question)
        ask_btn.grid(row=0, column=1)
        
        # Action buttons
        action_frame = ttk.Frame(left_panel)
        action_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
        clear_btn = ttk.Button(action_frame, text="Clear Chat",
                              command=self.clear_chat)
        clear_btn.grid(row=0, column=0, padx=(0, 5))
        
        tips_btn = ttk.Button(action_frame, text="Quick Tips",
                            command=self.show_quick_tips)
        tips_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Voice and translation buttons (if Azure services available)
        if self.azure_manager.tts_client:
            speak_btn = ttk.Button(action_frame, text="🔊 Speak Last",
                                 command=self.speak_last_response)
            speak_btn.grid(row=0, column=2, padx=(0, 5))
    
    def setup_right_panel(self, parent):
        """Setup the right panel with Financial Planning App"""
        right_panel = ttk.Frame(parent, padding="5")
        right_panel.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.grid_rowconfigure(2, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ttk.Label(right_panel, text="💰 Financial Planning App",
                         font=('Helvetica', 16, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Description
        desc = ttk.Label(right_panel, 
                        text="Budget planning and investment tracking application",
                        font=('Arial', 10))
        desc.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)
        
        # Launch button
        launch_frame = ttk.Frame(right_panel)
        launch_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        self.launch_btn = ttk.Button(launch_frame, text="🚀 Launch Financial App",
                                    command=self.launch_streamlit_app,
                                    style='Accent.TButton')
        self.launch_btn.grid(row=0, column=0, pady=10)
        
        self.stop_btn = ttk.Button(launch_frame, text="⏹ Stop App",
                                  command=self.stop_streamlit_app,
                                  state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=(10, 0), pady=10)
        
        # App status
        status_frame = ttk.LabelFrame(right_panel, text="App Status", padding="10")
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.app_status_label = ttk.Label(status_frame, 
                                         text="Status: Not Running",
                                         font=('Arial', 10))
        self.app_status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Info text
        info_text = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD,
                                              width=50, height=15,
                                              font=('Arial', 9))
        info_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        app_info = """
📊 Financial Planning App Features:

• Budget Tracking: Monitor your monthly income, expenses, and savings
• Investment Planning: Track multiple investment types (stocks, bonds, crypto, etc.)
• Net Worth Projection: See your financial growth over time
• Visual Analytics: Interactive charts and graphs
• AI Suggestions: Get personalized financial advice from multiple AI models
• Real-time Data: Fetch live market data from Alpha Vantage
• Chatbot Integration: Ask questions to your financial assistant

💡 How to Use:
1. Click "Launch Financial App" button above
2. The app will open in your web browser
3. Enter your financial information in the sidebar
4. Explore the charts and visualizations
5. Get AI-powered suggestions for your financial plan

❓ Need Help?
Ask the AI Tutor (left panel) any questions about:
- How to use the app
- Understanding the calculations
- Financial planning tips
- How the app is built
        """
        info_text.insert('1.0', app_info)
        info_text.config(state=tk.DISABLED)
    
    def setup_status_bar(self):
        """Setup status bar at the bottom"""
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Ready", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
        
        # Azure services status
        services_status = []
        if self.azure_manager.chat_client:
            services_status.append("Chat✓")
        if self.azure_manager.tts_client:
            services_status.append("TTS✓")
        if self.azure_manager.stt_client:
            services_status.append("STT✓")
        if self.azure_manager.translator_client:
            services_status.append("Translator✓")
        
        if services_status:
            azure_label = ttk.Label(status_frame, 
                                   text=f"Azure: {' '.join(services_status)}",
                                   anchor=tk.E)
            azure_label.pack(side=tk.RIGHT, padx=5, pady=2)
        else:
            azure_label = ttk.Label(status_frame,
                                   text="Azure: Not Configured",
                                   foreground="orange",
                                   anchor=tk.E)
            azure_label.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def add_chat_message(self, role: str, message: str):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        if role == "user":
            self.chat_display.insert(tk.END, "You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif role == "assistant":
            self.chat_display.insert(tk.END, "AI Tutor: ", "assistant")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif role == "system":
            self.chat_display.insert(tk.END, f"ℹ️ {message}\n\n", "system")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def ask_question(self):
        """Handle user question"""
        question = self.question_entry.get().strip()
        if not question:
            return
        
        # Clear entry
        self.question_entry.delete(0, tk.END)
        
        # Add to chat
        self.add_chat_message("user", question)
        
        # Get response in thread to avoid blocking UI
        def get_response():
            self.update_status("AI Tutor is thinking...")
            response = self.ai_tutor.ask(question)
            self.add_chat_message("assistant", response)
            self.last_response = response
            self.update_status("Ready")
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def load_tutorial(self):
        """Load selected tutorial topic"""
        topic = self.topics_var.get()
        if not topic:
            messagebox.showinfo("Select Topic", "Please select a tutorial topic first.")
            return
        
        content = self.ai_tutor.get_tutorial_content(topic)
        self.add_chat_message("system", f"Tutorial: {topic}")
        self.add_chat_message("assistant", content)
    
    def clear_chat(self):
        """Clear the chat history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.ai_tutor.reset_conversation()
        self.add_chat_message("system", "Chat cleared. How can I help you?")
    
    def show_quick_tips(self):
        """Show quick tips"""
        tips = self.ai_tutor.get_quick_tips()
        tips_text = "\n".join(tips)
        self.add_chat_message("system", "Quick Tips:")
        self.add_chat_message("assistant", tips_text)
    
    def speak_last_response(self):
        """Speak the last AI response using TTS"""
        if not hasattr(self, 'last_response'):
            messagebox.showinfo("No Response", "No response to speak yet.")
            return
        
        if not self.azure_manager.tts_client:
            messagebox.showwarning("TTS Not Available", 
                                 "Text-to-Speech service is not configured.")
            return
        
        def speak():
            self.update_status("Converting text to speech...")
            audio_data = self.ai_tutor.speak_response(self.last_response)
            if audio_data:
                # Save and play audio
                audio_file = Path("/tmp/response.mp3")
                with open(audio_file, 'wb') as f:
                    f.write(audio_data)
                
                # Try to play audio (platform-specific)
                try:
                    if sys.platform == "win32":
                        os.startfile(audio_file)
                    elif sys.platform == "darwin":
                        subprocess.run(["open", audio_file])
                    else:
                        subprocess.run(["xdg-open", audio_file])
                    self.update_status("Playing audio...")
                except Exception as e:
                    messagebox.showerror("Playback Error", f"Could not play audio: {e}")
            else:
                messagebox.showerror("TTS Error", "Failed to generate speech.")
            self.update_status("Ready")
        
        threading.Thread(target=speak, daemon=True).start()
    
    def launch_streamlit_app(self):
        """Launch the Streamlit financial planning app"""
        if self.streamlit_process and self.streamlit_process.poll() is None:
            messagebox.showinfo("Already Running", 
                              "The financial app is already running.")
            return
        
        app_file = Path(__file__).parent / "budget_invest_app.py"
        if not app_file.exists():
            messagebox.showerror("File Not Found",
                               "budget_invest_app.py not found!")
            return
        
        # Check if Streamlit is installed
        try:
            result = subprocess.run([sys.executable, "-m", "streamlit", "--version"],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Streamlit Not Installed",
                                   "Please install Streamlit: pip install streamlit")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Could not check Streamlit: {e}")
            return
        
        # Launch Streamlit in background
        try:
            self.streamlit_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", str(app_file),
                 "--server.port", str(self.streamlit_port),
                 "--server.headless", "true"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Update UI
            self.launch_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.app_status_label.config(text=f"Status: Running on port {self.streamlit_port}")
            self.update_status(f"Financial app launched on port {self.streamlit_port}")
            
            # Open browser after a short delay
            def open_browser():
                import time
                time.sleep(3)
                webbrowser.open(f"http://localhost:{self.streamlit_port}")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch app: {e}")
            self.launch_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def stop_streamlit_app(self):
        """Stop the Streamlit app"""
        if self.streamlit_process and self.streamlit_process.poll() is None:
            self.streamlit_process.terminate()
            self.streamlit_process.wait()
            
            # Update UI
            self.launch_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.app_status_label.config(text="Status: Not Running")
            self.update_status("Financial app stopped")
        else:
            messagebox.showinfo("Not Running", "The financial app is not running.")
    
    def update_status(self, message: str):
        """Update the status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def on_closing(self):
        """Handle window closing"""
        if self.streamlit_process and self.streamlit_process.poll() is None:
            if messagebox.askokcancel("Quit", 
                                     "The financial app is still running. Stop and quit?"):
                self.stop_streamlit_app()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DualPanelApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
