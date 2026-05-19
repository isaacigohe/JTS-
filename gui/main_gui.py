import tkinter as tk
from tkinter import ttk, messagebox
import re, webbrowser
from bson.objectid import ObjectId
from database.db_manager import DBManager
from scraper.remoteok_scraper import RemoteOKScraper
from scraper.remotive_scraper import RemotiveScraper
from scraper.arbeitnow_scraper import ArbeitnowScraper
from scraper.fuzu_scraper import FuzuScraper
# IMPORT OUR BRAND NEW STYLES AND PALETTES
import gui.styles as theme

def clean_html(raw_html):
    if not raw_html: return "No description available."
    # Strip complex structural layout elements smoothly
    text = re.sub(r'</?(p|br|div|li|h1|h2|h3|ol|ul)>', '\n', raw_html)
    cleantext = re.sub(r'<.*?>', '', text)
    for old, new in [('&nbsp;', ' '), ('&amp;', '&'), ('&quot;', '"'), ('â', '—')]:
        cleantext = cleantext.replace(old, new)
    return re.sub(r'\n\s*\n+', '\n\n', cleantext).strip()

class MainWindow:
    def __init__(self, master, user):
        self.master = master
        self.master.title("JTS - Job Tracking System")
        
        # FIX ISSUE 2 (Screen Size adjustment for visible footer)
        self.master.geometry("1100x680") 
        self.master.configure(bg=theme.GREY_BG)
        
        self.user = user
        self.db_manager = DBManager()
        self.jobs_collection = self.db_manager.get_collection("jobs")
        self.saved_jobs_collection = self.db_manager.get_collection("saved_jobs")
        
        # Trigger Style Configurations
        theme.apply_global_styles()
        self.setup_ui()
        self.load_jobs()

    def setup_ui(self):
        # 1. Executive Top Header Banner Block
        header_frame = tk.Frame(self.master, bg=theme.NAVY, height=70)
        header_frame.pack(fill="x", side="top")

        tk.Label(header_frame, text="JTS | JOB TRACKER", font=("Helvetica", 16, "bold"), bg=theme.NAVY, fg=theme.WHITE, padx=20).pack(side="left", pady=15)

        user_info = tk.Frame(header_frame, bg=theme.NAVY)
        user_info.pack(side="right", padx=20)
        tk.Label(user_info, text=f"👤 {self.user['email']}", font=("Arial", 10), bg=theme.NAVY, fg=theme.GREY_BG).pack(side="top", anchor="e")
        theme.create_btn(user_info, "Logout", self.logout, role="danger").pack(side="top", anchor="e", pady=2)

        # 2. Search / Action Interactivity Bar Area
        action_bar = tk.Frame(self.master, bg=theme.WHITE, pady=10, padx=20)
        action_bar.pack(fill="x")

        search_frame = tk.Frame(action_bar, bg=theme.WHITE)
        search_frame.pack(side="left")
        tk.Label(search_frame, text="Search Jobs:", font=("Arial", 10), bg=theme.WHITE, fg=theme.TEXT_MAIN).pack(side="left")
        
        self.search_entry = theme.create_input(search_frame, width=32)
        self.search_entry.pack(side="left", padx=10)
        theme.create_btn(search_frame, "Search", self.search_jobs).pack(side="left")

        theme.create_btn(action_bar, " Refresh Database", self.refresh_jobs, role="refresh").pack(side="right")

        # 3. Main Data Core Presentation Grid View Table (Treeview)
        # Compacted vertical padding from 20 to 10 to keep components inside standard layouts
        table_container = tk.Frame(self.master, bg=theme.GREY_BG, padx=20, pady=10)
        table_container.pack(fill="both", expand=True)

        cols = ("Title", "Company", "Location", "Source", "Status")
        self.tree = ttk.Treeview(table_container, columns=cols, show="headings", selectmode="browse")
        
        widths = {"Title": 350, "Company": 180, "Location": 150, "Source": 110, "Status": 110}
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=widths[c], anchor="center")
        self.tree.column("Title", anchor="w") 
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # 4. Lower Profile Data Commands Panel (Compact structure layout padding)
        footer = tk.Frame(self.master, bg=theme.WHITE, pady=10, padx=20)
        footer.pack(fill="x", side="bottom")
        
        theme.create_btn(footer, "Save Job", self.save_job).pack(side="left", padx=(0, 15))
        theme.create_btn(footer, "View Saved Jobs", self.view_saved_jobs).pack(side="left", padx=15)
        theme.create_btn(footer, "Update Status", self.update_status).pack(side="left", padx=15)
        theme.create_btn(footer, "Remove Saved Job", self.delete_saved_job, role="secondary").pack(side="left", padx=15)

    def load_jobs(self, query=None):
        for item in self.tree.get_children(): 
            self.tree.delete(item)
            
        jobs = self.jobs_collection.find(query) if query else self.jobs_collection.find().limit(100)
        
        for job in jobs:
            if "_id" in job:
                rid = str(job["_id"])
            else:
                rid = str(job.get("job_id", job.get("url", "unknown_id")))
                
            # PERSISTENT CROSS-REFERENCE CHECK:
            # Check if this logged-in user has saved or applied to this job in 'saved_jobs'
            user_interaction = self.saved_jobs_collection.find_one({
                "user_id": self.user["_id"], 
                "job_id": rid
            })
            
            # If a record exists in MongoDB, read its status. Otherwise, show "Available"
            display_status = user_interaction["status"] if user_interaction else "Available"
                
            self.tree.insert("", "end", iid=rid, values=(
                job.get("title", "Untitled"), 
                job.get("company", "Unknown"),
                job.get("location", "Remote"), 
                job.get("source", "Unknown"), 
                display_status  # Displays the true persistent state from MongoDB!
            ))
    def refresh_jobs(self):
        messagebox.showinfo("JTS", "Connecting to live servers and updating database...")
        
        # Initialize your list of scrapers
        scrapers = [RemoteOKScraper(), RemotiveScraper(), ArbeitnowScraper(), FuzuScraper()]
        all_jobs = []
        
        # Run each scraper separately so if one fails, the others still work!
        for s in scrapers:
            try: 
                scraped_data = s.scrape_jobs()
                if scraped_data:
                    all_jobs.extend(scraped_data)
                    print(f"[Sync] {s.__class__.__name__} successfully pulled {len(scraped_data)} items.")
            except Exception as e: 
                print(f"[Sync Error] Failed running {s.__class__.__name__}: {e}")
                
        # CONSTANT STORAGE VERIFICATION ENGINE
        if all_jobs:
            try:
                # 1. Clear out old temporary cache records safely
                self.jobs_collection.delete_many({})
                
                # 2. Clean out any potential hardcoded '_id' fields that cause MongoDB crashes
                for job in all_jobs:
                    if '_id' in job:
                        del job['_id']  # Let MongoDB generate a clean, fresh, permanent unique ID
                
                # 3. Execute bulk write operation into MongoDB 'jobs' collection
                result = self.jobs_collection.insert_many(all_jobs)
                
                # Verify insertion count right in your terminal console
                print(f"[Database Persistence] Successfully stored {len(result.inserted_ids)} records into MongoDB!")
                
                # 4. Reload the treeview layout visually
                self.load_jobs()
                messagebox.showinfo("Success", f"Database Synchronized! Permanent records stored: {len(result.inserted_ids)}")
                
            except Exception as e:
                print(f"[Database Drop Error] Critical write block: {e}")
                messagebox.showerror("Database Write Error", f"Could not store records to MongoDB jobs collection: {e}")
        else:
            messagebox.showwarning("Sync Warning", "Scrapers returned 0 active listings. Check internet connection or terminal logs.")
    def search_jobs(self):
        # FIX ISSUE 2 (Dynamic Search matching all fields)
        k = self.search_entry.get().strip()
        if k: 
            self.load_jobs({"$or": [
                {"title": {"$regex": k, "$options": "i"}}, 
                {"company": {"$regex": k, "$options": "i"}},
                {"source": {"$regex": k, "$options": "i"}},
                {"location": {"$regex": k, "$options": "i"}}
            ]})
        else: 
            self.load_jobs()

    def save_job(self):
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Selection Error", "Please select a job from the list first.")
            return
            
        jid = sel[0]  # Get the unique ID (MongoDB ObjectId string)
        
        # Check if this user has already interacting with this job document
        existing = self.saved_jobs_collection.find_one({"user_id": self.user["_id"], "job_id": jid})
        
        if existing:
            messagebox.showinfo("JTS Profile", "This job is already saved or tracked in your profile!")
            return
            
        # Permanent Write Operation directly to MongoDB saved_jobs collection
        tracking_data = {
            "user_id": self.user["_id"], 
            "job_id": jid, 
            "status": "Saved"
        }
        
        self.saved_jobs_collection.insert_one(tracking_data)
        
        # Visually update the status in your UI table immediately
        self.tree.set(jid, "Status", "Saved")
        messagebox.showinfo("Success", "Job permanently logged into your MongoDB 'saved_jobs' collection!")
    def view_saved_jobs(self):
        saved = [r["job_id"] for r in self.saved_jobs_collection.find({"user_id": self.user["_id"]})]
        obj_ids = []
        for s in saved:
            try: obj_ids.append(ObjectId(s))
            except: pass
        self.load_jobs({"$or": [{"_id": {"$in": obj_ids}}, {"job_id": {"$in": saved}}]})
        for item in self.tree.get_children():
            rel = self.saved_jobs_collection.find_one({"user_id": self.user["_id"], "job_id": item})
            if rel: self.tree.set(item, "Status", rel["status"])

    def update_status(self):
        sel = self.tree.selection()
        if not sel: return
        jid = sel[0]
        rel = self.saved_jobs_collection.find_one({"user_id": self.user["_id"], "job_id": jid})
        if not rel: return
        new = "Applied" if rel["status"] == "Saved" else "Saved"
        self.saved_jobs_collection.update_one({"_id": rel["_id"]}, {"$set": {"status": new}})
        self.tree.set(jid, "Status", new)

    def delete_saved_job(self):
        sel = self.tree.selection()
        if not sel: return
        jid = sel[0]
        self.saved_jobs_collection.delete_one({"user_id": self.user["_id"], "job_id": jid})
        self.tree.delete(jid)

    def on_item_double_click(self, event):
        sel = self.tree.selection()
        if sel:
            jid = sel[0]
            job = None
            
            # Try finding the document by its native MongoDB object ID first
            try:
                if len(jid) == 24:
                    job = self.jobs_collection.find_one({"_id": ObjectId(jid)})
            except:
                pass
                
            # Fallback fallback search matrix check if it wasn't a standard ObjectId
            if not job:
                job = self.jobs_collection.find_one({"$or": [
                    {"job_id": jid},
                    {"url": jid}
                ]})
                
            if job: 
                self.show_details(job)

    def show_details(self, job):
        win = tk.Toplevel(self.master)
        win.title("Job Details")
        win.geometry("650x550")
        win.configure(bg=theme.WHITE)
        
        # 1. TOP HEADER
        h = tk.Frame(win, bg=theme.NAVY, pady=15, padx=20)
        h.pack(fill="x", side="top")
        tk.Label(h, text=job.get('title', 'Untitled'), font=("Helvetica", 13, "bold"), bg=theme.NAVY, fg=theme.WHITE, wraplength=600).pack(anchor="w")
        tk.Label(h, text=f" {job.get('company', 'Unknown')}  |   {job.get('location', 'Remote')}", bg=theme.NAVY, fg=theme.GREY_BG, font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        
        # 2. DESIGNED FOOTER BUTTON BAR
        apply_footer = tk.Frame(win, bg=theme.GREY_BG, pady=12, padx=20)
        apply_footer.pack(fill="x", side="bottom")
        
        url = job.get('url') or job.get('link') or job.get('apply_url')
        jid = str(job.get("_id")) # Get the underlying ID string to update collections
        
        # This function runs when you click "Apply Now"
        def execute_application(target_url, job_id):
            # 1. Open the live application page in your web browser
            webbrowser.open(target_url)
            
            # 2. FORCE MONGODB TO PERMANENTLY UPDATE THE 'jobs' COLLECTION
            try:
                # Find the job by its ObjectId and add/change a 'status' field to 'Applied'
                if len(job_id) == 24:
                    self.jobs_collection.update_one(
                        {"_id": ObjectId(job_id)},
                        {"$set": {"status": "Applied"}}
                    )
                    print(f"[MongoDB Update] Successfully updated status to 'Applied' inside 'jobs' collection for ID: {job_id}")
            except Exception as e:
                print(f"[MongoDB Error] Failed to update 'jobs' collection: {e}")
            
            # 3. Update the UI table visually right away
            try:
                self.tree.set(job_id, "Status", "Applied")
            except:
                pass
            print(f"[Database] Job {job_id} successfully stored as 'Applied' for User {self.user['_id']}.")

        # --- ALIGNED TO THE RIGHT ---
        btn_cancel = theme.create_btn(apply_footer, "Cancel", win.destroy, role="danger")
        btn_cancel.pack(side="right", padx=(10, 0))
        
        if url:
            # Trigger our inline DB logging function right when they hit Apply Now!
            btn_apply = theme.create_btn(apply_footer, "Apply Now", lambda: execute_application(url, jid), role="primary")
            btn_apply.pack(side="right")
        else:
            lbl_no_link = tk.Label(apply_footer, text="⚠️ No application URL provided", fg=theme.TEXT_MUTED, bg=theme.GREY_BG, font=("Arial", 10, "italic"))
            lbl_no_link.pack(side="right")

        # 3. CENTER CONTENT - Description Text Area
        t = tk.Text(win, font=("Arial", 10), padx=15, pady=15, wrap="word", bg=theme.WHITE, fg=theme.TEXT_MAIN, relief="flat")
        t.insert("1.0", clean_html(job.get("description", "")))
        t.config(state="disabled")
        t.pack(fill="both", expand=True) 
    def logout(self):
        self.master.destroy()
        from gui.login_gui import LoginWindow
        root = tk.Tk()
        
        # Make sure to pass your active DBManager class here as well
        from database.db_manager import DBManager
        LoginWindow(root, auth_manager=DBManager())
        root.mainloop()