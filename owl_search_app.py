import tkinter as tk
from tkinter import filedialog, messagebox
import rdflib

class OWLSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OWL Search Tool")

        self.language = "TH"
        self.graph = None

        self.load_owl_file()

        # ปุ่มเลือกไฟล์ OWL
        # self.btn_load = tk.Button(root, text="เลือกไฟล์ OWL", command=self.load_owl_file)
        # self.btn_load.pack(pady=5)


        # ช่องป้อนคำค้นหา
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        self.label_search = tk.Label(input_frame, text="ค้นหาจังหวัด:")
        self.label_search.pack(side='left', padx=5)

        self.entry_search = tk.Entry(input_frame, width=50)
        self.entry_search.pack(side='left', padx=5)

        # ปุ่มเปลี่ยนภาษา
        self.btn_change_lang = tk.Button(input_frame, text="TH", command=self.change_language)
        self.btn_change_lang.pack(pady=5)

        # ปุ่มค้นหา
        search_button_frame = tk.Frame(root)
        search_button_frame.pack(pady=10)

        self.btn_search0 = tk.Button(search_button_frame, text="ต้นไม้", command=lambda: self.search_owl('tree'))
        self.btn_search0.pack(side="left", padx=5)
    
        self.btn_search1 = tk.Button(search_button_frame, text="ดอกไม้", command=lambda: self.search_owl('flower'))
        self.btn_search1.pack(side="left", padx=5)

        self.btn_search2 = tk.Button(search_button_frame, text="ชื่อท้องถิ่น", command=lambda: self.search_owl('trad_name'))
        self.btn_search2.pack(side="left", padx=5)

        self.btn_search3 = tk.Button(search_button_frame, text="พิกัด", command=lambda: self.search_owl('coordinate'))
        self.btn_search3.pack(side="left", padx=5)

        self.btn_search4 = tk.Button(search_button_frame, text="คำขวัญ", command=lambda: self.search_owl('motto'))
        self.btn_search4.pack(side="left", padx=5)

        self.btn_search5 = tk.Button(search_button_frame, text="ตรา", command=lambda: self.search_owl('seal'))
        self.btn_search5.pack(side="left", padx=5)

        self.btn_search6 = tk.Button(search_button_frame, text="รูป", command=lambda: self.search_owl('image'))
        self.btn_search6.pack(side="left", padx=5)

        self.btn_search7 = tk.Button(search_button_frame, text="URL", command=lambda: self.search_owl('URL'))
        self.btn_search7.pack(side="left", padx=5)

        # กล่องข้อความแสดงผล
        self.text_result = tk.Text(root, height=10, width=80)
        self.text_result.pack(pady=5)

    def load_owl_file(self):
        # file_path = filedialog.askopenfilename(filetypes=[("OWL files", "*.owl")])
        file_path = 'mytourism.owl'
        if file_path:
            self.graph = rdflib.Graph()
            self.graph.parse(file_path, format="xml")
            # messagebox.showinfo("โหลดสำเร็จ", "โหลดไฟล์ OWL สำเร็จ!")

    def change_language(self):
        if self.language == "TH":
            self.language = "EN"
        else:
            self.language = "TH"
        self.btn_change_lang.config(text=self.language)

    def search_owl(self, search_type):
        if not self.graph:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกไฟล์ OWL ก่อน!")
            return
        
        query_str = self.entry_search.get().strip()
    
        # เพิ่ม Prefix
        prefix = "PREFIX tourism: <http://www.my_ontology.edu/mytourism#>"

        if search_type == 'flower':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?flower WHERE {{
                ?a 
                tourism:hasNameOfProvince ?name .
                OPTIONAL {{ ?a tourism:hasFlower ?flower . }}

                FILTER (langMatches(lang(?name), "{self.language}"))
                FILTER (!bound(?flower) || langMatches(lang(?flower), "{self.language}"))

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """

        elif search_type == 'tree':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?tree WHERE {{
                ?a 
                tourism:hasNameOfProvince ?name .
                OPTIONAL {{ ?a tourism:hasTree ?tree . }}

                FILTER (langMatches(lang(?name), "{self.language}"))
                FILTER (!bound(?tree) || langMatches(lang(?tree), "{self.language}"))

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """

        elif search_type == 'trad_name':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?tradname WHERE {{
                ?a 
                tourism:hasNameOfProvince ?name;
                tourism:hasTraditionalNameOfProvince ?tradname;

                FILTER (langMatches(lang(?name), "{self.language}"))
                FILTER (langMatches(lang(?tradname), "{self.language}"))

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """
        elif search_type == 'coordinate':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?latitude ?longitude WHERE {{
                ?a tourism:hasNameOfProvince ?name .
                OPTIONAL {{ ?a tourism:hasLatitudeOfProvince ?latitude . }}
                OPTIONAL {{ ?a tourism:hasLongitudeOfProvince ?longitude . }}

                FILTER (langMatches(lang(?name), "{self.language}"))

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """
        elif search_type == 'motto':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?motto WHERE {{
                ?a 
                tourism:hasNameOfProvince ?name;
                tourism:hasMotto ?motto;

                FILTER (langMatches(lang(?name), "{self.language}"))
                FILTER (langMatches(lang(?motto), "{self.language}"))

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """
        elif search_type == 'seal':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?seal WHERE {{
                ?a 
                tourism:hasNameOfProvince ?name;
                tourism:hasSeal ?seal;

                FILTER (langMatches(lang(?name), "{self.language}"))
                FILTER (langMatches(lang(?seal), "{self.language}"))

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """
        elif search_type == 'image':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?image WHERE {{
                ?a 
                tourism:hasNameOfProvince ?name;
                tourism:hasImageOfProvince ?image;

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """
        elif search_type == 'URL':
            sparql_query = f"""
            {prefix}
            SELECT ?name ?URL WHERE {{
                ?a 
                tourism:hasNameOfProvince ?name;
                tourism:hasURLOfProvince ?URL;

                FILTER (regex(str(?name), "{query_str}", "i"))
            }}
            """

        results = self.graph.query(sparql_query)

        self.text_result.delete("1.0", tk.END)  # เคลียร์ผลลัพธ์เก่า
        for row in results:
            if search_type == 'tree':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name}, ต้นไม้: {row.tree}\n")
            elif search_type == 'flower':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name}, ดอกไม้: {row.flower}\n")
            elif search_type == 'trad_name':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name}, ชื่อท้องถิ่น: {row.tradname}\n")
            elif search_type == 'coordinate':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name} \nละติจูด: {row.latitude}, ลองจิจูด: {row.longitude}")
            elif search_type == 'motto':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name} \nคำขวัญ: {row.motto}")
            elif search_type == 'seal':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name} \nตรา: {row.seal}")
            elif search_type == 'image':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name} \nรูป: {row.image}")
            elif search_type == 'URL':
                self.text_result.insert(tk.END, f"จังหวัด: {row.name} \nURL: {row.URL}")
                

if __name__ == "__main__":
    root = tk.Tk()
    app = OWLSearchApp(root)
    root.mainloop()
