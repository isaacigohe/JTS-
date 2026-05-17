import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DBManager
from scraper.remoteok_scraper import RemoteOKScraper
from scraper.remotive_scraper import RemotiveScraper
from scraper.dice_scraper import DiceScraper
from scraper.fuzu_scraper import FuzuScraper
from scraper.nodesk_scraper import NoDeskScraper

class MainWindow:
    def __init__(self, master, user):
        self.master = master
        self.master.title("Job Listing Tracker System (JTS)")
        self.master.geometry("1000x700")
        
        self.user = user
        self.db_manager = DBManager()
        self.jobs_collection = self.db_manager.get_collection("jobs")
        self.saved_jobs_collection = self.db_manager.get_collection("saved_jobs")
        
        self.setup_ui()
        self.load_jobs()

    def setup_ui(self):
        # Top Control Panel
        control_panel = tk.Frame(self.master)
        control_panel.pack(fill="x", padx=10, pady=10)
        
        tk.Label(control_panel, text=f"Logged in as: {self.user['email']}", font=("Arial", 10, "bold")).pack(side="left")
                
        self.refresh_button = tk.Button(control_panel, text="Refresh Jobs", command=self.refresh_jobs)
        self.refresh_button.pack(side="right", padx=5)
        
        self.search_entry = tk.Entry(control_panel)
        self.search_entry.pack(side="right", padx=5)
        
        tk.Button(control_panel, text="Search", command=self.search_jobs).pack(side="right")

    # Main Content Area (Treeview)
        self.tree = ttk.Treeview(self.master, columns=("Title", "Company", "Location", "Source", "Status"), show="headings")
        self.tree.heading("Title", text="Job Title")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Source", text="Source")
        self.tree.heading("Status", text="Status")
                
        self.tree.column("Title", width=300)
        self.tree.column("Company", width=200)
        self.tree.column("Location", width=150)
        self.tree.column("Source", width=100)
        self.tree.column("Status", width=100)
                
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Bottom Action Panel
        action_panel = tk.Frame(self.master)
        action_panel.pack(fill="x", padx=10, pady=10)
        
        tk.Button(action_panel, text="Save Job", command=self.save_job).pack(side="left", padx=5)
        tk.Button(action_panel, text="View Saved Jobs", command=self.view_saved_jobs).pack(side="left", padx=5)
        tk.Button(action_panel, text="Update Status", command=self.update_status).pack(side="left", padx=5)
        tk.Button(action_panel, text="Delete Saved Job", command=self.delete_saved_job).pack(side="left", padx=5)

    def load_jobs(self, query=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
                
        if query:
            jobs = self.jobs_collection.find(query)
        else:
            jobs = self.jobs_collection.find().limit(100)
            
        for job in jobs:
            self.tree.insert("", "end", iid=str(job["_id"]), values=(
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("source"),
                "Available"
            ))

    def refresh_jobs(self):
        messagebox.showinfo("Info", "Scraping new jobs from multiple sources... Please wait.")
        scrapers = [
            RemoteOKScraper(), 
            RemotiveScraper(),
            DiceScraper(),
            FuzuScraper(),
            NoDeskScraper()
        ]
        all_jobs = []
        for s in scrapers:
            try:
                jobs = s.scrape_jobs()
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"Error with {s.__class__.__name__}: {e}")
                
        if all_jobs:
            self.jobs_collection.delete_many({})
            self.jobs_collection.insert_many(all_jobs)
            self.load_jobs()
            messagebox.showinfo("Success", f"Scraped {len(all_jobs)} jobs from multiple sources successfully!")
        else:
            messagebox.showwarning("Warning", "No jobs found or error during scraping.")

    def search_jobs(self):
        keyword = self.search_entry.get()
        if keyword:
            query = {"$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"company": {"$regex": keyword, "$options": "i"}},
                {"description": {"$regex": keyword, "$options": "i"}}
            ]}
            self.load_jobs(query)
        else:
            self.load_jobs()

    def save_job(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a job to save.")
            return
                
        job_id = selected_item[0]
        if self.saved_jobs_collection.find_one({"user_id": self.user["_id"], "job_id": job_id}):
            messagebox.showinfo("Info", "Job already saved.")
            return
            
        self.saved_jobs_collection.insert_one({
            "user_id": self.user["_id"],
            "job_id": job_id,
            "status": "Saved"
        })
        messagebox.showinfo("Success", "Job saved successfully!")

    def view_saved_jobs(self):
        saved_relations = self.saved_jobs_collection.find({"user_id": self.user["_id"]})
        saved_ids = [r["job_id"] for r in saved_relations]
                
        from bson.objectid import ObjectId
        query = {"_id": {"$in": [ObjectId(sid) for sid in saved_ids]}}
        self.load_jobs(query)
        
        for item in self.tree.get_children():
            rel = self.saved_jobs_collection.find_one({"user_id": self.user["_id"], "job_id": item})
            if rel:
                self.tree.set(item, "Status", rel["status"])

    def update_status(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a saved job.")
            return
                
        job_id = selected_item[0]
        rel = self.saved_jobs_collection.find_one({"user_id": self.user["_id"], "job_id": job_id})
        if not rel:
            messagebox.showwarning("Warning", "This job is not in your saved list.")
            return
            
        new_status = "Applied" if rel["status"] == "Saved" else "Saved"
        self.saved_jobs_collection.update_one(
            {"_id": rel["_id"]},
            {"$set": {"status": new_status}}
        )
        self.tree.set(job_id, "Status", new_status)

    def delete_saved_job(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a job to remove.")
            return
                
        job_id = selected_item[0]
        self.saved_jobs_collection.delete_one({"user_id": self.user["_id"], "job_id": job_id})
        self.tree.delete(job_id)
        messagebox.showinfo("Success", "Job removed from saved list.")

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            job_id = selected_item[0]
            from bson.objectid import ObjectId
            job = self.jobs_collection.find_one({"_id": ObjectId(job_id)})
            if job:
                self.show_details(job)

    def show_details(self, job):
        import webbrowser
        import re
        def clean_html(raw_html):
            if not raw_html: return "No description available."
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', raw_html)
            cleantext = cleantext.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
            return cleantext.strip()
            
        details_win = tk.Toplevel(self.master)
        details_win.title(f"Job Details - {job['company']}")
        details_win.geometry("700x600")
        details_win.configure(bg="#f0f2f5")
        
        header = tk.Frame(details_win, bg="#ffffff", padx=20, pady=20)
        header.pack(fill="x")
        tk.Label(header, text=job['title'], font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#1a73e8", wraplength=650, justify="left").pack(anchor="w")
        tk.Label(header, text=job['company'], font=("Helvetica", 14), bg="#ffffff", fg="#5f6368").pack(anchor="w", pady=(5, 0))
                
        info_bar = tk.Frame(header, bg="#ffffff", pady=10)
        info_bar.pack(fill="x")
                
        tk.Label(info_bar, text=f"📍 {job['location']}", font=("Helvetica", 10), bg="#ffffff", fg="#3c4043").pack(side="left", padx=(0, 20))
        tk.Label(info_bar, text=f"💰 {job.get('salary', 'Not specified')}", font=("Helvetica", 10), bg="#ffffff", fg="#3c4043").pack(side="left")
        
        content_frame = tk.Frame(details_win, bg="#f0f2f5", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        tk.Label(content_frame, text="Job Description", font=("Helvetica", 12, "bold"), bg="#f0f2f5", fg="#202124").pack(anchor="w", pady=(0, 10))
        
        desc_text = tk.Text(content_frame, wrap="word", font=("Helvetica", 11), bg="#ffffff", padx=15, pady=15, relief="flat")
        desc_text.insert("1.0", clean_html(job.get("description", "")))
        desc_text.config(state="disabled")
        desc_text.pack(fill="both", expand=True)
        
        footer = tk.Frame(details_win, bg="#ffffff", padx=20, pady=15)
        footer.pack(fill="x")
        
        tk.Button(footer, text="Apply Now", bg="#1a73e8", fg="white", font=("Helvetica", 10, "bold"), padx=20, pady=8, relief="flat", cursor="hand2", command=lambda: webbrowser.open(job.get('url', ''))).pack(side="right", padx=5)
        tk.Button(footer, text="Close", font=("Helvetica", 10), padx=20, pady=8, command=details_win.destroy).pack(side="right")